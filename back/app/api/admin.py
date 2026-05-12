"""
============================================
管理工具 API - 导入导出、未引用文件管理
============================================
"""

import os
import io
import zipfile
import shutil
import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from app.core.config import settings
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.moment import Moment
from app.models.motto import Motto
from app.models.book import Book

router = APIRouter(prefix="/api/admin", tags=["管理工具"])

# ============================================
# 导入导出
# ============================================

@router.get("/export")
async def export_data(current_user: User = Depends(get_current_user)):
    """
    导出所有数据（数据库 + 上传文件）为 ZIP 包
    """
    import tempfile
    
    # 创建临时 ZIP 文件
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    tmp_path = tmp.name
    tmp.close()
    
    try:
        with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 1. 导出数据库文件
            db_path = settings.DATABASE_URL.replace('sqlite:///', '')
            if os.path.exists(db_path):
                zf.write(db_path, 'data/blog.db')
            
            # 2. 导出上传文件
            upload_dir = settings.UPLOAD_DIR
            if os.path.exists(upload_dir):
                for root, dirs, files in os.walk(upload_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join('uploads', os.path.relpath(file_path, upload_dir))
                        zf.write(file_path, arcname)
            
            # 3. 导出元数据信息
            meta = f"""导出时间: {datetime.now().isoformat()}
站点名称: {current_user.site_name}
导出工具: 魂牵梦绕博客系统
"""
            zf.writestr('export_info.txt', meta)
        
        # 返回 ZIP 文件
        filename = f"blog-export-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        def iterfile():
            with open(tmp_path, 'rb') as f:
                yield from f
            os.unlink(tmp_path)
        
        return StreamingResponse(
            iterfile(),
            media_type='application/zip',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/import")
async def import_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """
    导入数据 ZIP 包
    注意：导入会覆盖现有数据库和上传文件！
    """
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="请上传 ZIP 文件")
    
    import tempfile
    
    # 保存上传的 ZIP
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    tmp_path = tmp.name
    tmp.close()
    
    try:
        contents = await file.read()
        with open(tmp_path, 'wb') as f:
            f.write(contents)
        
        # 解析 ZIP
        with zipfile.ZipFile(tmp_path, 'r') as zf:
            # 检查是否有数据库文件
            has_db = 'data/blog.db' in zf.namelist()
            
            # 备份当前数据库
            db_path = settings.DATABASE_URL.replace('sqlite:///', '')
            if os.path.exists(db_path) and has_db:
                backup_path = db_path + '.backup'
                shutil.copy2(db_path, backup_path)
            
            # 解压到临时目录
            extract_dir = tempfile.mkdtemp()
            zf.extractall(extract_dir)
            
            # 导入数据库
            if has_db:
                import_db_path = os.path.join(extract_dir, 'data', 'blog.db')
                if os.path.exists(import_db_path):
                    shutil.copy2(import_db_path, db_path)
            
            # 导入上传文件
            upload_src = os.path.join(extract_dir, 'uploads')
            if os.path.exists(upload_src):
                upload_dir = settings.UPLOAD_DIR
                # 清空现有上传目录
                if os.path.exists(upload_dir):
                    shutil.rmtree(upload_dir)
                os.makedirs(upload_dir, exist_ok=True)
                # 复制上传文件
                for item in os.listdir(upload_src):
                    src = os.path.join(upload_src, item)
                    dst = os.path.join(upload_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
            
            # 清理临时目录
            shutil.rmtree(extract_dir, ignore_errors=True)
        
        return {"message": "导入成功", "has_db": has_db}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ============================================
# 未引用文件管理
# ============================================

def _extract_image_urls(text: str) -> set:
    """从文本中提取所有图片 URL"""
    urls = set()
    if not text:
        return urls
    # 匹配 /uploads/ 开头的路径
    for m in re.finditer(r'/uploads/([^"\'\s,)]+)', text):
        urls.add(m.group(1))
    # 匹配 uploads/ 开头的路径
    for m in re.finditer(r'uploads/([^"\'\s,)]+)', text):
        urls.add(m.group(1))
    # 匹配完整 URL
    for m in re.finditer(rf'{re.escape(settings.BASE_URL)}/uploads/([^"\'\s,)]+)', text):
        urls.add(m.group(1))
    return urls


def _get_all_referenced_files() -> set:
    """获取所有被引用的文件名"""
    import asyncio
    
    referenced = set()
    
    # 从文章内容中提取
    posts = asyncio.get_event_loop().run_until_complete(Post.all().values('content', 'cover_url'))
    for p in posts:
        referenced.update(_extract_image_urls(p.get('content', '')))
        if p.get('cover_url'):
            referenced.update(_extract_image_urls(p['cover_url']))
    
    # 从动态中提取
    moments = asyncio.get_event_loop().run_until_complete(Moment.all().values('content', 'images'))
    for m in moments:
        referenced.update(_extract_image_urls(m.get('content', '')))
        if m.get('images'):
            for img in m['images'].split(','):
                referenced.update(_extract_image_urls(img.strip()))
    
    # 从语录中提取
    mottos = asyncio.get_event_loop().run_until_complete(Motto.all().values('content', 'images'))
    for m in mottos:
        referenced.update(_extract_image_urls(m.get('content', '')))
        if m.get('images'):
            for img in m['images'].split(','):
                referenced.update(_extract_image_urls(img.strip()))
    
    # 从书籍封面中提取
    books = asyncio.get_event_loop().run_until_complete(Book.all().values('cover_url'))
    for b in books:
        if b.get('cover_url'):
            referenced.update(_extract_image_urls(b['cover_url']))
    
    return referenced


@router.get("/orphan-files")
async def get_orphan_files(
    current_user: User = Depends(get_current_user),
):
    """
    扫描上传目录，找出未被任何内容引用的文件
    """
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        return {"files": [], "total_size": 0, "count": 0}
    
    # 获取所有被引用的文件名
    referenced = _get_all_referenced_files()
    
    # 扫描上传目录
    orphan_files = []
    total_size = 0
    
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if not os.path.isfile(file_path):
            continue
        
        # 检查是否被引用
        if filename not in referenced:
            stat = os.stat(file_path)
            orphan_files.append({
                "filename": filename,
                "size": stat.st_size,
                "size_display": _format_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_thumb": filename.startswith("thumb_"),
            })
            total_size += stat.st_size
    
    # 按修改时间排序（最新的在前）
    orphan_files.sort(key=lambda x: x['modified'], reverse=True)
    
    return {
        "files": orphan_files,
        "total_size": total_size,
        "total_size_display": _format_size(total_size),
        "count": len(orphan_files),
    }


@router.post("/orphan-files/move")
async def move_orphan_files(
    target_dir: str = Query(..., description="目标目录名"),
    filenames: list[str] = Query(..., description="要移动的文件名列表"),
    current_user: User = Depends(get_current_user),
):
    """
    将未引用文件移动到指定目录
    """
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        raise HTTPException(status_code=400, detail="上传目录不存在")
    
    # 创建目标目录
    target_path = os.path.join(upload_dir, target_dir)
    os.makedirs(target_path, exist_ok=True)
    
    moved = []
    errors = []
    
    for filename in filenames:
        src = os.path.join(upload_dir, filename)
        dst = os.path.join(target_path, filename)
        
        if not os.path.exists(src):
            errors.append({"filename": filename, "error": "文件不存在"})
            continue
        
        try:
            shutil.move(src, dst)
            moved.append(filename)
        except Exception as e:
            errors.append({"filename": filename, "error": str(e)})
    
    return {
        "message": f"成功移动 {len(moved)} 个文件",
        "moved": moved,
        "errors": errors,
    }


@router.post("/orphan-files/delete")
async def delete_orphan_files(
    filenames: list[str] = Query(..., description="要删除的文件名列表"),
    current_user: User = Depends(get_current_user),
):
    """
    删除未引用文件
    """
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        raise HTTPException(status_code=400, detail="上传目录不存在")
    
    deleted = []
    errors = []
    
    for filename in filenames:
        file_path = os.path.join(upload_dir, filename)
        
        if not os.path.exists(file_path):
            errors.append({"filename": filename, "error": "文件不存在"})
            continue
        
        try:
            os.remove(file_path)
            deleted.append(filename)
        except Exception as e:
            errors.append({"filename": filename, "error": str(e)})
    
    return {
        "message": f"成功删除 {len(deleted)} 个文件",
        "deleted": deleted,
        "errors": errors,
    }


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
