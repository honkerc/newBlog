"""
============================================
文件管理 API - 类似 ZFile 的静态文件管理
============================================
独立于 uploads 目录，专门管理一个文件目录。
支持密码访问保护。
"""

import os
import shutil
import mimetypes
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Header
from fastapi.responses import FileResponse, StreamingResponse
from app.core.config import settings
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/files", tags=["文件管理"])

# 文件存储目录
FILES_DIR = os.getenv("FILES_DIR", "./files")
# 访问密码（为空则不限制）
FILES_PASSWORD = os.getenv("FILES_PASSWORD", "")

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.json', '.xml', '.csv',
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.bmp',
    '.mp4', '.mp3', '.wav', '.ogg', '.flac',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.py', '.js', '.ts', '.html', '.css', '.vue', '.java', '.cpp', '.h',
    '.yaml', '.yml', '.toml', '.ini', '.cfg',
    '.sh', '.bat', '.ps1',
    '.iso', '.img',
    '.epub', '.mobi',
}


async def _verify_access(password: str = Query(""), x_password: str = Header(""), authorization: str = Header("")):
    """验证访问权限：支持密码验证或 JWT token 验证"""
    # 如果没有设置密码，直接放行
    if not FILES_PASSWORD:
        return True
    # 密码验证
    if password == FILES_PASSWORD or x_password == FILES_PASSWORD:
        return True
    # JWT token 验证（复用登录系统的 token）
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            from app.core.security import verify_token
            payload = verify_token(token)
            if payload:
                return True
        except:
            pass
    raise HTTPException(status_code=403, detail="访问被拒绝，请提供正确的密码或登录")


