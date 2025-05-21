import os
import mimetypes
import subprocess
import argparse
import csv
import json
from pathlib import Path
import stat

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm"}


def get_mime_type(path: Path) -> str:
    try:
        output = subprocess.check_output(["file", "-b", str(path)])
        return output.decode().strip()
    except Exception as e:
        return f"Error: {e}"


def remove_exec_permission(path: Path):
    if os.access(path, os.X_OK):
        current_mode = os.stat(path).st_mode
        new_mode = current_mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH
        os.chmod(path, new_mode)
        return True
    return False


def is_video_file(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS


def check_file(path: Path) -> dict:
    abs_path = str(path.resolve())
    had_exec = remove_exec_permission(path)
    mime_info = get_mime_type(path)
    suspicious = not ("video" in mime_info.lower() or "media" in mime_info.lower())

    return {
        "file": abs_path,
        "exec_permission_removed": had_exec,
        "mime_type": mime_info,
        "suspicious": suspicious
    }


def scan_directory(dir_path: Path) -> list:
    results = []
    for file_path in dir_path.rglob("*"):
        if file_path.is_file() and is_video_file(file_path):
            result = check_file(file_path)
            results.append(result)
    return results


def export_report(results, filepath, fmt):
    if fmt == "csv":
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    elif fmt == "json":
        with open(filepath, "w") as jsonfile:
            json.dump(results, jsonfile, indent=2)


def main():
    parser = argparse.ArgumentParser(description="影片安全掃描工具")
    parser.add_argument("--path", type=str, default="/Volumes/T7/v", help="要掃描的資料夾路徑")
    parser.add_argument("--report", type=str, default="result.csv", help="輸出報告檔案 (可選)")
    parser.add_argument("--format", type=str, choices=["csv", "json"], default="csv", help="報告格式")
    args = parser.parse_args()

    target_dir = Path(args.path)
    if not target_dir.is_dir():
        print(f"❌ 資料夾不存在: {target_dir}")
        return

    print(f"🔍 開始掃描：{target_dir.resolve()}")
    results = scan_directory(target_dir)

    print(f"✅ 掃描完成，共發現 {len(results)} 個影片檔案")
    for r in results:
        status = "⚠️" if r["suspicious"] else "✅"
        print(f"{status} {r['file']} ({r['mime_type']})")

    if args.report:
        export_report(results, args.report, args.format)
        print(f"📝 已匯出報告：{args.report}")


if __name__ == "__main__":
    main()
