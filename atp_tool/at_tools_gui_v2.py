import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd


def find_sheet_by_keyword(file_path, keyword="Purchase Order Data"):
    """
    在 Excel 每個 sheet 中搜尋是否存在指定字串，並回傳所有符合的 sheet 名稱。
    """
    xl = pd.ExcelFile(file_path)
    matched_sheets = []

    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None, dtype=str)

        # 將所有 cell 壓成一維並檢查是否包含 keyword
        if df.stack().str.contains(keyword, na=False).any():
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
    wanted_cols = ["Sold-to Abbreviation", "Customer Reference","Customer PO Item No", "CRD","Close","ETD"]
    
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


def read_from_EU_OO_v2(file_,sheet_,filter_):
    df_raw = pd.read_excel(file_, sheet_, header=None)
    # 取第 11 列 (index = 10) 作為欄位名稱
    new_header = df_raw.iloc[0]
    
    # 重新設定欄位名稱 + 取 header 下面的資料
    df = df_raw[1:].copy()
    df.columns = new_header
    
    # Step 4: 只留下三個欄位
    wanted_cols = ["Sold-to Abbreviation", "Customer Reference","Customer PO Item No", "CRD","Close","ETD"]
    
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

    df["ETD"] = pd.to_datetime(df["ETD"], format="%m/%d/%Y")
    df["ETD"] = df["ETD"].dt.strftime("%m/%d/%Y")
    
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


