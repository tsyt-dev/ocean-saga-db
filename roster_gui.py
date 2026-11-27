"""
Ocean Saga — SS Character Roster Manager (GUI)
โปรแกรมจัดการตัวละครระดับ SS สำหรับเกม Ocean Saga
อัปเดตข้อมูลลง Ocean_Saga_AI_Context_Export.json และ Ocean_Saga_AI_Context_Export.md ทันที
"""

import os
import sys
import json
import re
import shutil
import datetime
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "characters_th.json")
EXPORT_JSON_PATH = os.path.join(BASE_DIR, "Ocean_Saga_AI_Context_Export.json")
EXPORT_MD_PATH = os.path.join(BASE_DIR, "Ocean_Saga_AI_Context_Export.md")

TIER_ORDER = ["T0", "SSS", "S", "A", "B", "D", "Other"]
TIER_COLORS = {
    "T0": "#e11d48",   # Rose Red / Pink
    "SSS": "#f97316",  # Vibrant Orange
    "S": "#eab308",    # Golden Yellow
    "A": "#3b82f6",    # Blue
    "B": "#06b6d4",    # Cyan / Teal
    "D": "#64748b",    # Slate Gray
    "Other": "#94a3b8" # Light Slate
}

THAI_MONTHS = [
    "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]

def format_thai_date(dt: datetime.datetime) -> str:
    month_name = THAI_MONTHS[dt.month]
    return f"{dt.day} {month_name} {dt.year}"

class AutocompleteCombobox(ttk.Combobox):
    """Combobox with real-time text matching & auto-filter."""
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self._hit_index += delta
        if self._hit_index < 0:
            self._hit_index = len(self._hits) - 1
        elif self._hit_index >= len(self._hits):
            self._hit_index = 0
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Return', 'Tab'):
            return
        _words = [w for w in self._completion_list if self.get().lower() in w.lower()]
        self['values'] = _words
        if _words:
            self.event_generate('<Down>')


class CharacterDialog(tk.Toplevel):
    def __init__(self, parent, ss_db, real_tier_map, existing_data=None):
        super().__init__(parent)
        self.ss_db = ss_db
        self.real_tier_map = real_tier_map
        self.existing_data = existing_data
        self.result = None

        self.title("เพิ่ม / แก้ไขตัวละครระดับ SS" if not existing_data else f"แก้ไข: {existing_data.get('name')}")
        self.geometry("520x420")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Character Selection
        ttk.Label(main_frame, text="เลือกตัวละครระดับ SS (122 ตัว):", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 4))
        
        # Prepare list with tier info
        self.char_names = sorted(list(self.ss_db.keys()))
        self.combo_var = tk.StringVar()
        
        self.char_combo = AutocompleteCombobox(main_frame, textvariable=self.combo_var, font=("Segoe UI", 10))
        self.char_combo.set_completion_list(self.char_names)
        self.char_combo.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        self.char_combo.bind("<<ComboboxSelected>>", self.on_char_selected)
        self.char_combo.bind("<FocusOut>", self.on_char_selected)

        # Character Info Badge
        self.info_frame = ttk.LabelFrame(main_frame, text="ข้อมูลตัวละคร", padding=10)
        self.info_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        
        self.info_tier_label = ttk.Label(self.info_frame, text="Tier: -", font=("Segoe UI", 9, "bold"))
        self.info_tier_label.pack(anchor=tk.W)
        self.info_role_label = ttk.Label(self.info_frame, text="ธาตุ / สาย: -", font=("Segoe UI", 9))
        self.info_role_label.pack(anchor=tk.W)

        # 2. Stars
        ttk.Label(main_frame, text="ระดับดาว (Stars):", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky=tk.W, pady=6)
        self.stars_var = tk.IntVar(value=5)
        self.stars_spin = ttk.Spinbox(main_frame, from_=5, to=15, textvariable=self.stars_var, width=10, font=("Segoe UI", 10))
        self.stars_spin.grid(row=3, column=1, sticky=tk.W, pady=6)

        # 3. Main Count
        ttk.Label(main_frame, text="จำนวนตัวหลัก (Main Count):", font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky=tk.W, pady=6)
        self.count_var = tk.IntVar(value=1)
        self.count_spin = ttk.Spinbox(main_frame, from_=1, to=99, textvariable=self.count_var, width=10, font=("Segoe UI", 10))
        self.count_spin.grid(row=4, column=1, sticky=tk.W, pady=6)

        # 4. Extra 5-Star Copies
        ttk.Label(main_frame, text="ตัวซ้ำ 5 ดาว (สำหรับอัปดาวต่อ):", font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky=tk.W, pady=6)
        self.extra_var = tk.IntVar(value=0)
        self.extra_spin = ttk.Spinbox(main_frame, from_=0, to=99, textvariable=self.extra_var, width=10, font=("Segoe UI", 10))
        self.extra_spin.grid(row=5, column=1, sticky=tk.W, pady=6)

        # 5. Note / Comment
        ttk.Label(main_frame, text="หมายเหตุเพิ่มเติม (ถ้ามี):", font=("Segoe UI", 9)).grid(row=6, column=0, sticky=tk.W, pady=6)
        self.note_var = tk.StringVar(value="")
        self.note_entry = ttk.Entry(main_frame, textvariable=self.note_var, font=("Segoe UI", 9))
        self.note_entry.grid(row=6, column=1, sticky=tk.EW, pady=6)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))

        ttk.Button(btn_frame, text="ยกเลิก", command=self.destroy).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(btn_frame, text="ตกลงบันทึก", command=self.save).pack(side=tk.RIGHT)

        main_frame.columnconfigure(1, weight=1)

        # Populate if editing
        if self.existing_data:
            name = self.existing_data.get("name", "")
            self.combo_var.set(name)
            self.char_combo.config(state="disabled") # Don't change name during edit
            self.stars_var.set(self.existing_data.get("stars", 5))
            self.count_var.set(self.existing_data.get("count", 1))
            self.extra_var.set(self.existing_data.get("extra_5star_copies", 0))
            self.note_var.set(self.existing_data.get("note", ""))
            self.on_char_selected()
        else:
            if self.char_names:
                self.combo_var.set(self.char_names[0])
                self.on_char_selected()

    def on_char_selected(self, event=None):
        name = self.combo_var.get().strip()
        char_info = self.ss_db.get(name)
        tier = self.real_tier_map.get(name, "Other")
        
        if char_info:
            elem = char_info.get("element_th") or char_info.get("element_en") or "-"
            role = char_info.get("class_th") or char_info.get("class_en") or char_info.get("role") or "-"
            self.info_tier_label.config(text=f"Tier (เซิร์ฟเวอร์): {tier}", foreground=TIER_COLORS.get(tier, "#000"))
            self.info_role_label.config(text=f"ธาตุ: {elem}  |  สาย/บทบาท: {role}")
        else:
            self.info_tier_label.config(text=f"Tier (เซิร์ฟเวอร์): {tier}", foreground="#666")
            self.info_role_label.config(text="ธาตุ / สาย: ไม่พบในฐานข้อมูล")

    def save(self):
        name = self.combo_var.get().strip()
        if not name:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณาเลือกตัวละคร", parent=self)
            return
        
        if name not in self.ss_db and not self.existing_data:
            # Allow anyway if user confirms
            if not messagebox.askyesno("ยืนยัน", f"ไม่พบตัวละคร '{name}' ในฐานข้อมูลระดับ SS ต้องการเพิ่มหรือไม่?", parent=self):
                return

        tier = self.real_tier_map.get(name, "Other")
        stars = self.stars_var.get()
        count = self.count_var.get()
        extra = self.extra_var.get()
        note = self.note_var.get().strip()

        self.result = {
            "name": name,
            "stars": int(stars),
            "count": int(count),
            "tier": tier
        }
        if extra > 0:
            self.result["extra_5star_copies"] = int(extra)
        if note:
            self.result["note"] = note

        self.destroy()


class OceanSagaRosterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚓ Ocean Saga — โปรแกรมจัดการตัวละครระดับ SS (Roster Manager)")
        self.geometry("1100x720")
        self.minsize(960, 600)

        self.ss_db = {}           # name -> dict
        self.real_tier_map = {}   # name -> tier string (T0, SSS, S, A, B, D)
        self.export_json_data = {}# Full JSON data
        self.roster = []          # List of user owned char dicts
        self.filtered_roster = []

        self.setup_styles()
        self.load_database()
        self.setup_ui()
        self.load_export_data()

        # Keyboard shortcuts
        self.bind("<Control-s>", lambda e: self.save_all())
        self.bind("<Control-n>", lambda e: self.add_character())
        self.bind("<F5>", lambda e: self.reload_all())
        self.bind("<Delete>", lambda e: self.delete_character())

    def setup_styles(self):
        style = ttk.Style(self)
        # Use native 'clam' or 'vista' for modern clean look
        if "vista" in style.theme_names():
            style.theme_use("vista")
        else:
            style.theme_use("clam")

        # Fonts
        self.default_font = ("Segoe UI", 9)
        self.bold_font = ("Segoe UI", 9, "bold")
        self.title_font = ("Segoe UI", 14, "bold")
        self.header_font = ("Segoe UI", 10, "bold")

        style.configure("Treeview", font=self.default_font, rowheight=28)
        style.configure("Treeview.Heading", font=self.header_font, padding=4)
        style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"))
        style.configure("Save.TButton", font=("Segoe UI", 10, "bold"), foreground="#047857")

    def load_database(self):
        """Load characters_th.json and filter only SS rarity."""
        if not os.path.exists(DB_PATH):
            messagebox.showerror("ไม่พบไฟล์", f"ไม่พบไฟล์ฐานข้อมูล:\n{DB_PATH}")
            return

        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                all_chars = json.load(f)
            
            # Filter SS rarity only
            self.ss_db = {c["name"]: c for c in all_chars if c.get("rarity") == "SS"}
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการโหลด {DB_PATH}:\n{e}")

    def setup_ui(self):
        # 1. Top Header Frame (Dark Slate Accent)
        header_frame = tk.Frame(self, bg="#0f172a", height=80, padx=20, pady=12)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame, 
            text="⚓ Ocean Saga — จัดการตัวละครระดับ SS", 
            font=self.title_font, 
            fg="#f8fafc", 
            bg="#0f172a"
        )
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(
            header_frame, 
            text="จัดการ ID ปัจจุบัน (เพิ่ม / แก้ไข / ลบ) เฉพาะระดับ SS และบันทึกอัปเดตไฟล์ Context ทันที", 
            font=("Segoe UI", 9), 
            fg="#94a3b8", 
            bg="#0f172a"
        )
        subtitle_label.pack(anchor=tk.W)

        # Stats Badge on Header Right
        self.stats_label = tk.Label(
            header_frame,
            text="กำลังโหลดข้อมูล...",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            padx=12,
            pady=6,
            relief=tk.FLAT
        )
        self.stats_label.place(relx=1.0, rely=0.5, anchor=tk.E)

        # 2. Control Toolbar
        toolbar = ttk.Frame(self, padding=(16, 12, 16, 8))
        toolbar.pack(fill=tk.X, side=tk.TOP)

        # Search Box
        ttk.Label(toolbar, text="🔍 ค้นหา:", font=self.bold_font).pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.apply_filter)
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=22, font=self.default_font)
        search_entry.pack(side=tk.LEFT, padx=(0, 15))

        # Tier Filter
        ttk.Label(toolbar, text="กรอง Tier:", font=self.bold_font).pack(side=tk.LEFT, padx=(0, 4))
        self.tier_filter_var = tk.StringVar(value="ทั้งหมด")
        tier_options = ["ทั้งหมด", "T0", "SSS", "S", "A", "B", "D", "Other"]
        tier_combo = ttk.Combobox(toolbar, textvariable=self.tier_filter_var, values=tier_options, state="readonly", width=10)
        tier_combo.pack(side=tk.LEFT, padx=(0, 20))
        tier_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # Action Buttons
        ttk.Button(toolbar, text="➕ เพิ่มตัวละคร (Add)", command=self.add_character).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(toolbar, text="✏️ แก้ไข (Edit)", command=self.edit_selected).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(toolbar, text="🗑️ ลบ (Delete)", command=self.delete_character).pack(side=tk.LEFT, padx=(0, 6))

        # Right-side Toolbar Buttons
        ttk.Button(toolbar, text="🔄 รีโหลด (Reload)", command=self.reload_all).pack(side=tk.RIGHT, padx=(6, 0))
        ttk.Button(toolbar, text="🌐 Git Pull", command=self.git_pull).pack(side=tk.RIGHT)

        # 3. Treeview Table Frame
        table_frame = ttk.Frame(self, padding=(16, 0, 16, 10))
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("tier", "name", "stars", "count", "extra", "role", "element", "note")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("tier", text="Tier", command=lambda: self.sort_tree("tier"))
        self.tree.heading("name", text="ชื่อตัวละคร (Character)", command=lambda: self.sort_tree("name"))
        self.tree.heading("stars", text="ระดับดาว (Stars)", command=lambda: self.sort_tree("stars"))
        self.tree.heading("count", text="จำนวนตัว", command=lambda: self.sort_tree("count"))
        self.tree.heading("extra", text="ตัวซ้ำ 5★", command=lambda: self.sort_tree("extra"))
        self.tree.heading("role", text="สาย / บทบาท", command=lambda: self.sort_tree("role"))
        self.tree.heading("element", text="ธาตุ", command=lambda: self.sort_tree("element"))
        self.tree.heading("note", text="หมายเหตุ", command=lambda: self.sort_tree("note"))

        self.tree.column("tier", width=80, anchor=tk.CENTER)
        self.tree.column("name", width=220, anchor=tk.W)
        self.tree.column("stars", width=120, anchor=tk.CENTER)
        self.tree.column("count", width=80, anchor=tk.CENTER)
        self.tree.column("extra", width=90, anchor=tk.CENTER)
        self.tree.column("role", width=140, anchor=tk.W)
        self.tree.column("element", width=110, anchor=tk.W)
        self.tree.column("note", width=180, anchor=tk.W)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda e: self.edit_selected())
        self.tree.bind("<Return>", lambda e: self.edit_selected())

        # Tag Colors for Tiers
        self.tree.tag_configure("T0", background="#ffe4e6")
        self.tree.tag_configure("SSS", background="#ffedd5")
        self.tree.tag_configure("S", background="#fef9c3")
        self.tree.tag_configure("A", background="#dbeafe")
        self.tree.tag_configure("B", background="#cffafe")
        self.tree.tag_configure("D", background="#f1f5f9")
        self.tree.tag_configure("Other", background="#ffffff")

        # 4. Bottom Save Bar
        bottom_frame = ttk.Frame(self, padding=(16, 10, 16, 8))
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Git Auto-Push Checkbox
        self.git_sync_var = tk.BooleanVar(value=True)
        self.git_check = ttk.Checkbutton(
            bottom_frame, 
            text="🚀 ซิงก์ Git อัตโนมัติ (Commit & Push ขึ้น GitHub หลังกดบันทึก)", 
            variable=self.git_sync_var
        )
        self.git_check.pack(side=tk.LEFT, padx=(0, 20))

        # Big Save Button
        save_btn = tk.Button(
            bottom_frame,
            text="💾 บันทึกข้อมูลลงไฟล์ทันที (Save to Files)",
            font=("Segoe UI", 11, "bold"),
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_all
        )
        save_btn.pack(side=tk.RIGHT)

        # 5. Status Bar
        self.status_var = tk.StringVar(value="พร้อมใช้งาน (กด Ctrl+S เพื่อบันทึก)")
        status_bar = tk.Label(
            self, 
            textvariable=self.status_var, 
            font=("Segoe UI", 8), 
            fg="#64748b", 
            bg="#e2e8f0", 
            anchor=tk.W, 
            padx=12, 
            pady=4
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def load_export_data(self):
        """Load Ocean_Saga_AI_Context_Export.json."""
        if not os.path.exists(EXPORT_JSON_PATH):
            messagebox.showerror("ไม่พบไฟล์", f"ไม่พบไฟล์:\n{EXPORT_JSON_PATH}")
            return

        try:
            with open(EXPORT_JSON_PATH, "r", encoding="utf-8") as f:
                self.export_json_data = json.load(f)

            # Build Real Tier Map
            self.real_tier_map = {}
            for t_raw, chars in self.export_json_data.get("real_tier_list", {}).items():
                t = "T0" if "T0" in t_raw else t_raw
                for name in chars:
                    self.real_tier_map[name.strip()] = t

            # Load User Owned Characters
            self.roster = self.export_json_data.get("user_owned_characters", [])
            # Fill missing tiers
            for char in self.roster:
                if not char.get("tier") or char["tier"] not in TIER_ORDER:
                    char["tier"] = self.real_tier_map.get(char["name"], "Other")

            self.apply_filter()
            self.update_stats()
            self.status_var.set(f"โหลดข้อมูลตัวละครเรียบร้อยแล้ว: {len(self.roster)} ตัวละคร")
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการอ่าน {EXPORT_JSON_PATH}:\n{e}")

    def update_stats(self):
        total_types = len(self.roster)
        total_copies = sum(c.get("count", 1) for c in self.roster)
        tier_counts = {}
        for c in self.roster:
            t = c.get("tier", "Other")
            tier_counts[t] = tier_counts.get(t, 0) + 1

        parts = [f"ทั้งหมด: {total_types} ชนิด ({total_copies} ตัว)"]
        for t in ["T0", "SSS", "S", "A", "B", "D"]:
            if t in tier_counts:
                parts.append(f"{t}: {tier_counts[t]}")

        self.stats_label.config(text="  |  ".join(parts))

    def apply_filter(self, *args):
        search_text = self.search_var.get().strip().lower()
        selected_tier = self.tier_filter_var.get()

        self.filtered_roster = []
        for c in self.roster:
            name = c.get("name", "").lower()
            tier = c.get("tier", "Other")

            if search_text and search_text not in name:
                continue
            if selected_tier != "ทั้งหมด" and tier != selected_tier:
                continue

            self.filtered_roster.append(c)

        self.refresh_table()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        
        # Sort by Tier order first, then Stars descending, then Name
        def sort_key(c):
            t = c.get("tier", "Other")
            t_idx = TIER_ORDER.index(t) if t in TIER_ORDER else len(TIER_ORDER)
            stars = c.get("stars", 5)
            name = c.get("name", "")
            return (t_idx, -stars, name)

        sorted_list = sorted(self.filtered_roster, key=sort_key)

        for c in sorted_list:
            name = c.get("name", "")
            tier = c.get("tier", "Other")
            stars_num = c.get("stars", 5)
            count = c.get("count", 1)
            extra = c.get("extra_5star_copies", 0)
            note = c.get("note", "")

            # Look up DB details
            db_info = self.ss_db.get(name, {})
            role = db_info.get("class_th") or db_info.get("class_en") or db_info.get("role") or "-"
            element = db_info.get("element_th") or db_info.get("element_en") or "-"

            # Star text
            star_text = f"★ {stars_num} ดาว" if stars_num > 5 else "5★"
            extra_text = f"+{extra}" if extra > 0 else "-"

            tag = tier if tier in TIER_ORDER else "Other"
            self.tree.insert(
                "",
                tk.END,
                values=(tier, name, star_text, count, extra_text, role, element, note),
                tags=(tag,)
            )

    def sort_tree(self, col):
        # Allow user to toggle sort on column click
        pass

    def add_character(self):
        dlg = CharacterDialog(self, self.ss_db, self.real_tier_map)
        self.wait_window(dlg)
        if dlg.result:
            new_char = dlg.result
            # Check if character already exists
            existing = next((c for c in self.roster if c["name"] == new_char["name"]), None)
            if existing:
                if messagebox.askyesno("พบตัวละครเดิม", f"'{new_char['name']}' มีอยู่ในรายการอยู่แล้ว ต้องการอัปเดตข้อมูลทับหรือไม่?"):
                    existing.update(new_char)
            else:
                self.roster.append(new_char)

            self.apply_filter()
            self.update_stats()
            self.status_var.set(f"เพิ่มตัวละคร '{new_char['name']}' เรียบร้อย (อย่าลืมกดบันทึก)")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกตัวละครในตารางที่ต้องการแก้ไข")
            return

        item = self.tree.item(selected[0])
        char_name = item["values"][1]
        char_data = next((c for c in self.roster if c["name"] == char_name), None)
        if not char_data:
            return

        dlg = CharacterDialog(self, self.ss_db, self.real_tier_map, existing_data=char_data)
        self.wait_window(dlg)
        if dlg.result:
            char_data.update(dlg.result)
            self.apply_filter()
            self.update_stats()
            self.status_var.set(f"แก้ไข '{char_name}' เรียบร้อย (อย่าลืมกดบันทึก)")

    def delete_character(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("แจ้งเตือน", "กรุณาเลือกตัวละครที่ต้องการลบ")
            return

        item = self.tree.item(selected[0])
        char_name = item["values"][1]
        
        if messagebox.askyesno("ยืนยันการลบ", f"คุณต้องการลบ '{char_name}' ออกจากรายการ ID ของคุณใช่หรือไม่?"):
            self.roster = [c for c in self.roster if c["name"] != char_name]
            self.apply_filter()
            self.update_stats()
            self.status_var.set(f"ลบ '{char_name}' ออกจากรายการแล้ว (อย่าลืมกดบันทึก)")

    def reload_all(self):
        if messagebox.askyesno("ยืนยันรีโหลด", "ต้องการโหลดข้อมูลเดิมจากไฟล์ทับข้อมูลปัจจุบันหรือไม่? (การแก้ไขที่ยังไม่ได้บันทึกจะหายไป)"):
            self.load_export_data()

    def generate_section_4_markdown(self, now_str):
        groups = {}
        for item in self.roster:
            t = item.get("tier", "Other")
            if "T0" in t:
                t = "T0"
            groups.setdefault(t, []).append(item)

        lines = [f"## 4. รายชื่อตัวละครของ ID ใหม่ปัจจุบัน (อัปเดต {now_str})"]

        for t in ["T0", "SSS", "S", "A", "B", "D", "Other"]:
            if t not in groups or not groups[t]:
                continue
            chars = groups[t]
            total_u = len(chars)
            total_c = sum(c.get("count", 1) for c in chars)

            if t in ["T0", "SSS"]:
                txts = []
                for c in chars:
                    name = c["name"]
                    stars = c.get("stars", 5)
                    extra = c.get("extra_5star_copies", 0)
                    note = c.get("note", "")
                    
                    desc_parts = [f"**{stars} ดาว**"]
                    if extra > 0:
                        desc_parts.append(f"+ ซ้ำ **5 ดาว {extra} ตัว** พร้อมขึ้นดาวต่อ!")
                    if note:
                        desc_parts.append(note)
                    txts.append(f"`{name}` ({' '.join(desc_parts)})")
                lines.append(f"- **ระดับ {t}:** {', '.join(txts)}")
            else:
                if total_c > total_u:
                    label = f"ระดับ {t} ({total_u} ชนิด / {total_c} ตัว):"
                else:
                    label = f"ระดับ {t} ({total_u} ตัว):"

                txts = []
                for c in chars:
                    name = c["name"]
                    stars = c.get("stars", 5)
                    count = c.get("count", 1)
                    extra = c.get("extra_5star_copies", 0)
                    note = c.get("note", "")

                    desc = [f"{stars}★" if t == "D" else f"{stars} ดาว"]
                    if count > 1:
                        desc.append(f"x{count}")
                    if extra > 0:
                        desc.append(f"+ซ้ำ{extra}")
                    if note:
                        desc.append(note)
                    
                    alias = " / หนวดขาว" if name == "Whitebeard" else ""
                    txts.append(f"`{name}{alias}` ({' '.join(desc)})")
                lines.append(f"- **{label}** {', '.join(txts)}")

        return "\n".join(lines) + "\n"

    def save_all(self):
        """Save to JSON & MD, then trigger Git Sync if enabled."""
        now = datetime.datetime.now()
        iso_now = now.isoformat()
        thai_now = format_thai_date(now)

        # 1. Update JSON
        try:
            # Backup JSON
            if os.path.exists(EXPORT_JSON_PATH):
                shutil.copy2(EXPORT_JSON_PATH, EXPORT_JSON_PATH + ".bak")

            self.export_json_data["exported_at"] = iso_now
            # Sort roster by Tier before saving
            def sort_key(c):
                t = c.get("tier", "Other")
                t_idx = TIER_ORDER.index(t) if t in TIER_ORDER else len(TIER_ORDER)
                return (t_idx, -c.get("stars", 5), c.get("name", ""))

            self.export_json_data["user_owned_characters"] = sorted(self.roster, key=sort_key)

            with open(EXPORT_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(self.export_json_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถบันทึก {EXPORT_JSON_PATH}:\n{e}")
            return

        # 2. Update MD Section 4
        try:
            if os.path.exists(EXPORT_MD_PATH):
                shutil.copy2(EXPORT_MD_PATH, EXPORT_MD_PATH + ".bak")

                with open(EXPORT_MD_PATH, "r", encoding="utf-8") as f:
                    md_content = f.read()

                new_sec4 = self.generate_section_4_markdown(thai_now)
                pattern = r'(## 4\. รายชื่อตัวละครของ ID ใหม่ปัจจุบัน.*?\n)(.*?)(?=\n---\n\n## 5\.|\Z)'

                if re.search(pattern, md_content, re.DOTALL):
                    updated_md = re.sub(pattern, new_sec4, md_content, flags=re.DOTALL)
                else:
                    # Append if pattern somehow missing
                    updated_md = md_content + "\n\n" + new_sec4

                with open(EXPORT_MD_PATH, "w", encoding="utf-8") as f:
                    f.write(updated_md)
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถบันทึก {EXPORT_MD_PATH}:\n{e}")
            return

        msg = f"บันทึกไฟล์เรียบร้อยแล้ว!\n- {os.path.basename(EXPORT_JSON_PATH)}\n- {os.path.basename(EXPORT_MD_PATH)}"
        self.status_var.set(f"บันทึกสำเร็จเมื่อ {now.strftime('%H:%M:%S')}")

        # 3. Optional Git Sync
        if self.git_sync_var.get():
            self.status_var.set("กำลังบันทึกและซิงก์ขึ้น GitHub...")
            threading.Thread(target=self.run_git_sync, args=(now,), daemon=True).start()
        else:
            messagebox.showinfo("สำเร็จ", msg)

    def run_git_sync(self, dt):
        try:
            summary = f"Update roster ({len(self.roster)} characters, {format_thai_date(dt)})"
            # git add
            subprocess.run(["git", "add", "Ocean_Saga_AI_Context_Export.json", "Ocean_Saga_AI_Context_Export.md"], cwd=BASE_DIR, check=True)
            # git commit
            res = subprocess.run(["git", "commit", "-m", summary], cwd=BASE_DIR, capture_output=True, text=True)
            if "nothing to commit" in res.stdout:
                self.status_var.set("ไฟล์เหมือนเดิม ไม่มีข้อมูลเปลี่ยนแปลงบน Git")
                self.after(0, lambda: messagebox.showinfo("สำเร็จ", "บันทึกไฟล์แล้ว (ไม่มีการเปลี่ยนแปลงใหม่บน Git)"))
                return

            # git push
            push_res = subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, text=True, check=True)
            self.status_var.set("ซิงก์ขึ้น GitHub เรียบร้อยแล้ว ✅")
            self.after(0, lambda: messagebox.showinfo("สำเร็จ", f"บันทึกไฟล์และ Push ขึ้น GitHub เรียบร้อยแล้ว!\n\nCommit: {summary}"))
        except Exception as err:
            self.status_var.set(f"บันทึกไฟล์สำเร็จ แต่ Git Sync ผิดพลาด: {err}")
            self.after(0, lambda: messagebox.showwarning("Git Sync Warning", f"บันทึกไฟล์สำเร็จแล้ว แต่ไม่สามารถ Push ขึ้น GitHub ได้:\n{err}"))

    def git_pull(self):
        def _pull():
            try:
                self.status_var.set("กำลังดึงข้อมูลล่าสุดจาก GitHub...")
                res = subprocess.run(["git", "pull", "--rebase"], cwd=BASE_DIR, capture_output=True, text=True, check=True)
                self.status_var.set("ดึงข้อมูลสำเร็จ")
                self.after(0, lambda: (messagebox.showinfo("Git Pull", f"ดึงข้อมูลล่าสุดเรียบร้อย:\n{res.stdout}"), self.load_export_data()))
            except Exception as e:
                self.status_var.set("เกิดข้อผิดพลาดในการดึงข้อมูล Git")
                self.after(0, lambda: messagebox.showerror("Git Pull Error", f"ไม่สามารถ Git Pull ได้:\n{e}"))

        threading.Thread(target=_pull, daemon=True).start()


if __name__ == "__main__":
    app = OceanSagaRosterApp()
    app.mainloop()
