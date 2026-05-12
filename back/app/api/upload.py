"""
============================================
文件上传 API
============================================
上传图片时自动生成压缩缩略图，前端默认显示缩略图，
点击图片时才加载原始图片，提升页面性能。
"""

import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.core.config import settings
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/upload", tags=["上传"])

# 缩略图配置
THUMB_MAX_WIDTH = 400      # 缩略图最大宽度
THUMB_QUALITY = 75         # 缩略图 JPEG 压缩质量
THUMB_PREFIX = "thumb_"    # 缩略图文件名前缀


def _resolve_filename(upload_dir: str, original_name: str) -> str:
    """生成不冲突的文件名，保留原始文件名，冲突时追加 (1) (2) 等后缀"""
    name, ext = os.path.splitext(original_name)
    # 清理文件名中的非法字符
    safe_name = "".join(c for c in name if c.isalnum() or c in "._- ").strip()
    if not safe_name:
        safe_name = "untitled"

    candidate = f"{safe_name}{ext}"
    file_path = os.path.join(upload_dir, candidate)
    if not os.path.exists(file_path):
        return candidate

    counter = 1
    while True:
        candidate = f"{safe_name}({counter}){ext}"
        file_path = os.path.join(upload_dir, candidate)
        if not os.path.exists(file_path):
            return candidate
        counter += 1


def _is_image(ext: str) -> bool:
    """判断文件扩展名是否为图片"""
    return ext.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')


def _create_thumbnail(upload_dir: str, filename: str):
    """
    为图片生成压缩缩略图。
    缩略图保存在同一目录，文件名加 thumb_ 前缀。
    非图片或生成失败时静默跳过。
    """
    name, ext = os.path.splitext(filename)
    if not _is_image(ext):
        return None

    try:
        from PIL import Image

        src_path = os.path.join(upload_dir, filename)
        thumb_name = f"{THUMB_PREFIX}{filename}"
        thumb_path = os.path.join(upload_dir, thumb_name)

        img = Image.open(src_path)

        # 转换为 RGB（处理 RGBA/调色板模式）
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
            # 创建白色背景，合并透明度
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 按比例缩放
        w, h = img.size
        if w > THUMB_MAX_WIDTH:
            ratio = THUMB_MAX_WIDTH / w
            new_w = THUMB_MAX_WIDTH
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        # 保存为 JPEG（统一格式，压缩率高）
        save_ext = '.jpg'
        thumb_name = f"{THUMB_PREFIX}{name}{save_ext}"
        thumb_path = os.path.join(upload_dir, thumb_name)

        img.save(thumb_path, 'JPEG', quality=THUMB_QUALITY, optimize=True)

        return thumb_name
    except Exception as e:
        print(f"[upload] 生成缩略图失败 ({filename}): {e}")
        return None


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传文件（需登录）"""
    contents = await file.read()

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    filename = _resolve_filename(settings.UPLOAD_DIR, file.filename)
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    url = f"{settings.BASE_URL}/uploads/{filename}"

    # 生成缩略图
    thumb_name = _create_thumbnail(settings.UPLOAD_DIR, filename)
    thumb_url = f"{settings.BASE_URL}/uploads/{thumb_name}" if thumb_name else url

    return {
        "filename": filename,
        "url": url,
        "thumb_url": thumb_url,
        "size": len(contents),
    }
