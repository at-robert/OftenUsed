import re
import requests
import os

def extract_file_id(url: str) -> str | None:
    """
    從 Google Drive 連結中擷取出檔案 ID
    範例：https://drive.google.com/file/d/<ID>/view
    """
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def check_gdrive_file(file_id: str) -> bool:
    """
    檢查 Google Drive 檔案是否可下載
    回傳 True = 可下載, False = 無法下載
    """
    session = requests.Session()
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        response = session.get(url, allow_redirects=True, timeout=10)
    except requests.RequestException:
        return False

    # 不同狀況判斷
    if response.status_code != 200:
        return False

    text = response.text
    headers = response.headers

    # 常見封鎖訊息
    if "Too many users have viewed" in text:
        return False
    if "Sign in" in text or "login" in text:
        return False
    if "Sorry, you can't view or download this file" in text:
        return False

    # 若是 HTML 頁面可能無法直接下載
    if "text/html" in headers.get("Content-Type", ""):
        # 但若包含 confirm token，代表仍可透過 API 下載
        if re.search(r"confirm=[0-9A-Za-z_-]+", text):
            return True
        else:
            return False

    # 若是檔案類型 (含 content-disposition) → 可下載
    if "content-disposition" in headers:
        return True

    return False


def main():
    pwd = os.path.expanduser('~') + '/'
    input_file = pwd + "/Downloads/gd_list.txt"
    downloadable_files = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for url in lines:
        file_id = extract_file_id(url)
        if not file_id:
            print(f"[SKIP] 無法解析 ID：{url}")
            continue

        ok = check_gdrive_file(file_id)
        if ok:
            downloadable_files.append(url)
            print(f"[OK] 可下載：{url}")
        else:
            print(f"[NO] 無法下載：{url}")

    # 輸出結果總結
    print("\n===== 可下載檔案列表 =====")
    if downloadable_files:
        for u in downloadable_files:
            print(u)
    else:
        print("（沒有可下載的檔案）")


if __name__ == "__main__":
    main()
