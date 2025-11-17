import pandas as pd

def find_sheet_by_keyword(file_path, keyword="Purchase Order Data"):
    """
    在 Excel 每個 sheet 中搜尋是否存在指定字串，並回傳所有符合的 sheet 名稱。
    """
    xl = pd.ExcelFile(file_path)  # 先讀取 workbook
    matched_sheets = []

    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None, dtype=str)

        # 檢查整個 sheet 是否有 keyword
        if df.applymap(lambda x: keyword in x if isinstance(x, str) else False).any().any():
            matched_sheets.append(sheet)

    return matched_sheets


def read_from_client(file_, sheet_):
    # 先讀整個 sheet（不含 header）
    df_raw = pd.read_excel(file_, sheet_, header=None)
    
    # 取第 11 列 (index = 10) 作為欄位名稱
    new_header = df_raw.iloc[12]
    
    # 重新設定欄位名稱 + 取 header 下面的資料
    df = df_raw[13:].copy()
    df.columns = new_header
    
    # Step 4: 只留下三個欄位
    wanted_cols = ["PO_NUMBER","PO_LINE","NEW_REQUEST_DATE", "SUPPLIER_CONFIRM_DATE"]
    
    # 若欄名有前後空白或大小寫不同，可用這種方式比對
    df.columns = df.columns.str.strip()
    
    df = df[wanted_cols]
    
    # Step 5: index 重新編號
    df = df.reset_index(drop=True)


    # 先把字串轉成 datetime
    df["NEW_REQUEST_DATE"] = pd.to_datetime(df["NEW_REQUEST_DATE"], format="%m/%d/%Y")
    
    # 計算上一個星期二 (weekday: Tuesday = 1)
    # dt.weekday：Monday=0, Tuesday=1, ... Sunday=6
    df["LAST_TUESDAY"] = df["NEW_REQUEST_DATE"] - pd.to_timedelta(
        (df["NEW_REQUEST_DATE"].dt.weekday - 1) % 7,
        unit="D"
    )
    
    # 格式化成 yyyy-mm-dd
    df["LAST_TUESDAY"] = df["LAST_TUESDAY"].dt.strftime("%Y/%m/%d")

    df["PO_LINE"] = pd.to_numeric(df["PO_LINE"], errors="coerce")
    df["PO_LINE"] = df["PO_LINE"].fillna(0)
    
    return df

def read_from_EU_OO(file_,sheet_,filter_):
    df_raw = pd.read_excel(file_, sheet_, header=None)
    # 取第 11 列 (index = 10) 作為欄位名稱
    new_header = df_raw.iloc[0]
    
    # 重新設定欄位名稱 + 取 header 下面的資料
    df = df_raw[1:].copy()
    df.columns = new_header
    
    # Step 4: 只留下三個欄位
    wanted_cols = ["Sold-to Abbreviation", "Customer Reference","Customer PO Item No", "CRD","Close"]
    
    # 若欄名有前後空白或大小寫不同，可用這種方式比對
    df.columns = df.columns.str.strip()
    
    df = df[wanted_cols]
    
    # Step 5: index 重新編號
    df = df.reset_index(drop=True)

    # df = df[df['Sold-to Abbreviation'] == filter_]

    df_filtered = df[
    (df["Sold-to Abbreviation"] == filter_) &
    (df["Close"].fillna("") == "")
]
    df = df_filtered

    df["Customer PO Item No"] = pd.to_numeric(df["Customer PO Item No"], errors="coerce")
    df["Customer PO Item No"] = df["Customer PO Item No"].fillna(0)
    
    return df


def reorder_by_reference_multi(df_main, keys_main, df_ref, keys_ref, drop_missing=True):
    """
    根據 df_ref 的 keys_ref 的順序，重新排列 df_main 的 keys_main 的順序。
    支援 df_main 重複 key。

    參數:
        df_main     : 要被排序的 DataFrame
        keys_main   : df_main 的欄位清單，例如 ["PO_NUMBER", "PO_LINE"]
        df_ref      : 提供排序的 DataFrame
        keys_ref    : df_ref 對應欄位清單，例如 ["Customer Reference", "Customer PO Item No"]
        drop_missing: 是否丟掉 df_main 中沒有對應 df_ref 的資料

    回傳:
        排序後的新 DataFrame
    """
    # Step 1: 建立排序用的 sort_order
    df_ref_sorted = df_ref[keys_ref].drop_duplicates().copy()
    df_ref_sorted["sort_order"] = range(len(df_ref_sorted))

    # Step 2: merge df_main 與 df_ref_sorted
    df_merged = df_main.merge(
        df_ref_sorted,
        left_on=keys_main,
        right_on=keys_ref,
        how="left"
    )

    # Step 3: drop 沒有對應的資料
    if drop_missing:
        df_merged = df_merged.dropna(subset=["sort_order"])

    # Step 4: 依 sort_order 排序
    df_merged = df_merged.sort_values("sort_order").reset_index(drop=True)

    # Step 5: 移除輔助欄位
    df_merged = df_merged.drop(columns=keys_ref + ["sort_order"], errors='ignore')

    return df_merged


#------------------------------------------
# 主程式
#------------------------------------------
if __name__ == "__main__":
    # Client Order 
    file_path = "0000000205POCONF20251114060058.xlsx"
    sheet_name = find_sheet_by_keyword(file_path)
    df1 = read_from_client(file_path,sheet_name[0])

    # EU Open Order
    file_path = "ATP-EU OPEN ORDER  testing.xlsx"
    sheet_name = "Marco & Mathias (Mandy)"
    df2 = read_from_EU_OO(file_path,sheet_name,'FLEX NL')

    df_new = reorder_by_reference_multi(
    df_main=df1,
    keys_main=["PO_NUMBER", "PO_LINE"],
    df_ref=df2,
    keys_ref=["Customer Reference", "Customer PO Item No"],
    drop_missing=True
)
    print(" Number of rows = {}".format(len(df_new)))
    print(df_new)   
    df_new.to_csv("df_new.csv", index=False, encoding="utf-8-sig")