def _get_safe_path(path: str) -> str:
    """获取安全的文件路径，防止路径穿越"""
    # 规范化路径
    safe = os.path.normpath(path)
    # 移除开头的斜杠
    safe = safe.lstrip('/\\')
    # 拼接完整路径
    full = os.path.join(FILES_DIR, safe)
    # 确保在 FILES_DIR 内
    full = os.path.normpath(full)
    if not full.startswith(os.path.normpath(FILES_DIR)):
        raise HTTPException(status_code=400, detail="无效的路径")
    return full


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _get_file_info(path: str, base_path: str) -> dict:
    """获取文件信息"""
    stat = os.stat(path)
    rel_path = os.path.relpath(path, base_path)
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    
    return {
        "name": name,
        "path": rel_path.replace('\\', '/'),
        "is_dir": os.path.isdir(path),
        "size": stat.st_size if os.path.isfile(path) else 0,
        "size_display": _format_size(stat.st_size) if os.path.isfile(path) else "-",
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "ext": ext,
        "is_image": ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.bmp'),
        "is_video": ext in ('.mp4', '.webm', '.ogg', '.mov'),
        "is_audio": ext in ('.mp3', '.wav', '.ogg', '.flac', '.aac'),
        "is_text": ext in ('.txt', '.md', '.json', '.xml', '.csv', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.log'),
        "is_code": ext in ('.py', '.js', '.ts', '.html', '.css', '.vue', '.java', '.cpp', '.h', '.sh', '.bat', '.ps1'),
        "is_archive": ext in ('.zip', '.rar', '.7z', '.tar', '.gz'),
    }


@router.get("/list")
async def list_files(
    path: str = Query("", description="目录路径"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    列出目录中的文件和文件夹
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="路径不存在")
    
    if not os.path.isdir(target):
        raise HTTPException(status_code=400, detail="不是目录")
    
    items = []
    try:
        for name in sorted(os.listdir(target)):
            item_path = os.path.join(target, name)
            # 跳过隐藏文件
            if name.startswith('.'):
                continue
            items.append(_get_file_info(item_path, FILES_DIR))
    except PermissionError:
        raise HTTPException(status_code=403, detail="没有权限访问该目录")
    
    # 目录排在前面，文件排在后面
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    
    # 获取当前目录信息
    current_dir = _get_file_info(target, FILES_DIR) if path else {
        "name": "根目录",
        "path": "",
        "is_dir": True,
    }
    
    return {
        "items": items,
        "current": current_dir,
        "total": len(items),
    }


@router.get("/download")
async def download_file(
    path: str = Query(..., description="文件路径"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    下载文件
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if os.path.isdir(target):
        # 如果是目录，打包为 ZIP 下载
        import tempfile
        import zipfile
        
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        tmp_path = tmp.name
        tmp.close()
        
        try:
            with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(target):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(target))
                        zf.write(file_path, arcname)
            
            dir_name = os.path.basename(target)
            
            def iterfile():
                with open(tmp_path, 'rb') as f:
                    yield from f
                os.unlink(tmp_path)
            
            return StreamingResponse(
                iterfile(),
                media_type='application/zip',
                headers={'Content-Disposition': f'attachment; filename="{dir_name}.zip"'}
            )
        except Exception as e:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise HTTPException(status_code=500, detail=f"打包失败: {str(e)}")
    
    # 单个文件下载
    media_type, _ = mimetypes.guess_type(target)
    return FileResponse(
        target,
        media_type=media_type or 'application/octet-stream',
        filename=os.path.basename(target),
    )


@router.get("/preview")
async def preview_file(
    path: str = Query(..., description="文件路径"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    预览文件内容（文本文件）
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    if os.path.isdir(target):
        raise HTTPException(status_code=400, detail="不能预览目录")
    
    ext = os.path.splitext(target)[1].lower()
    text_exts = {'.txt', '.md', '.json', '.xml', '.csv', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.log',
                 '.py', '.js', '.ts', '.html', '.css', '.vue', '.java', '.cpp', '.h', '.sh', '.bat', '.ps1'}
    
    if ext not in text_exts:
        # 非文本文件直接返回文件
        media_type, _ = mimetypes.guess_type(target)
        return FileResponse(target, media_type=media_type or 'application/octet-stream')
    
    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            "filename": os.path.basename(target),
            "content": content,
            "size": os.path.getsize(target),
        }
    except UnicodeDecodeError:
        # 如果 UTF-8 解码失败，尝试其他编码
        try:
            with open(target, 'r', encoding='gbk') as f:
                content = f.read()
            return {
                "filename": os.path.basename(target),
                "content": content,
                "size": os.path.getsize(target),
            }
        except:
            raise HTTPException(status_code=400, detail="无法预览该文件")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    path: str = Query("", description="上传到哪个目录"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    上传文件
    """
    await _verify_access(password, x_password, authorization)
    
    target_dir = _get_safe_path(path)
    os.makedirs(target_dir, exist_ok=True)
    
    # 检查文件扩展名
    ext = os.path.splitext(file.filename)[1].lower()
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")
    
    # 生成不冲突的文件名
    filename = file.filename
    name, ext = os.path.splitext(filename)
    safe_name = "".join(c for c in name if c.isalnum() or c in "._- ").strip()
    if not safe_name:
        safe_name = "untitled"
    
    candidate = f"{safe_name}{ext}"
    file_path = os.path.join(target_dir, candidate)
    
    counter = 1
    while os.path.exists(file_path):
        candidate = f"{safe_name}({counter}){ext}"
        file_path = os.path.join(target_dir, candidate)
        counter += 1
    
    # 保存文件
    contents = await file.read()
    with open(file_path, 'wb') as f:
        f.write(contents)
    
    return {
        "message": "上传成功",
        "file": _get_file_info(file_path, FILES_DIR),
    }


@router.post("/mkdir")
async def create_directory(
    path: str = Query(..., description="目录路径"),
    name: str = Query(..., description="目录名"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    创建目录
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    new_dir = os.path.join(target, name)
    
    if os.path.exists(new_dir):
        raise HTTPException(status_code=400, detail="目录已存在")
    
    os.makedirs(new_dir, exist_ok=True)
    
    return {
        "message": "目录创建成功",
        "dir": _get_file_info(new_dir, FILES_DIR),
    }


@router.delete("/delete")
async def delete_item(
    path: str = Query(..., description="要删除的文件或目录路径"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    删除文件或目录
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="路径不存在")
    
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        return {"message": "删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@router.post("/rename")
async def rename_item(
    path: str = Query(..., description="原路径"),
    new_name: str = Query(..., description="新名称"),
    password: str = Query("", description="访问密码"),
    x_password: str = Header(""),
    authorization: str = Header(""),
):
    """
    重命名文件或目录
    """
    await _verify_access(password, x_password, authorization)
    
    target = _get_safe_path(path)
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="路径不存在")
    
    parent = os.path.dirname(target)
    new_path = os.path.join(parent, new_name)
    
    if os.path.exists(new_path):
        raise HTTPException(status_code=400, detail="目标已存在")
    
    os.rename(target, new_path)
    
    return {
        "message": "重命名成功",
        "file": _get_file_info(new_path, FILES_DIR),
    }