def check_columns_equal(df1, df2, col1="PO_NUMBER", col2="Customer Reference"):
    # 檢查長度
    if len(df1[col1]) != len(df2[col2]):
        return {
            "result": False,
            "reason": f"Length not match: df1={len(df1[col1])}, df2={len(df2[col2])}"
        }

    # 使用 pandas Series.equals() → 內容 + 順序 都要一樣
    if df1[col1].reset_index(drop=True).equals(df2[col2].reset_index(drop=True)):
        return {
            "result": True,
            "reason": "Columns match in both content and order."
        }
    else:
        # 找出不一致位置
        mismatches = df1[col1].reset_index(drop=True) != df2[col2].reset_index(drop=True)
        mismatch_indices = mismatches[mismatches].index.tolist()
        return {
            "result": False,
            "reason": f"Found {len(mismatch_indices)} mismatches.",
            "indices": mismatch_indices,
            "df1_values": df1[col1].iloc[mismatch_indices].tolist(),
            "df2_values": df2[col2].iloc[mismatch_indices].tolist(),
        }

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ATP EU OO Tools")
        self.root.geometry("1850x880")     # 稍微加高以容納新按鍵

        # 字型設定
        self.font_large = ("Arial", 14)
        self.font_button = ("Arial", 14, "bold")

        self.build_ui()

    # -------------------------------
    # GUI Layout
    # -------------------------------
    def build_ui(self):

        # ---- df1 ----
        tk.Label(self.root, text="Client給的檔案：", font=self.font_large)\
            .grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.df1_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.df1_path, width=50, font=self.font_large)\
            .grid(row=0, column=1, padx=10)

        tk.Button(self.root, text="檔案", font=self.font_button, width=4,
                  command=self.choose_df1)\
            .grid(row=0, column=2, padx=10)

        # ---- df2 ----
        tk.Label(self.root, text="EU OO檔案：", font=self.font_large)\
            .grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.df2_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.df2_path, width=50, font=self.font_large)\
            .grid(row=1, column=1, padx=10)

        tk.Button(self.root, text="檔案", font=self.font_button, width=4,
                  command=self.choose_df2)\
            .grid(row=1, column=2, padx=10)

        # ---- Start Processing Button ----
        tk.Button(self.root, text="算出上個星期二", font=self.font_button,
                  width=15, height=2, bg="#4CAF50", fg="blue",
                  command=self.run_process)\
            .grid(row=2, column=0, columnspan=3, pady=10)

        # ---- ⭐ 新增一顆按鍵在下面 ⭐ ----
        tk.Button(self.root, text="算出ETD回給Client", font=self.font_button,
                  width=15, height=2, bg="#2196F3", fg="blue",
                  command=self.additional_action)\
            .grid(row=3, column=0, columnspan=3, pady=10)

        # ============================================================
        # ⭐⭐⭐ 右側區塊：Message(left) + TreeView(right) ⭐⭐⭐
        # ============================================================
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=3, rowspan=50, sticky="nsew", padx=10)

        # 右側區塊使用 2 欄：左 message / 右 table
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)
        right_frame.rowconfigure(1, weight=1)

        # ---- 左側 Message Label ----
        tk.Label(right_frame, text="訊息/結果：", font=self.font_large)\
            .grid(row=0, column=0, sticky="nw")

        # ---- 右側 Table Label ----
        tk.Label(right_frame, text="原本的Client 表格：", font=self.font_large)\
            .grid(row=0, column=1, sticky="nw")

        # ---- 左側：Message 區 ----
        self.msg = tk.Text(right_frame, width=60, height=45, font=("Consolas", 12))
        self.msg.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        # ---- 右側：TreeView 區 ----
        table_frame = tk.Frame(right_frame)
        table_frame.grid(row=1, column=1, sticky="nsew")

        # Treeview 字型調小
        style = ttk.Style()
        self.tree_font = ("Consolas", 12)
        style.configure("Treeview", font=self.tree_font, rowheight=18)

        # 可顯示約 50 rows
        self.table = ttk.Treeview(table_frame, show="headings", height=45)
        self.table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.bind("<Control-c>", self.copy_treeview_selection)



    # -------------------------------
    # File Choosers
    # -------------------------------
    def choose_df1(self):
        filename = filedialog.askopenfilename(
            title="選擇 Client給的檔案",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if filename:
            self.df1_path.set(filename)

            sheet_name = find_sheet_by_keyword(filename)
            df = read_from_client(filename,sheet_name[0])
            if len(df) > 0:
                self.show_dataframe(df[['PO_NUMBER', "PO_LINE",'LAST_TUESDAY']])
                self.auto_adjust_treeview_column_width(max_width_limit=150)

    def choose_df2(self):
        filename = filedialog.askopenfilename(
            title="選擇 EU OO檔案",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if filename:
            self.df2_path.set(filename)

   # -------------------------------
    # Show dataframe
    # -------------------------------
    def show_dataframe(self, df):
        # 清空原表格欄位與資料
        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(df.columns)

        # 設定欄位
        for col in df.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor="center")

        # 插入 DataFrame 每一列
        for _, row in df.iterrows():
            self.table.insert("", tk.END, values=list(row))


    # -------------------------------
    # Tree View Auto adjustment
    # -------------------------------
    def auto_adjust_treeview_column_width(self, max_width_limit=180):
        """
        自動調整 TreeView 欄寬，但設定最大寬度，避免欄位太大。
        max_width_limit：每欄最大寬度（像素）
        """
        for col in self.table["columns"]:
            # 依 column title 設初始寬度
            max_width = len(col) * 10

            col_index = self.table["columns"].index(col)

            # 檢查每筆資料，取最長字串
            for item in self.table.get_children():
                value = str(self.table.item(item, "values")[col_index])
                width = len(value) * 7   # 字體小時 7px 比較準確
                if width > max_width:
                    max_width = width

            # ⭐ 限制最大寬度（避免欄位太寬）
            if max_width > max_width_limit:
                max_width = max_width_limit

            # ⭐ 也避免太窄（保留基本可視寬度）
            if max_width < 60:
                max_width = 60

            self.table.column(col, width=max_width,stretch=False)

    # -------------------------------
    # Tree View Copy to clipboard
    # -------------------------------
    def copy_treeview_selection(self, event=None):
        """
        將 TreeView 選取行複製到剪貼簿（Tab 分隔，可貼 Excel）
        """
        selected = self.table.selection()
        if not selected:
            return

        rows_text = []

        # 取得欄位名稱
        columns = self.table["columns"]

        # 每行轉成 tab 分隔文字
        for item in selected:
            values = self.table.item(item, "values")
            rows_text.append("\t".join(str(v) for v in values))

        # 最後組成多行
        final_text = "\n".join(rows_text)

        # 加入剪貼簿
        self.root.clipboard_clear()
        self.root.clipboard_append(final_text)
        self.root.update()

        return "break"


    # -------------------------------
    # Main Processing
    # -------------------------------
    def run_process(self):
        self.msg.delete("1.0", tk.END)

        if not self.df1_path.get() or not self.df2_path.get():
            self.msg.insert(tk.END, "請先選擇檔案們\n")
            return

        self.msg.insert(tk.END, "算出上個星期二 Client->EU OO\n")

        # Client Order 
        file_path = self.df1_path.get()
        sheet_name = find_sheet_by_keyword(file_path)
        df1 = read_from_client(file_path,sheet_name[0])

        # EU Open Order
        file_path = self.df2_path.get()
        sheet_name = "Marco & Mathias (Mandy)"
        df2 = read_from_EU_OO(file_path,sheet_name,'FLEX NL')

        # ====== 這裡放你要的處理邏輯 ======
        # 目前示範：只印 df1 的前 50 rows
        # 未來你把你的 df 新排列邏輯貼上即可
        df_new = reorder_by_reference_multi(
        df_main=df1,
        keys_main=["PO_NUMBER", "PO_LINE"],
        df_ref=df2,
        keys_ref=["Customer Reference", "Customer PO Item No"],
        drop_missing=True
)

        ret = check_columns_equal(df_new,df2)

        if ret['result'] == False:
            self.msg.insert(tk.END,str(ret))
        else:
            self.msg.insert(tk.END, " Number of Rows = {} \n".format(len(df_new)))
            self.msg.insert(tk.END, df_new['LAST_TUESDAY'].to_string(index=False))

            df_new.to_csv("df_last_tues.csv", index=False, encoding="utf-8-sig")

    # -------------------------------
    # ⭐ 新增按鍵對應的 function ⭐
    # -------------------------------
    def additional_action(self):
        self.msg.delete("1.0", tk.END)

        if not self.df1_path.get() or not self.df2_path.get():
            self.msg.insert(tk.END, "請先選擇檔案們\n")
            return
    
        # self.msg.insert(tk.END, "\n--- 下一步動作按下 ---\n")
        self.msg.insert(tk.END, "算出Client的ETD\n")


        # Client Order 
        file_path = self.df1_path.get()
        sheet_name = find_sheet_by_keyword(file_path)
        df1 = read_from_client(file_path,sheet_name[0])

        # EU Open Order
        file_path = self.df2_path.get()
        sheet_name = "Marco & Mathias (Mandy)"
        df2 = read_from_EU_OO_v2(file_path,sheet_name,'FLEX NL')


        df_new = reorder_by_reference_multi(
        df_main=df2,
        keys_main=["Customer Reference", "Customer PO Item No"],
        df_ref=df1,
        keys_ref=["PO_NUMBER", "PO_LINE"],
        drop_missing=True
)

        ret = check_columns_equal(df_new,df1,col1="Customer Reference",col2="PO_NUMBER")

        if ret['result'] == False:
            self.msg.insert(tk.END,str(ret))
        else:
            self.msg.insert(tk.END, " Number of Rows = {} \n".format(len(df_new)))
            self.msg.insert(tk.END, df_new['ETD'].to_string(index=False))

            df_new.to_csv("df_etd.csv", index=False, encoding="utf-8-sig")


# -------------------------------
# 啟動 App
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
