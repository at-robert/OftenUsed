import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import GSpreadException
from collections import Counter

# 設定與授權
pwd = os.path.expanduser('~') + '/'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    pwd + 'Documents/Gdrive_credential/client_secret.json', scope)
client = gspread.authorize(creds)

google_sheet_name = "2025 FW_HR_List"
spreadsheet = client.open(google_sheet_name)
worksheets = spreadsheet.worksheets()

output_path = pwd + "Downloads/2025 FW_HR_List.xlsx"
skipped_sheets = []

def clean_headers(headers):
    """處理重複與空白欄名"""
    cleaned = []
    counter = Counter()
    for h in headers:
        h_clean = h.strip() if h else "     "
        counter[h_clean] += 1
        if counter[h_clean] > 1:
            h_clean = f"{h_clean}_{counter[h_clean]}"
        cleaned.append(h_clean)
    return cleaned

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for ws in worksheets:
        sheet_name = ws.title
        try:
            # 讀取整個表格（含欄位名）
            values = ws.get_all_values()
            if not values or len(values) < 2:
                print(f"⚠️ 分頁「{sheet_name}」無資料或只有標題，跳過")
                skipped_sheets.append(sheet_name)
                continue

            headers = clean_headers(values[0])
            rows = values[1:]
            df = pd.DataFrame(rows, columns=headers)

            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

        except Exception as e:
            print(f"❌ 無法處理分頁：{sheet_name}，錯誤：{e}")
            skipped_sheets.append(sheet_name)

# 最後回報
if skipped_sheets:
    print(f"\n🚫 以下分頁未能成功匯出：{skipped_sheets}")
else:
    print(f"\n✅ 所有分頁皆成功匯出到：{output_path}")
