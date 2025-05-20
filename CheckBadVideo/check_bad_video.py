import os
import mimetypes
import subprocess
from pathlib import Path
import stat

# 支援的影片格式副檔名
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"}

# 指定要掃描的資料夾
SCAN_DIR = "/Volumes/T7/v"  # ← 請替換成你自己的資料夾路徑

def get_mime_type(path: Path) -> str:
    """使用 file 命令獲取真實 MIME 類型描述"""
    try:
        output = subprocess.check_output(["file", "-b", str(path)])
        return output.decode().strip()
    except Exception as e:
        return f"無法判斷 ({e})"

def remove_exec_permission(path: Path):
    """如果檔案具有執行權限，則自動移除"""
    if os.access(path, os.X_OK):
        print(f"⚠️  {path.name} 具有執行權限，正在移除...")
        current_mode = os.stat(path).st_mode
        new_mode = current_mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH
        os.chmod(path, new_mode)
        print(f"✅ 已移除執行權限：{path.name}")
    else:
        print(f"✅ {path.name} 無執行權限")

def is_video_file(path: Path) -> bool:
    """初步檢查副檔名是否為影片"""
    return path.suffix.lower() in VIDEO_EXTENSIONS

def check_file(path: Path):
    

    # 1. 檢查並移除執行權限
    # remove_exec_permission(path)

    # 2. 使用 file 判斷 MIME 類型
    mime_info = get_mime_type(path)
   

    # 3. 判斷是否為預期的影片類型
    if "video" in mime_info.lower() or "media" in mime_info.lower():
        # print("✅ 判斷為影片檔")
        i = 1
    else:
        print(f"\n🔍 檢查檔案: {path.name}")
        print(f"📄 檔案 MIME 類型：{mime_info}")
        print("⚠️  非典型影片檔，請進一步檢查")

def scan_directory(dir_path):
    print(f"\n📂 開始掃描資料夾: {dir_path}")
    for entry in Path(dir_path).iterdir():
        if entry.is_file() and is_video_file(entry):
            check_file(entry)

if __name__ == "__main__":
    scan_directory(SCAN_DIR)
