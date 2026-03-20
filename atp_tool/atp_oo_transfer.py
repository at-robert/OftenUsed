import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import datetime
import os

class ExcelProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Data Integrator - Mandy Version")
        self.root.geometry("1400x800")
        
        # --- 1. 變數設定 ---
        self.file_path = ""
        self.all_sheets = []
        self.sheet_checkboxes = {} 
        self.final_mandy_df = pd.DataFrame() # 儲存最後生成的完整資料
        
        self.column_names_list = [
            'Order Date', 'Sold-to Party', 'Ship-to Party', 'SAP SO#', 'SO Item',
            'Customer PO#', 'line no.', 'Part Number', 'Customer Part Number',
            'Qty Ordered', 'Unit Price', 'Required. Date', 'shipping schedule',
            'Remark', 'Tracking no.', '(訂單變更) 新增項次', '來源項次',
            'End Customer PN', 'BU', 'Interface', 'Flash / DRAM', 'ETD reason', 'ETD History'
        ]
        
        self.mandy_columns_list = [
            'Upload', 'Close', 'SO Type', 'Source SO No', 'Source SO Item No', 'Sales Document',
            'Sales Document Item', 'Sold-to Abbreviation', 'Ship-to Abbreviation', 'Customer Reference Date',
            'Sold-to Party', 'Ship-to Party', 'Customer Reference', 'Customer PO Item No', 'Material',
            'Module Material', 'Customer Material', 'Order Quantity', 'Unit Price', 'CRD', 'ETD', 'ETA',
            'Is Sample (Y)', 'Remark', 'Amount', 'Purchase Order Type', 'Sample/Loan SFID', 'Is Gift Item (ZFTO)',
            'FOC Invoice Price', 'Masking Price', 'Masking Price Currency', 'End Customer PO#', 'End Customer PN',
            'Incoterm (Header)', 'Inco.Location (Header)', 'Incoterm (Item)', 'Inco.Location (Item)',
            'Special Procurement Application No', 'Titop DN', 'Tiptop DN Item', 'Unit Price Currency',
            'Original Unit Price', 'BU', 'Interface', 'Flash / DRAM', 'ETD Reason', 'Allocation Date',
            'ETD History', '訂單變更類型', '拆項來源項次 / 取消原因', '(ZDR) \nItem Description'
        ]

        self.tree_view_cols = [
            'Customer Reference Date', 'Sold-to Party', 'Ship-to Party', 'Sales Document',
            'Sales Document Item', 'Customer Reference', 'Customer PO Item No', 'Material',
            'Customer Material', 'Order Quantity', 'Unit Price', 'CRD', 'ETD', 'Remark',
            'BU', 'Interface', 'Flash / DRAM', 'ETD Reason', 'ETD History'
        ]

        self.setup_ui()

    def setup_ui(self):
        main_paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # --- 左半邊：控制台 ---
        left_frame = ttk.Frame(main_paned, padding=15)
        main_paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Step 1: Select Input File", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Button(left_frame, text="📁 Open Excel File", command=self.open_file).pack(fill=tk.X, pady=5)
        self.path_label = ttk.Label(left_frame, text="No file selected", wraplength=350, foreground="gray")
        self.path_label.pack(pady=5, anchor=tk.W)

        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(left_frame, text="Step 2: Filter & Select Sheets", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_sheets)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_tool_frame = ttk.Frame(left_frame)
        btn_tool_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_tool_frame, text="Select Visible", command=self.select_all_visible).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(btn_tool_frame, text="Clear Visible", command=self.clear_all_visible).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        list_container = ttk.Frame(left_frame, relief="sunken", borderwidth=1)
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(list_container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(left_frame, text="🚀 APPLY & EXPORT", command=self.process_data).pack(fill=tk.X, ipady=10, pady=10)

        # --- 右半邊：資料預覽 ---
        right_frame = ttk.Frame(main_paned, padding=15)
        main_paned.add(right_frame, weight=3)

        self.info_label = ttk.Label(right_frame, text="Rows: 0 | Displaying 19 Core Columns", font=('Arial', 11, 'bold'), foreground="#2c3e50")
        self.info_label.pack(anchor=tk.W, pady=(0, 10))

        # Treeview 與 滾動條佈局
        self.tree_container = ttk.Frame(right_frame)
        self.tree_container.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_container, show="headings", selectmode="extended")
        
        # 垂直滾動條
        self.tree_scroll_y = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll_y.set)
        
        # 水平滾動條
        self.tree_scroll_x = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.tree_scroll_x.set)

        # 佈局配置
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree_scroll_y.grid(row=0, column=1, sticky='ns')
        self.tree_scroll_x.grid(row=1, column=0, sticky='ew')
        
        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(0, weight=1)

        # --- 綁定右鍵選單 (複製功能) ---
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy Cell Value", command=self.copy_cell)
        self.context_menu.add_command(label="Copy Entire Row", command=self.copy_row)
        self.tree.bind("<Button-3>", self.show_context_menu) # Windows/Linux 右鍵
        self.tree.bind("<Button-2>", self.show_context_menu) # macOS 右鍵

    # --- 功能邏輯 ---
    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file:
            self.file_path = file
            self.path_label.config(text=file, foreground="blue")
            xl = pd.ExcelFile(file)
            self.all_sheets = xl.sheet_names
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            self.sheet_checkboxes = {}
            self.update_sheet_list(self.all_sheets)

    def update_sheet_list(self, sheets_to_display):
        for name, (var, chk) in self.sheet_checkboxes.items():
            chk.pack_forget()
        for sheet in sheets_to_display:
            if sheet not in self.sheet_checkboxes:
                var = tk.BooleanVar(value=False)
                chk = ttk.Checkbutton(self.scroll_frame, text=sheet, variable=var)
                self.sheet_checkboxes[sheet] = (var, chk)
            self.sheet_checkboxes[sheet][1].pack(anchor=tk.W, pady=1)

    def filter_sheets(self, *args):
        search_term = self.search_var.get().lower()
        filtered = [s for s in self.all_sheets if search_term in s.lower()]
        self.update_sheet_list(filtered)

    def select_all_visible(self):
        search_term = self.search_var.get().lower()
        for name, (var, chk) in self.sheet_checkboxes.items():
            if search_term in name.lower():
                var.set(True)

    def clear_all_visible(self):
        search_term = self.search_var.get().lower()
        for name, (var, chk) in self.sheet_checkboxes.items():
            if search_term in name.lower():
                var.set(False)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.clicked_row = item
            self.clicked_col = self.tree.identify_column(event.x)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_cell(self):
        column_index = int(self.clicked_col.replace('#', '')) - 1
        item_values = self.tree.item(self.clicked_row, 'values')
        cell_value = item_values[column_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(cell_value)

    def copy_row(self):
        item_values = self.tree.item(self.clicked_row, 'values')
        row_text = "\t".join(map(str, item_values))
        self.root.clipboard_clear()
        self.root.clipboard_append(row_text)

    def smart_date_format(self, x):
        if pd.isna(x) or str(x).strip().lower() in ['nan', 'none', '']:
            return ''
        try:
            dt = pd.to_datetime(x)
            return dt.strftime('%Y/%m/%d')
        except:
            return str(x).strip()

    def process_data(self):
        selected_sheets = [name for name, (var, chk) in self.sheet_checkboxes.items() if var.get()]
        if not selected_sheets:
            messagebox.showwarning("Warning", "Please select at least one sheet!")
            return

        try:
            dict_df = pd.read_excel(self.file_path, sheet_name=selected_sheets, dtype=str)
            wb = openpyxl.load_workbook(self.file_path, read_only=False, data_only=True)
            for sheet_name in selected_sheets:
                ws = wb[sheet_name]
                df = dict_df[sheet_name]
                keep_indices = []
                for i in range(len(df)):
                    excel_row_num = i + 2
                    is_hidden = False
                    if excel_row_num in ws.row_dimensions:
                        if ws.row_dimensions[excel_row_num].hidden:
                            is_hidden = True
                    if not is_hidden:
                        keep_indices.append(i)
                dict_df[sheet_name] = df.iloc[keep_indices].copy()
            wb.close()

            for name in selected_sheets:
                df = dict_df[name]
                if 'line no.' in df.columns:
                    mask = df['line no.'].isnull() | (df['line no.'].str.strip() == "")
                    if mask.any():
                        first_blank_index = mask.idxmax()
                        dict_df[name] = df.iloc[:df.index.get_loc(first_blank_index)]

            processed_dfs = []
            for sheet_name in selected_sheets:
                aligned_df = dict_df[sheet_name].reindex(columns=self.column_names_list)
                aligned_df['Source Sheet'] = sheet_name
                processed_dfs.append(aligned_df)
            final_df = pd.concat(processed_dfs, ignore_index=True)

            mapping_dict = {
                'Order Date': 'Customer Reference Date', 'Sold-to Party': 'Sold-to Party',
                'Ship-to Party': 'Ship-to Party', 'SAP SO#': 'Sales Document',
                'SO Item': 'Sales Document Item', 'Customer PO#': 'Customer Reference',
                'line no.': 'Customer PO Item No', 'Part Number': 'Material',
                'Customer Part Number': 'Customer Material', 'Qty Ordered': 'Order Quantity',
                'Unit Price': 'Unit Price', 'Required. Date': 'CRD',
                'shipping schedule': 'ETD', 'Remark': 'Remark', 'BU': 'BU',
                'Interface': 'Interface', 'Flash / DRAM': 'Flash / DRAM',
                'ETD reason': 'ETD Reason', 'ETD History': 'ETD History'
            }

            self.final_mandy_df = final_df[list(mapping_dict.keys())].copy()
            self.final_mandy_df = self.final_mandy_df.rename(columns=mapping_dict)
            self.final_mandy_df = self.final_mandy_df.reindex(columns=self.mandy_columns_list)

            date_cols = ['Customer Reference Date', 'ETD', 'CRD']
            for col in date_cols:
                if col in self.final_mandy_df.columns:
                    self.final_mandy_df[col] = self.final_mandy_df[col].apply(self.smart_date_format)

            other_cols = [c for c in self.final_mandy_df.columns if c not in date_cols]
            self.final_mandy_df[other_cols] = self.final_mandy_df[other_cols].astype(str).replace(['nan', 'None'], '')

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"mandy_output_{timestamp}.xlsx"
            self.final_mandy_df.to_excel(output_name, index=False)

            self.display_in_tree(self.final_mandy_df)
            messagebox.showinfo("Success", f"Process complete!\nTotal Rows: {len(self.final_mandy_df)}\nSaved as: {output_name}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_in_tree(self, full_df):
        display_df = full_df[self.tree_view_cols].copy()
        self.tree["columns"] = list(display_df.columns)
        for col in display_df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, minwidth=100, anchor=tk.W) # 設定欄位寬度以啟動水平滾動
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data_rows = display_df.values.tolist()
        for row in data_rows: # 載入所有資料以便滾動觀看
            self.tree.insert("", tk.END, values=row)

        self.info_label.config(text=f"Previewing 19 Core Columns | Total Rows: {len(full_df)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelProcessorApp(root)
    root.mainloop()