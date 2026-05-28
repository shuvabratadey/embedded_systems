"""
ESP-IDF BLE GATT Configurator
A GUI tool for generating ESP-IDF BLE C code, inspired by Silicon Labs' GATT Configurator.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import uuid
import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  THEME & STYLE CONSTANTS
# ─────────────────────────────────────────────────────────────
BG_DARK      = "#1a1d23"
BG_MID       = "#22262f"
BG_PANEL     = "#2a2e3a"
BG_CARD      = "#303544"
BG_HOVER     = "#373d4e"
ACCENT_BLUE  = "#4a9eff"
ACCENT_GREEN = "#3ecf8e"
ACCENT_AMBER = "#f5a623"
ACCENT_RED   = "#e05c5c"
TEXT_PRIMARY = "#e8eaf0"
TEXT_SEC     = "#8b91a1"
TEXT_MUTED   = "#5a6070"
BORDER       = "#3a3f50"
SEL_BG       = "#1e3a5f"

FONT_TITLE   = ("Consolas", 13, "bold")
FONT_HEAD    = ("Consolas", 11, "bold")
FONT_NORMAL  = ("Consolas", 10)
FONT_SMALL   = ("Consolas", 9)
FONT_MONO    = ("Courier New", 10)

# ─────────────────────────────────────────────────────────────
#  STANDARD BLE UUIDs (GATT Services & Characteristics)
# ─────────────────────────────────────────────────────────────
STANDARD_SERVICES = {
    "Generic Access (0x1800)":             "1800",
    "Generic Attribute (0x1801)":          "1801",
    "Device Information (0x180A)":         "180A",
    "Battery Service (0x180F)":            "180F",
    "Heart Rate (0x180D)":                 "180D",
    "Health Thermometer (0x1809)":         "1809",
    "Human Interface Device (0x1812)":     "1812",
    "Nordic UART Service (Custom)":        "6E400001-B5A3-F393-E0A9-E50E24DCCA9E",
    "Custom Service":                      "CUSTOM",
}

STANDARD_CHARACTERISTICS = {
    "Device Name (0x2A00)":                "2A00",
    "Appearance (0x2A01)":                 "2A01",
    "Battery Level (0x2A19)":              "2A19",
    "Model Number String (0x2A24)":        "2A24",
    "Serial Number String (0x2A25)":       "2A25",
    "Firmware Revision String (0x2A26)":   "2A26",
    "Hardware Revision String (0x2A27)":   "2A27",
    "Software Revision String (0x2A28)":   "2A28",
    "Manufacturer Name String (0x2A29)":   "2A29",
    "Heart Rate Measurement (0x2A37)":     "2A37",
    "Temperature Measurement (0x2A1C)":    "2A1C",
    "Nordic UART TX (Custom)":             "6E400002-B5A3-F393-E0A9-E50E24DCCA9E",
    "Nordic UART RX (Custom)":             "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",
    "Custom Characteristic":               "CUSTOM",
}

# ─────────────────────────────────────────────────────────────
#  DATA MODELS
# ─────────────────────────────────────────────────────────────
class BLECharacteristic:
    def __init__(self, name="New Characteristic", uuid_val="CUSTOM"):
        self.name       = name
        self.uuid       = uuid_val if uuid_val != "CUSTOM" else str(uuid.uuid4()).upper()
        self.prop_read     = tk.BooleanVar(value=False)
        self.prop_write    = tk.BooleanVar(value=False)
        self.prop_write_nr = tk.BooleanVar(value=False)
        self.prop_notify   = tk.BooleanVar(value=False)
        self.prop_indicate = tk.BooleanVar(value=False)
        self.prop_broadcast= tk.BooleanVar(value=False)
        self.perm_read     = tk.BooleanVar(value=False)
        self.perm_write    = tk.BooleanVar(value=False)
        self.perm_read_enc = tk.BooleanVar(value=False)
        self.perm_write_enc= tk.BooleanVar(value=False)
        self.value_type    = tk.StringVar(value="uint8_t")
        self.value_len     = tk.IntVar(value=1)
        self.init_value    = tk.StringVar(value="0x00")
        self.description   = tk.StringVar(value="")
        self.has_cccd      = tk.BooleanVar(value=False)

class BLEService:
    def __init__(self, name="New Service", uuid_val="CUSTOM"):
        self.name            = name
        self.uuid            = uuid_val if uuid_val != "CUSTOM" else str(uuid.uuid4()).upper()
        self.primary         = tk.BooleanVar(value=True)
        self.characteristics = []

class BLEConfig:
    def __init__(self):
        self.device_name     = tk.StringVar(value="ESP32_BLE")
        self.adv_interval_min= tk.IntVar(value=160)
        self.adv_interval_max= tk.IntVar(value=320)
        self.tx_power        = tk.StringVar(value="ESP_PWR_LVL_P9")
        self.appearance      = tk.StringVar(value="0x0000")
        self.mtu             = tk.IntVar(value=500)
        self.security_mode   = tk.StringVar(value="None")
        self.services        = []

# ─────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────
class BLEConfigurator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ESP-IDF BLE GATT Configurator")
        self.geometry("1400x880")
        self.minsize(1100, 700)
        self.configure(bg=BG_DARK)
        self.config_data    = BLEConfig()
        self.selected_node  = None   # ('service', idx) or ('char', svc_idx, char_idx)
        self._build_styles()
        self._build_ui()
        self._refresh_tree()

    # ── Styles ──────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Treeview
        style.configure("GATT.Treeview",
            background=BG_MID, foreground=TEXT_PRIMARY,
            fieldbackground=BG_MID, borderwidth=0,
            rowheight=28, font=FONT_NORMAL)
        style.configure("GATT.Treeview.Heading",
            background=BG_PANEL, foreground=ACCENT_BLUE,
            font=FONT_HEAD, borderwidth=0, relief="flat")
        style.map("GATT.Treeview",
            background=[("selected", SEL_BG)],
            foreground=[("selected", TEXT_PRIMARY)])

        # Scrollbar
        style.configure("Dark.Vertical.TScrollbar",
            troughcolor=BG_DARK, background=BORDER,
            arrowcolor=TEXT_SEC, borderwidth=0)
        style.configure("Dark.Horizontal.TScrollbar",
            troughcolor=BG_DARK, background=BORDER,
            arrowcolor=TEXT_SEC, borderwidth=0)

        # Combobox
        style.configure("Dark.TCombobox",
            fieldbackground=BG_CARD, background=BG_CARD,
            foreground=TEXT_PRIMARY, selectbackground=SEL_BG,
            borderwidth=1, relief="flat", font=FONT_NORMAL)
        style.map("Dark.TCombobox",
            fieldbackground=[("readonly", BG_CARD)],
            foreground=[("readonly", TEXT_PRIMARY)])

        # Checkbutton
        style.configure("Dark.TCheckbutton",
            background=BG_PANEL, foreground=TEXT_PRIMARY,
            font=FONT_NORMAL, focuscolor="")
        style.map("Dark.TCheckbutton",
            background=[("active", BG_PANEL)],
            foreground=[("active", ACCENT_BLUE)])

        # Notebook
        style.configure("Dark.TNotebook",
            background=BG_DARK, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
            background=BG_PANEL, foreground=TEXT_SEC,
            font=FONT_NORMAL, padding=[12, 6],
            borderwidth=0)
        style.map("Dark.TNotebook.Tab",
            background=[("selected", BG_MID)],
            foreground=[("selected", ACCENT_BLUE)])

        # Separator
        style.configure("Dark.TSeparator", background=BORDER)

        # LabelFrame
        style.configure("Dark.TLabelframe",
            background=BG_PANEL, foreground=ACCENT_BLUE,
            font=FONT_HEAD, bordercolor=BORDER, borderwidth=1)
        style.configure("Dark.TLabelframe.Label",
            background=BG_PANEL, foreground=ACCENT_BLUE, font=FONT_HEAD)

        # Spinbox (via Entry)
        self.option_add("*TCombobox*Listbox.background", BG_CARD)
        self.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
        self.option_add("*TCombobox*Listbox.selectBackground", SEL_BG)
        self.option_add("*TCombobox*Listbox.font", FONT_NORMAL)

    # ── Main UI Layout ───────────────────────────────────────
    def _build_ui(self):
        # ── Top Toolbar
        self._build_toolbar()

        # ── Main 3-pane layout
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
            bg=BORDER, sashwidth=4, sashrelief="flat",
            opaqueresize=True)
        paned.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Left: service/char browser (GATT tree)
        left_frame = tk.Frame(paned, bg=BG_DARK, width=320)
        self._build_gatt_panel(left_frame)
        paned.add(left_frame, minsize=260)

        # Center: properties panel
        center_frame = tk.Frame(paned, bg=BG_DARK, width=440)
        self._build_properties_panel(center_frame)
        paned.add(center_frame, minsize=340)

        # Right: BLE settings + code preview
        right_frame = tk.Frame(paned, bg=BG_DARK)
        self._build_right_panel(right_frame)
        paned.add(right_frame, minsize=360)

        # ── Status bar
        self._build_statusbar()

    # ── Toolbar ─────────────────────────────────────────────
    def _build_toolbar(self):
        bar = tk.Frame(self, bg=BG_PANEL, height=52, bd=0)
        bar.pack(fill=tk.X, side=tk.TOP)
        bar.pack_propagate(False)

        # Logo / Title
        logo = tk.Label(bar, text="⬡  ESP-IDF BLE GATT Configurator",
            bg=BG_PANEL, fg=ACCENT_BLUE, font=("Consolas", 14, "bold"),
            padx=16)
        logo.pack(side=tk.LEFT, pady=8)

        sep = tk.Frame(bar, bg=BORDER, width=1)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=10)

        btn_data = [
            ("＋ Add Service",    ACCENT_BLUE,  self._add_service_dialog),
            ("＋ Add Char",       ACCENT_GREEN, self._add_char_dialog),
            ("✕ Delete",          ACCENT_RED,   self._delete_selected),
            ("⬆ Move Up",         TEXT_SEC,     self._move_up),
            ("⬇ Move Down",       TEXT_SEC,     self._move_down),
        ]
        for label, color, cmd in btn_data:
            btn = self._toolbar_btn(bar, label, color, cmd)
            btn.pack(side=tk.LEFT, padx=4, pady=8)

        sep2 = tk.Frame(bar, bg=BORDER, width=1)
        sep2.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=10)

        gen_btn = self._toolbar_btn(bar, "⚙  Generate main.c", ACCENT_AMBER,
            self._generate_code, bold=True)
        gen_btn.pack(side=tk.LEFT, padx=4, pady=8)

        save_btn = self._toolbar_btn(bar, "💾  Save Config", TEXT_SEC, self._save_config)
        save_btn.pack(side=tk.LEFT, padx=4, pady=8)
        load_btn = self._toolbar_btn(bar, "📂  Load Config", TEXT_SEC, self._load_config)
        load_btn.pack(side=tk.LEFT, padx=4, pady=8)

        # Right-side: ESP chip indicator
        chip = tk.Label(bar, text="● ESP32  |  IDF v5.x",
            bg=BG_PANEL, fg=ACCENT_GREEN, font=FONT_SMALL, padx=12)
        chip.pack(side=tk.RIGHT)

    def _toolbar_btn(self, parent, text, color, cmd, bold=False):
        fnt = ("Consolas", 10, "bold") if bold else FONT_NORMAL
        btn = tk.Label(parent, text=text, bg=BG_CARD, fg=color,
            font=fnt, padx=10, pady=4, cursor="hand2",
            relief="flat", bd=0)
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>", lambda e: btn.config(bg=BG_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BG_CARD))
        return btn

    # ── GATT Tree Panel (Left) ───────────────────────────────
    def _build_gatt_panel(self, parent):
        # Header
        hdr = tk.Frame(parent, bg=BG_PANEL, height=36)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="GATT Profile", bg=BG_PANEL,
            fg=ACCENT_BLUE, font=FONT_HEAD, padx=12).pack(side=tk.LEFT, pady=6)

        # Tree frame
        tree_frame = tk.Frame(parent, bg=BG_MID)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
            style="Dark.Vertical.TScrollbar")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, style="GATT.Treeview",
            yscrollcommand=vsb.set, selectmode="browse",
            columns=("uuid", "type"), show="tree headings")
        self.tree.heading("#0",    text="Name")
        self.tree.heading("uuid",  text="UUID")
        self.tree.heading("type",  text="Type")
        self.tree.column("#0",    width=145, minwidth=100)
        self.tree.column("uuid",  width=130, minwidth=80)
        self.tree.column("type",  width=80,  minwidth=60)
        self.tree.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-Button-1>", self._on_tree_double)

        # Tag colors
        self.tree.tag_configure("service",  foreground=ACCENT_BLUE,  font=FONT_HEAD)
        self.tree.tag_configure("char",     foreground=TEXT_PRIMARY,  font=FONT_NORMAL)
        self.tree.tag_configure("cccd",     foreground=TEXT_MUTED,    font=FONT_SMALL)

        # Drag-and-drop state
        self._drag_item = None
        self.tree.bind("<ButtonPress-1>",  self._drag_start)
        self.tree.bind("<B1-Motion>",      self._drag_motion)
        self.tree.bind("<ButtonRelease-1>",self._drag_release)

        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0, bg=BG_CARD,
            fg=TEXT_PRIMARY, activebackground=SEL_BG,
            activeforeground=TEXT_PRIMARY, font=FONT_NORMAL,
            bd=0, relief="flat")
        self.context_menu.add_command(label="Add Service",        command=self._add_service_dialog)
        self.context_menu.add_command(label="Add Characteristic", command=self._add_char_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Rename",             command=self._rename_selected)
        self.context_menu.add_command(label="Delete",             command=self._delete_selected)
        self.tree.bind("<Button-3>", self._show_context_menu)

        # Bottom add buttons
        btn_row = tk.Frame(parent, bg=BG_PANEL)
        btn_row.pack(fill=tk.X, pady=2)
        self._mini_btn(btn_row, "＋ Service",    ACCENT_BLUE,  self._add_service_dialog).pack(side=tk.LEFT, padx=6, pady=6)
        self._mini_btn(btn_row, "＋ Char",       ACCENT_GREEN, self._add_char_dialog).pack(side=tk.LEFT, pady=6)
        self._mini_btn(btn_row, "✕ Delete",      ACCENT_RED,   self._delete_selected).pack(side=tk.RIGHT, padx=6, pady=6)

    def _mini_btn(self, parent, text, color, cmd):
        btn = tk.Label(parent, text=text, bg=BG_CARD, fg=color,
            font=FONT_SMALL, padx=8, pady=3, cursor="hand2")
        btn.bind("<Button-1>", lambda e: cmd())
        btn.bind("<Enter>", lambda e: btn.config(bg=BG_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BG_CARD))
        return btn

    # ── Properties Panel (Center) ────────────────────────────
    def _build_properties_panel(self, parent):
        # Header bar
        hdr = tk.Frame(parent, bg=BG_PANEL, height=36, width=500)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        self.props_title = tk.Label(hdr, text="Properties",
            bg=BG_PANEL, fg=ACCENT_BLUE, font=FONT_HEAD, padx=12)
        self.props_title.pack(side=tk.LEFT, pady=6)

        # Stack all three panels in the same area; show/hide via pack
        self._props_container = tk.Frame(parent, bg=BG_DARK)
        self._props_container.pack(fill=tk.BOTH, expand=True)

        # Empty placeholder
        self.props_empty = tk.Frame(self._props_container, bg=BG_DARK)
        self._build_empty_props(self.props_empty)

        # Service properties (scrollable)
        self.props_svc_outer = tk.Frame(self._props_container, bg=BG_PANEL)
        svc_canvas = tk.Canvas(self.props_svc_outer, bg=BG_PANEL,
            highlightthickness=0, bd=0)
        svc_vsb = ttk.Scrollbar(self.props_svc_outer, orient="vertical",
            style="Dark.Vertical.TScrollbar", command=svc_canvas.yview)
        svc_canvas.configure(yscrollcommand=svc_vsb.set)
        svc_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        svc_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.props_svc_frame = tk.Frame(svc_canvas, bg=BG_PANEL)
        svc_canvas.create_window((0, 0), window=self.props_svc_frame, anchor="nw")
        self.props_svc_frame.bind("<Configure>",
            lambda e: svc_canvas.configure(scrollregion=svc_canvas.bbox("all")))
        self._build_service_props(self.props_svc_frame)

        # Characteristic properties (scrollable)
        self.props_char_outer = tk.Frame(self._props_container, bg=BG_PANEL)
        char_canvas = tk.Canvas(self.props_char_outer, bg=BG_PANEL,
            highlightthickness=0, bd=0)
        char_vsb = ttk.Scrollbar(self.props_char_outer, orient="vertical",
            style="Dark.Vertical.TScrollbar", command=char_canvas.yview)
        char_canvas.configure(yscrollcommand=char_vsb.set)
        char_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        char_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.props_char_frame = tk.Frame(char_canvas, bg=BG_PANEL)
        char_canvas.create_window((0, 0), window=self.props_char_frame, anchor="nw")
        self.props_char_frame.bind("<Configure>",
            lambda e: char_canvas.configure(scrollregion=char_canvas.bbox("all")))
        self._build_char_props(self.props_char_frame)

        # Mousewheel scroll support
        def _on_mousewheel(canvas, event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        svc_canvas.bind("<MouseWheel>",  lambda e: _on_mousewheel(svc_canvas, e))
        char_canvas.bind("<MouseWheel>", lambda e: _on_mousewheel(char_canvas, e))
        self.props_svc_frame.bind("<MouseWheel>",  lambda e: _on_mousewheel(svc_canvas, e))
        self.props_char_frame.bind("<MouseWheel>", lambda e: _on_mousewheel(char_canvas, e))

        # Show placeholder by default
        self._show_props_panel("empty")

    def _build_empty_props(self, parent):
        tk.Label(parent,
            text="\n\n\n⬡\n\nSelect a service or\ncharacteristic\nto view properties",
            bg=BG_DARK, fg=TEXT_MUTED, font=("Consolas", 11),
            justify=tk.CENTER).pack(expand=True)

    def _show_props_panel(self, which):
        """Show one of 'empty', 'service', 'char' panels."""
        for w in (self.props_empty, self.props_svc_outer, self.props_char_outer):
            w.pack_forget()
        if which == "service":
            self.props_svc_outer.pack(fill=tk.BOTH, expand=True)
        elif which == "char":
            self.props_char_outer.pack(fill=tk.BOTH, expand=True)
        else:
            self.props_empty.pack(fill=tk.BOTH, expand=True)

    def _labeled_entry(self, parent, label, var, row, col=0, width=24, readonly=False):
        tk.Label(parent, text=label, bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL, anchor="w").grid(row=row, column=col, sticky="w",
            padx=(12,4), pady=(6,2))
        state = "readonly" if readonly else "normal"
        e = tk.Entry(parent, textvariable=var, bg=BG_CARD, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat", bd=4,
            font=FONT_NORMAL, width=width, state=state,
            disabledbackground=BG_CARD, disabledforeground=TEXT_SEC)
        e.grid(row=row+1, column=col, sticky="ew", padx=(12,4), pady=(0,4))
        return e

    def _build_service_props(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        tk.Label(parent, text="SERVICE PROPERTIES", bg=BG_PANEL,
            fg=ACCENT_BLUE, font=FONT_SMALL).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12,6))

        self._svc_name_var = tk.StringVar()
        self._svc_uuid_var = tk.StringVar()
        self._svc_primary_var = tk.BooleanVar(value=True)

        self._labeled_entry(parent, "Service Name", self._svc_name_var, 1, 0)
        self._labeled_entry(parent, "UUID (hex or full)", self._svc_uuid_var, 3, 0, width=32)

        tk.Label(parent, text="Service Type", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL, anchor="w").grid(row=5, column=0, sticky="w", padx=(12,4), pady=(6,2))
        chk = ttk.Checkbutton(parent, text="Primary Service",
            variable=self._svc_primary_var, style="Dark.TCheckbutton")
        chk.grid(row=6, column=0, sticky="w", padx=12, pady=(0,6))

        tk.Frame(parent, bg=BORDER, height=1).grid(
            row=7, column=0, columnspan=2, sticky="ew", padx=12, pady=8)

        apply_btn = tk.Label(parent, text="  ✓  Apply Changes  ",
            bg=ACCENT_BLUE, fg=BG_DARK, font=FONT_HEAD,
            padx=8, pady=6, cursor="hand2")
        apply_btn.grid(row=8, column=0, padx=12, pady=4, sticky="w")
        apply_btn.bind("<Button-1>", lambda e: self._apply_service_props())

    def _build_char_props(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        # ── Header
        tk.Label(parent, text="CHARACTERISTIC PROPERTIES", bg=BG_PANEL,
            fg=ACCENT_GREEN, font=FONT_SMALL).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12,6))

        self._char_name_var = tk.StringVar()
        self._char_uuid_var = tk.StringVar()
        self._char_desc_var = tk.StringVar()

        self._labeled_entry(parent, "Characteristic Name", self._char_name_var, 1, 0)
        self._labeled_entry(parent, "UUID", self._char_uuid_var, 3, 0, width=32)
        self._labeled_entry(parent, "User Description", self._char_desc_var, 5, 0, width=32)

        # ── Properties group (permissions auto-derived — no separate panel)
        sep1 = tk.LabelFrame(parent, text=" Properties ", bg=BG_PANEL,
            fg=ACCENT_GREEN, font=FONT_SMALL, bd=1, relief="groove",
            labelanchor="nw")
        sep1.grid(row=8, column=0, columnspan=2, sticky="ew",
            padx=12, pady=(10,4))

        self._prop_vars = {}
        # Keep _perm_vars as a hidden dict so codegen / save/load still works
        self._perm_vars = {
            "read":      tk.BooleanVar(value=False),
            "write":     tk.BooleanVar(value=False),
            "read_enc":  tk.BooleanVar(value=False),
            "write_enc": tk.BooleanVar(value=False),
        }

        props = [
            ("Read",            "read"),
            ("Write",           "write"),
            ("Write No Resp",   "write_nr"),
            ("Notify",          "notify"),
            ("Indicate",        "indicate"),
            ("Broadcast",       "broadcast"),
        ]
        for i, (label, key) in enumerate(props):
            var = tk.BooleanVar(value=False)
            self._prop_vars[key] = var
            chk = ttk.Checkbutton(sep1, text=label, variable=var,
                style="Dark.TCheckbutton")
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=8, pady=3)
            # Auto CCCD + auto-permissions on every property change
            var.trace_add("write", self._on_prop_changed)

        # Hint label: tells the user permissions are automatic
        tk.Label(sep1,
            text="ℹ  Read/Write permissions are set automatically from properties above.",
            bg=BG_PANEL, fg=TEXT_MUTED, font=("Consolas", 8), anchor="w"
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(2, 6))

        # ── Value group (smart section)
        sep3 = tk.LabelFrame(parent, text=" Value ", bg=BG_PANEL,
            fg=ACCENT_BLUE, font=FONT_SMALL, bd=1, relief="groove",
            labelanchor="nw")
        sep3.grid(row=9, column=0, columnspan=2, sticky="ew",
            padx=12, pady=(4, 4))
        sep3.columnconfigure(1, weight=1)

        # -- Data type
        tk.Label(sep3, text="Data Type:", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL).grid(row=0, column=0, sticky="w", padx=6, pady=(8,3))
        self._char_vtype_var = tk.StringVar(value="uint8_t")
        types = ["uint8_t", "uint16_t", "uint32_t", "int8_t", "int16_t",
                 "int32_t", "char[]", "uint8_t[]", "float", "double"]
        type_combo = ttk.Combobox(sep3, textvariable=self._char_vtype_var,
            values=types, style="Dark.TCombobox", width=14, state="readonly")
        type_combo.grid(row=0, column=1, sticky="w", padx=6, pady=(8,3))
        self._char_vtype_var.trace_add("write", self._on_value_changed)

        # -- Input format selector (row 1)
        tk.Label(sep3, text="Input Format:", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL).grid(row=1, column=0, sticky="w", padx=6, pady=3)

        fmt_frame = tk.Frame(sep3, bg=BG_PANEL)
        fmt_frame.grid(row=1, column=1, sticky="w", padx=6, pady=3)

        self._val_fmt_var = tk.StringVar(value="hex")
        for fval, flabel in [("hex","Hex"), ("dec","Decimal"), ("str","String"), ("bin","Binary")]:
            rb = tk.Radiobutton(fmt_frame, text=flabel, variable=self._val_fmt_var,
                value=fval, bg=BG_PANEL, fg=TEXT_PRIMARY, selectcolor=BG_CARD,
                activebackground=BG_PANEL, activeforeground=ACCENT_BLUE,
                font=FONT_SMALL, cursor="hand2", bd=0)
            rb.pack(side=tk.LEFT, padx=(0, 8))
            self._val_fmt_var.trace_add("write", self._on_value_changed)

        # -- Initial value entry (row 2)
        tk.Label(sep3, text="Initial Value:", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL).grid(row=2, column=0, sticky="w", padx=6, pady=3)

        val_entry_frame = tk.Frame(sep3, bg=BG_PANEL)
        val_entry_frame.grid(row=2, column=1, sticky="ew", padx=6, pady=3)
        val_entry_frame.columnconfigure(0, weight=1)

        self._char_vinit_var = tk.StringVar(value="0x00")
        self._val_entry = tk.Entry(val_entry_frame, textvariable=self._char_vinit_var,
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief="flat", bd=4, font=FONT_MONO)
        self._val_entry.grid(row=0, column=0, sticky="ew")
        self._char_vinit_var.trace_add("write", self._on_value_changed)

        # -- Live byte count badge  "N bytes"
        self._val_bytelen_var = tk.StringVar(value="1 byte")
        tk.Label(val_entry_frame, textvariable=self._val_bytelen_var,
            bg=BG_PANEL, fg=ACCENT_AMBER, font=("Consolas", 9, "bold"),
            padx=4).grid(row=0, column=1, sticky="w", padx=(4, 0))

        # -- Max Len (bytes) — auto-updated but also manually editable (row 3)
        tk.Label(sep3, text="Max Length (bytes):", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL).grid(row=3, column=0, sticky="w", padx=6, pady=3)

        len_frame = tk.Frame(sep3, bg=BG_PANEL)
        len_frame.grid(row=3, column=1, sticky="w", padx=6, pady=3)

        self._char_vlen_var = tk.IntVar(value=1)
        self._len_spin = tk.Spinbox(len_frame, textvariable=self._char_vlen_var,
            from_=1, to=512, bg=BG_CARD, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, buttonbackground=BG_CARD,
            relief="flat", font=FONT_NORMAL, width=5)
        self._len_spin.pack(side=tk.LEFT)

        self._len_auto_lbl = tk.Label(len_frame,
            text="  ← auto from value", bg=BG_PANEL, fg=TEXT_MUTED,
            font=("Consolas", 8))
        self._len_auto_lbl.pack(side=tk.LEFT)

        # -- C array preview (row 4) — read-only, updated live
        tk.Label(sep3, text="C Initialiser:", bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL).grid(row=4, column=0, sticky="nw", padx=6, pady=(6,3))

        self._val_preview_var = tk.StringVar(value="{0x00}")
        preview_lbl = tk.Label(sep3, textvariable=self._val_preview_var,
            bg="#0d1117", fg=ACCENT_GREEN, font=("Courier New", 9),
            anchor="w", justify=tk.LEFT, relief="flat", bd=0,
            padx=6, pady=4, wraplength=220)
        preview_lbl.grid(row=4, column=1, sticky="ew", padx=6, pady=(6,3))

        # -- Validation / error row (row 5)
        self._val_err_var = tk.StringVar(value="")
        self._val_err_lbl = tk.Label(sep3, textvariable=self._val_err_var,
            bg=BG_PANEL, fg=ACCENT_RED, font=("Consolas", 8),
            anchor="w", justify=tk.LEFT, wraplength=280)
        self._val_err_lbl.grid(row=5, column=0, columnspan=2,
            sticky="w", padx=6, pady=(0, 4))

        # ── CCCD
        self._char_cccd_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(parent, text="Add CCCD Descriptor (required for Notify/Indicate)",
            variable=self._char_cccd_var,
            style="Dark.TCheckbutton").grid(
            row=10, column=0, columnspan=2, sticky="w", padx=12, pady=4)

        # ── Apply button
        apply_btn = tk.Label(parent, text="  ✓  Apply Changes  ",
            bg=ACCENT_GREEN, fg=BG_DARK, font=FONT_HEAD,
            padx=8, pady=6, cursor="hand2")
        apply_btn.grid(row=11, column=0, padx=12, pady=8, sticky="w")
        apply_btn.bind("<Button-1>", lambda e: self._apply_char_props())

        # Trigger initial preview
        self._on_value_changed()

    # ── Helpers: parse the initial value field and return (bytes_list, error_str)
    def _parse_init_value(self):
        """Return (list_of_int_bytes, error_string).  error_string is '' on success."""
        raw   = self._char_vinit_var.get().strip()
        fmt   = self._val_fmt_var.get()
        vtype = self._char_vtype_var.get()
        if not raw:
            return [0x00], ""

        try:
            if fmt == "hex":
                # Accept:  0xAB 0xCD  |  AB CD  |  ABCD  |  0xABCD  |  single 0xAB
                tokens = raw.replace(",", " ").split()
                result = []
                for t in tokens:
                    t = t.strip()
                    if t.lower().startswith("0x"):
                        t = t[2:]
                    if not t:
                        continue
                    # If token is longer than 2 hex digits, split into bytes
                    if len(t) % 2 != 0:
                        t = "0" + t
                    for i in range(0, len(t), 2):
                        result.append(int(t[i:i+2], 16))
                if not result:
                    result = [0x00]
                return result, ""

            elif fmt == "dec":
                # Comma or space-separated decimal integers
                tokens = raw.replace(",", " ").split()
                result = [int(t) for t in tokens if t]
                for v in result:
                    if not 0 <= v <= 255:
                        return [0x00], f"Decimal value {v} out of 0–255 range."
                return result or [0x00], ""

            elif fmt == "str":
                # UTF-8 encode the string
                return list(raw.encode("utf-8")), ""

            elif fmt == "bin":
                # Space or comma separated 0/1 groups, or a stream of 0s and 1s
                clean = raw.replace(",", " ").replace(" ", "")
                if not all(c in "01" for c in clean):
                    return [0x00], "Binary must contain only 0 and 1 digits."
                # Pad to multiple of 8
                if len(clean) % 8:
                    clean = clean.zfill((len(clean) // 8 + 1) * 8)
                result = [int(clean[i:i+8], 2) for i in range(0, len(clean), 8)]
                return result or [0x00], ""

        except (ValueError, OverflowError) as exc:
            return [0x00], str(exc)

        return [0x00], "Unknown format."

    def _on_value_changed(self, *_args):
        """Live-update the byte count, max-length spinner, C preview, and error label."""
        if not hasattr(self, "_char_vinit_var"):
            return
        byte_list, err = self._parse_init_value()
        n = len(byte_list)

        # Error label
        self._val_err_var.set(err)
        self._val_entry.config(bg="#3a1a1a" if err else BG_CARD)

        # Byte count badge
        self._val_bytelen_var.set(f"{n} byte{'s' if n != 1 else ''}")

        # Auto-update max length only if computed length > current setting
        try:
            cur_len = int(self._char_vlen_var.get())
        except (tk.TclError, ValueError):
            cur_len = 1
        if n > cur_len:
            self._char_vlen_var.set(n)
            self._len_auto_lbl.config(fg=ACCENT_AMBER)
        else:
            self._len_auto_lbl.config(fg=TEXT_MUTED)

        # C initialiser preview
        vtype = self._char_vtype_var.get()
        if err:
            self._val_preview_var.set("{  /* invalid input */  }")
            return

        if vtype == "float":
            preview = "/* set at runtime */"
        elif vtype == "double":
            preview = "/* set at runtime */"
        elif vtype in ("char[]", "uint8_t[]"):
            # Show as string-style for char[], hex bytes for uint8_t[]
            if vtype == "char[]":
                try:
                    s = bytes(byte_list).decode("utf-8", errors="replace")
                    preview = '"{}"'.format(s.replace('\\', '\\\\').replace('"', '\\"'))
                except Exception:
                    preview = "{" + ", ".join(f"0x{b:02X}" for b in byte_list) + "}"
            else:
                preview = "{" + ", ".join(f"0x{b:02X}" for b in byte_list) + "}"
        else:
            preview = "{" + ", ".join(f"0x{b:02X}" for b in byte_list) + "}"

        # Wrap long previews
        if len(preview) > 38:
            parts = preview.strip("{}").split(", ")
            rows  = []
            row   = []
            width = 0
            for p in parts:
                width += len(p) + 2
                row.append(p)
                if width >= 36:
                    rows.append(", ".join(row))
                    row, width = [], 0
            if row:
                rows.append(", ".join(row))
            preview = "{\n  " + ",\n  ".join(rows) + "\n}"

        self._val_preview_var.set(preview)

    def _on_prop_changed(self, *args):
        """Auto-set CCCD and auto-derive hidden permission vars from property checkboxes."""
        if not hasattr(self, "_prop_vars"):
            return
        # Auto CCCD
        if (self._prop_vars.get("notify") and self._prop_vars["notify"].get()) or \
           (self._prop_vars.get("indicate") and self._prop_vars["indicate"].get()):
            if hasattr(self, "_char_cccd_var"):
                self._char_cccd_var.set(True)

        # Auto-derive permissions: Read prop → Read perm, Write/Write-NR prop → Write perm
        if hasattr(self, "_perm_vars"):
            has_read  = self._prop_vars.get("read",  tk.BooleanVar()).get()
            has_write = (self._prop_vars.get("write",    tk.BooleanVar()).get() or
                         self._prop_vars.get("write_nr", tk.BooleanVar()).get())
            # Notify/Indicate need read permission on the CCCD descriptor (handled separately)
            # but the value attribute itself doesn't need write perm just for notify
            self._perm_vars["read"].set(has_read)
            self._perm_vars["write"].set(has_write)
            # Encrypted variants: keep whatever was saved, don't auto-touch them
            # (they are no longer shown in the UI, so we just leave them as-is)

    def _on_notify_changed(self, *args):
        # Kept for compatibility; real logic is now in _on_prop_changed
        self._on_prop_changed(*args)

    # ── Right Panel (BLE Settings + Code) ───────────────────
    def _build_right_panel(self, parent):
        nb = ttk.Notebook(parent, style="Dark.TNotebook")
        nb.pack(fill=tk.BOTH, expand=True)

        # Tab 1: BLE Advertise & Settings
        settings_frame = tk.Frame(nb, bg=BG_PANEL)
        self._build_settings_tab(settings_frame)
        nb.add(settings_frame, text="  BLE Settings  ")

        # Tab 2: Code Preview
        code_frame = tk.Frame(nb, bg=BG_DARK)
        self._build_code_tab(code_frame)
        nb.add(code_frame, text="  Code Preview  ")

    def _settings_row(self, parent, label, widget_fn, row):
        tk.Label(parent, text=label, bg=BG_PANEL, fg=TEXT_SEC,
            font=FONT_SMALL, anchor="w", width=22).grid(
            row=row, column=0, sticky="w", padx=(14,4), pady=(6,2))
        w = widget_fn(parent)
        w.grid(row=row, column=1, sticky="ew", padx=(0,14), pady=(6,2))
        return w

    def _build_settings_tab(self, parent):
        parent.columnconfigure(1, weight=1)

        tk.Label(parent, text="ADVERTISE SETTINGS", bg=BG_PANEL,
            fg=ACCENT_BLUE, font=FONT_SMALL).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14,8))

        cfg = self.config_data

        # Device name
        def make_entry(var, w=22):
            return lambda p: tk.Entry(p, textvariable=var, bg=BG_CARD,
                fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                relief="flat", bd=4, font=FONT_NORMAL, width=w)

        self._settings_row(parent, "Device Name", make_entry(cfg.device_name), 1)
        self._settings_row(parent, "Appearance (hex)", make_entry(cfg.appearance, 10), 2)

        tk.Label(parent, text="Adv Interval Min (×0.625ms)", bg=BG_PANEL,
            fg=TEXT_SEC, font=FONT_SMALL, anchor="w").grid(
            row=3, column=0, sticky="w", padx=(14,4), pady=(6,2))
        tk.Spinbox(parent, textvariable=cfg.adv_interval_min,
            from_=16, to=16000, increment=16,
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            buttonbackground=BG_CARD, relief="flat", font=FONT_NORMAL,
            width=10).grid(row=3, column=1, sticky="w", padx=(0,14), pady=(6,2))

        tk.Label(parent, text="Adv Interval Max (×0.625ms)", bg=BG_PANEL,
            fg=TEXT_SEC, font=FONT_SMALL, anchor="w").grid(
            row=4, column=0, sticky="w", padx=(14,4), pady=(6,2))
        tk.Spinbox(parent, textvariable=cfg.adv_interval_max,
            from_=16, to=16000, increment=16,
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            buttonbackground=BG_CARD, relief="flat", font=FONT_NORMAL,
            width=10).grid(row=4, column=1, sticky="w", padx=(0,14), pady=(6,2))

        tk.Frame(parent, bg=BORDER, height=1).grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=14, pady=8)

        tk.Label(parent, text="CONNECTION SETTINGS", bg=BG_PANEL,
            fg=ACCENT_BLUE, font=FONT_SMALL).grid(
            row=6, column=0, columnspan=2, sticky="w", padx=14, pady=(8,8))

        tk.Label(parent, text="MTU Size (bytes)", bg=BG_PANEL,
            fg=TEXT_SEC, font=FONT_SMALL, anchor="w").grid(
            row=7, column=0, sticky="w", padx=(14,4), pady=(6,2))
        tk.Spinbox(parent, textvariable=cfg.mtu,
            from_=23, to=517, increment=1,
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            buttonbackground=BG_CARD, relief="flat", font=FONT_NORMAL,
            width=10).grid(row=7, column=1, sticky="w", padx=(0,14), pady=(6,2))

        tk.Label(parent, text="TX Power Level", bg=BG_PANEL,
            fg=TEXT_SEC, font=FONT_SMALL, anchor="w").grid(
            row=8, column=0, sticky="w", padx=(14,4), pady=(6,2))
        power_levels = [
            "ESP_PWR_LVL_N12", "ESP_PWR_LVL_N9", "ESP_PWR_LVL_N6",
            "ESP_PWR_LVL_N3",  "ESP_PWR_LVL_N0", "ESP_PWR_LVL_P3",
            "ESP_PWR_LVL_P6",  "ESP_PWR_LVL_P9",
        ]
        ttk.Combobox(parent, textvariable=cfg.tx_power,
            values=power_levels, style="Dark.TCombobox",
            state="readonly", width=18).grid(
            row=8, column=1, sticky="w", padx=(0,14), pady=(6,2))

        tk.Label(parent, text="Security Mode", bg=BG_PANEL,
            fg=TEXT_SEC, font=FONT_SMALL, anchor="w").grid(
            row=9, column=0, sticky="w", padx=(14,4), pady=(6,2))
        sec_modes = ["None", "No Auth No Encrypt", "Auth No Encrypt",
                     "Auth With Encrypt", "Auth MITM Encrypt"]
        ttk.Combobox(parent, textvariable=cfg.security_mode,
            values=sec_modes, style="Dark.TCombobox",
            state="readonly", width=22).grid(
            row=9, column=1, sticky="w", padx=(0,14), pady=(6,2))

        tk.Frame(parent, bg=BORDER, height=1).grid(
            row=10, column=0, columnspan=2, sticky="ew", padx=14, pady=8)

        # Quick stats
        stats_frame = tk.LabelFrame(parent, text=" Profile Summary ",
            bg=BG_PANEL, fg=TEXT_SEC, font=FONT_SMALL,
            bd=1, relief="groove")
        stats_frame.grid(row=11, column=0, columnspan=2,
            sticky="ew", padx=14, pady=4)
        stats_frame.columnconfigure(1, weight=1)

        self._stat_services = tk.StringVar(value="0")
        self._stat_chars    = tk.StringVar(value="0")
        self._stat_handles  = tk.StringVar(value="0")

        for row, (label, var) in enumerate([
            ("Services:",        self._stat_services),
            ("Characteristics:", self._stat_chars),
            ("Est. Handles:",    self._stat_handles),
        ]):
            tk.Label(stats_frame, text=label, bg=BG_PANEL,
                fg=TEXT_SEC, font=FONT_SMALL).grid(
                row=row, column=0, sticky="w", padx=8, pady=2)
            tk.Label(stats_frame, textvariable=var, bg=BG_PANEL,
                fg=ACCENT_BLUE, font=FONT_HEAD).grid(
                row=row, column=1, sticky="w", padx=4, pady=2)

        # Generate button (big)
        gen = tk.Label(parent, text="⚙  Generate main.c",
            bg=ACCENT_AMBER, fg=BG_DARK, font=("Consolas", 12, "bold"),
            padx=12, pady=10, cursor="hand2")
        gen.grid(row=12, column=0, columnspan=2,
            sticky="ew", padx=14, pady=12)
        gen.bind("<Button-1>", lambda e: self._generate_code())
        gen.bind("<Enter>", lambda e: gen.config(bg="#d4901f"))
        gen.bind("<Leave>", lambda e: gen.config(bg=ACCENT_AMBER))

    def _build_code_tab(self, parent):
        toolbar = tk.Frame(parent, bg=BG_PANEL)
        toolbar.pack(fill=tk.X)
        tk.Label(toolbar, text="Generated Code", bg=BG_PANEL,
            fg=ACCENT_AMBER, font=FONT_HEAD, padx=12).pack(side=tk.LEFT, pady=6)

        def copy_code():
            self.clipboard_clear()
            self.clipboard_append(self.code_text.get("1.0", tk.END))
            self._status("Code copied to clipboard!")

        self._mini_btn(toolbar, "📋 Copy",  ACCENT_BLUE,  copy_code).pack(side=tk.RIGHT, padx=6, pady=6)
        self._mini_btn(toolbar, "💾 Save",  ACCENT_GREEN, self._save_code_file).pack(side=tk.RIGHT, pady=6)
        self._mini_btn(toolbar, "⚙ Generate", ACCENT_AMBER, self._generate_code).pack(side=tk.RIGHT, padx=6, pady=6)

        # Code editor
        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(frame, orient="vertical",
            style="Dark.Vertical.TScrollbar")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = ttk.Scrollbar(frame, orient="horizontal",
            style="Dark.Horizontal.TScrollbar")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.code_text = tk.Text(frame, bg="#0d1117", fg="#c9d1d9",
            insertbackground=TEXT_PRIMARY, font=FONT_MONO,
            wrap=tk.NONE, bd=0, relief="flat",
            yscrollcommand=vsb.set, xscrollcommand=hsb.set,
            padx=12, pady=8, selectbackground="#264f78")
        self.code_text.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=self.code_text.yview)
        hsb.config(command=self.code_text.xview)

        self.code_text.insert("1.0", "// Press ⚙ Generate to create your ESP-IDF BLE main.c\n")

        # Syntax-highlighting tags
        self.code_text.tag_configure("kw",      foreground="#ff7b72")
        self.code_text.tag_configure("comment",  foreground="#6a737d")
        self.code_text.tag_configure("string",   foreground="#a5d6ff")
        self.code_text.tag_configure("number",   foreground="#79c0ff")
        self.code_text.tag_configure("preproc",  foreground="#d2a8ff")
        self.code_text.tag_configure("func",     foreground="#d2a8ff")
        self.code_text.tag_configure("type",     foreground="#ffa657")

    # ── Status Bar ───────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg=BG_PANEL, height=26)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        self._status_var = tk.StringVar(value="Ready — Add services to get started")
        tk.Label(bar, textvariable=self._status_var,
            bg=BG_PANEL, fg=TEXT_SEC, font=FONT_SMALL,
            anchor="w", padx=10).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(bar, text=f"ESP-IDF BLE Configurator v1.0  |  {datetime.now().year}",
            bg=BG_PANEL, fg=TEXT_MUTED, font=FONT_SMALL,
            padx=10).pack(side=tk.RIGHT, fill=tk.Y)

    def _status(self, msg):
        self._status_var.set(msg)
        if hasattr(self, "_status_after_id") and self._status_after_id:
            self.after_cancel(self._status_after_id)   # BUG FIX: cancel stale timer
        self._status_after_id = self.after(5000, lambda: self._status_var.set("Ready"))

    def _selected_iid(self):
        if not self.selected_node:
            return None
        if self.selected_node[0] == "service":
            return f"svc_{self.selected_node[1]}"
        if self.selected_node[0] == "char":
            return f"svc_{self.selected_node[1]}_char_{self.selected_node[2]}"
        return None

    def _clear_selection(self):
        self.selected_node = None
        self._show_props_panel("empty")
        self.props_title.config(text="Properties")
        if hasattr(self, "tree"):
            selection = self.tree.selection()
            if selection:
                self.tree.selection_remove(*selection)

    # ── Tree Refresh ─────────────────────────────────────────
    def _refresh_tree(self):
        # Save open state
        open_items = {iid for iid in self.tree.get_children("") if self.tree.item(iid, "open")}
        selected_iid = self._selected_iid()

        self.tree.delete(*self.tree.get_children())
        svc_count  = len(self.config_data.services)
        char_count = sum(len(s.characteristics) for s in self.config_data.services)
        handle_est = sum(
            1 + 2 * len(s.characteristics) +
            sum(1 for ch in s.characteristics if ch.has_cccd.get())
            for s in self.config_data.services
        )

        for si, svc in enumerate(self.config_data.services):
            ptype = "Primary" if svc.primary.get() else "Secondary"
            short_uuid = svc.uuid[:8] + "…" if len(svc.uuid) > 8 else svc.uuid
            iid = self.tree.insert("", "end",
                iid=f"svc_{si}",
                text=f"  ⬡  {svc.name}",
                values=(short_uuid, ptype),
                tags=("service",), open=f"svc_{si}" in open_items)

            for ci, ch in enumerate(svc.characteristics):
                props = []
                if ch.prop_read.get():     props.append("R")
                if ch.prop_write.get():    props.append("W")
                if ch.prop_write_nr.get(): props.append("WN")
                if ch.prop_notify.get():   props.append("N")
                if ch.prop_indicate.get(): props.append("I")
                pstr = "/".join(props) if props else "—"
                short_cuuid = ch.uuid[:8] + "…" if len(ch.uuid) > 8 else ch.uuid
                self.tree.insert(iid, "end",
                    iid=f"svc_{si}_char_{ci}",
                    text=f"    ◈  {ch.name}",
                    values=(short_cuuid, pstr),
                    tags=("char",))
                if ch.has_cccd.get():
                    self.tree.insert(f"svc_{si}_char_{ci}", "end",
                        iid=f"svc_{si}_char_{ci}_cccd",
                        text="       ▸  CCCD",
                        values=("0x2902", "Desc"),
                        tags=("cccd",))

        self._stat_services.set(str(svc_count))
        self._stat_chars.set(str(char_count))
        self._stat_handles.set(str(handle_est))
        if selected_iid and self.tree.exists(selected_iid):
            self.tree.selection_set(selected_iid)
            self.tree.focus(selected_iid)
            self.tree.see(selected_iid)

    # ── Tree Events ──────────────────────────────────────────
    def _on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        self._load_props_for(iid)

    def _on_tree_double(self, event):
        sel = self.tree.selection()
        if sel:
            self._rename_selected()

    def _load_props_for(self, iid):
        if iid.endswith("_cccd"):
            parent = self.tree.parent(iid)
            if parent:
                self.tree.selection_set(parent)
                iid = parent
        if iid.startswith("svc_") and "_char_" not in iid:
            try:
                si = int(iid.split("_")[1])
                svc = self.config_data.services[si]
            except (ValueError, IndexError):
                self._clear_selection()
                return
            self.selected_node = ("service", si)
            self._svc_name_var.set(svc.name)
            self._svc_uuid_var.set(svc.uuid)
            self._svc_primary_var.set(svc.primary.get())
            self._show_props_panel("service")
            self.props_title.config(text=f"Service: {svc.name}")

        elif "_char_" in iid and "cccd" not in iid:
            parts = iid.split("_")
            try:
                si = int(parts[1])
                ci = int(parts[3])
                ch = self.config_data.services[si].characteristics[ci]
            except (ValueError, IndexError):
                self._clear_selection()
                return
            self.selected_node = ("char", si, ci)
            self._char_name_var.set(ch.name)
            self._char_uuid_var.set(ch.uuid)
            self._char_desc_var.set(ch.description.get())
            for key, var in self._prop_vars.items():
                src = getattr(ch, f"prop_{key}", None)
                if src is not None:
                    var.set(src.get())
            for key, var in self._perm_vars.items():
                src = getattr(ch, f"perm_{key}", None)
                if src is not None:
                    var.set(src.get())
            self._char_vtype_var.set(ch.value_type.get())
            self._char_vlen_var.set(ch.value_len.get())
            # Saved values are always in canonical hex form — set format accordingly
            self._val_fmt_var.set("hex")
            self._char_vinit_var.set(ch.init_value.get())
            self._char_cccd_var.set(ch.has_cccd.get())
            # Trigger live preview so byte count, C preview etc. are correct immediately
            self._on_value_changed()
            self._show_props_panel("char")
            self.props_title.config(text=f"Char: {ch.name}")
        else:
            self._clear_selection()

    def _apply_service_props(self):
        if not self.selected_node or self.selected_node[0] != "service":
            return
        si  = self.selected_node[1]
        svc = self.config_data.services[si]
        new_uuid = self._svc_uuid_var.get().strip()
        # BUG FIX: validate UUID on Apply, not only at code-gen time
        compact = new_uuid.replace("-", "").replace("0x", "").replace("{", "").replace("}", "").upper()
        if compact and len(compact) not in (4, 8, 32) or not all(c in "0123456789ABCDEF" for c in compact):
            messagebox.showerror("Invalid UUID",
                "Service UUID must be a 16-bit (4 hex), 32-bit (8 hex), or 128-bit (32 hex) BLE UUID.")
            return
        svc.name = self._svc_name_var.get()
        svc.uuid = new_uuid
        svc.primary.set(self._svc_primary_var.get())
        self._refresh_tree()
        self._status(f"Service '{svc.name}' updated.")

    def _apply_char_props(self):
        if not self.selected_node or self.selected_node[0] != "char":
            return
        si, ci = self.selected_node[1], self.selected_node[2]
        ch = self.config_data.services[si].characteristics[ci]

        # Validate value via the live parser
        byte_list, err = self._parse_init_value()
        if err:
            messagebox.showerror("Invalid Initial Value",
                f"Could not parse the initial value:\n{err}")
            return

        # Validate max length
        try:
            value_len = int(self._char_vlen_var.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Invalid Value Length",
                "Max Len must be a whole number between 1 and 512.")
            return
        if not 1 <= value_len <= 512:
            messagebox.showerror("Invalid Value Length",
                "Max Len must be between 1 and 512 bytes.")
            return
        if len(byte_list) > value_len:
            messagebox.showerror("Value Too Long",
                f"Initial value is {len(byte_list)} bytes but Max Length is {value_len}.\n"
                "Increase Max Length or shorten the initial value.")
            return

        # Apply name / uuid / description
        ch.name = self._char_name_var.get()
        ch.uuid = self._char_uuid_var.get()
        ch.description.set(self._char_desc_var.get())

        # Apply properties
        for key, var in self._prop_vars.items():
            getattr(ch, f"prop_{key}").set(var.get())

        # Apply auto-derived permissions (already computed by _on_prop_changed)
        for key, var in self._perm_vars.items():
            getattr(ch, f"perm_{key}").set(var.get())

        # Store init value as canonical hex tokens regardless of input format
        ch.value_type.set(self._char_vtype_var.get())
        ch.value_len.set(value_len)
        canonical = ", ".join(f"0x{b:02X}" for b in byte_list)
        ch.init_value.set(canonical)
        # Update the entry to show the canonical form too
        self._char_vinit_var.set(canonical)
        self._val_fmt_var.set("hex")

        ch.has_cccd.set(self._char_cccd_var.get())
        self._refresh_tree()
        self._status(f"Characteristic '{ch.name}' updated.")

    # ── Add / Delete ─────────────────────────────────────────
    def _add_service_dialog(self):
        dlg = _AddDialog(self, "Add BLE Service",
            list(STANDARD_SERVICES.keys()), "service")
        self.wait_window(dlg)
        if dlg.result:
            name, uuid_key = dlg.result
            uuid_val = STANDARD_SERVICES.get(uuid_key, uuid_key)
            svc = BLEService(name, uuid_val)
            self.config_data.services.append(svc)
            self._refresh_tree()
            self._status(f"Service '{name}' added.")

    def _add_char_dialog(self):
        # Find target service
        si = None
        if self.selected_node:
            if self.selected_node[0] == "service":
                si = self.selected_node[1]
            elif self.selected_node[0] == "char":
                si = self.selected_node[1]
        if si is None:
            if self.config_data.services:
                si = 0
            else:
                messagebox.showwarning("No Service",
                    "Please add a service first before adding characteristics.")
                return

        dlg = _AddDialog(self, "Add Characteristic",
            list(STANDARD_CHARACTERISTICS.keys()), "characteristic")
        self.wait_window(dlg)
        if dlg.result:
            name, uuid_key = dlg.result
            uuid_val = STANDARD_CHARACTERISTICS.get(uuid_key, uuid_key)
            ch = BLECharacteristic(name, uuid_val)
            self.config_data.services[si].characteristics.append(ch)
            self._refresh_tree()
            self._status(f"Characteristic '{name}' added to '{self.config_data.services[si].name}'.")

    def _delete_selected(self):
        if not self.selected_node:
            return
        if self.selected_node[0] == "service":
            si = self.selected_node[1]
            name = self.config_data.services[si].name
            if messagebox.askyesno("Delete Service",
                    f"Delete service '{name}' and all its characteristics?"):
                del self.config_data.services[si]
                self._clear_selection()
                self._refresh_tree()
                self._status(f"Service '{name}' deleted.")
        elif self.selected_node[0] == "char":
            si, ci = self.selected_node[1], self.selected_node[2]
            name = self.config_data.services[si].characteristics[ci].name
            if messagebox.askyesno("Delete Characteristic",
                    f"Delete characteristic '{name}'?"):
                del self.config_data.services[si].characteristics[ci]
                self._clear_selection()
                self._refresh_tree()
                self._status(f"Characteristic '{name}' deleted.")

    def _rename_selected(self):
        if not self.selected_node:
            return
        if self.selected_node[0] == "service":
            svc = self.config_data.services[self.selected_node[1]]
            dlg = _RenameDialog(self, "Rename Service", svc.name)
            self.wait_window(dlg)
            if dlg.result:
                svc.name = dlg.result
                self._refresh_tree()
        elif self.selected_node[0] == "char":
            si, ci = self.selected_node[1], self.selected_node[2]
            ch = self.config_data.services[si].characteristics[ci]
            dlg = _RenameDialog(self, "Rename Characteristic", ch.name)
            self.wait_window(dlg)
            if dlg.result:
                ch.name = dlg.result
                self._refresh_tree()

    def _move_up(self):
        if not self.selected_node:
            return
        if self.selected_node[0] == "service":
            si = self.selected_node[1]
            if si > 0:
                svcs = self.config_data.services
                svcs[si-1], svcs[si] = svcs[si], svcs[si-1]
                self.selected_node = ("service", si-1)
                self._refresh_tree()
        elif self.selected_node[0] == "char":
            si, ci = self.selected_node[1], self.selected_node[2]
            chars = self.config_data.services[si].characteristics
            if ci > 0:
                chars[ci-1], chars[ci] = chars[ci], chars[ci-1]
                self.selected_node = ("char", si, ci-1)
                self._refresh_tree()

    def _move_down(self):
        if not self.selected_node:
            return
        if self.selected_node[0] == "service":
            si = self.selected_node[1]
            svcs = self.config_data.services
            if si < len(svcs)-1:
                svcs[si+1], svcs[si] = svcs[si], svcs[si+1]
                self.selected_node = ("service", si+1)
                self._refresh_tree()
        elif self.selected_node[0] == "char":
            si, ci = self.selected_node[1], self.selected_node[2]
            chars = self.config_data.services[si].characteristics
            if ci < len(chars)-1:
                chars[ci+1], chars[ci] = chars[ci], chars[ci+1]
                self.selected_node = ("char", si, ci+1)
                self._refresh_tree()

    # ── Drag & Drop ──────────────────────────────────────────
    def _drag_start(self, event):
        item = self.tree.identify_row(event.y)
        if item.endswith("_cccd"):
            item = self.tree.parent(item)
        self._drag_item = item
        self._drag_start_y = event.y

    def _drag_motion(self, event):
        if not self._drag_item:
            return
        target = self.tree.identify_row(event.y)
        if target and target != self._drag_item:
            self.tree.selection_set(target)

    def _drag_release(self, event):
        if not self._drag_item:
            return
        target = self.tree.identify_row(event.y)
        if not target:                          # BUG FIX: empty string when clicking blank area
            self._drag_item = None
            return
        if target.endswith("_cccd"):
            target = self.tree.parent(target)
        if target and target != self._drag_item:
            self._do_drag_drop(self._drag_item, target)
        self._drag_item = None

    def _do_drag_drop(self, src, dst):
        # Only support char reorder within same service
        if "_char_" in src and "_char_" in dst:
            s1 = int(src.split("_")[1])
            s2 = int(dst.split("_")[1])
            c1 = int(src.split("_")[3])
            c2 = int(dst.split("_")[3])
            if s1 == s2:
                chars = self.config_data.services[s1].characteristics
                chars.insert(c2, chars.pop(c1))
                self.selected_node = ("char", s1, c2)
                self._refresh_tree()
        elif src.startswith("svc_") and "_char_" not in src and \
             dst.startswith("svc_") and "_char_" not in dst:
            i1 = int(src.split("_")[1])
            i2 = int(dst.split("_")[1])
            svcs = self.config_data.services
            svcs.insert(i2, svcs.pop(i1))
            self.selected_node = ("service", i2)
            self._refresh_tree()

    # ── Context Menu ─────────────────────────────────────────
    def _show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._load_props_for(item)
            self.context_menu.entryconfigure("Rename", state="normal")
            self.context_menu.entryconfigure("Delete", state="normal")
        else:
            self._clear_selection()
            self.context_menu.entryconfigure("Rename", state="disabled")
            self.context_menu.entryconfigure("Delete", state="disabled")
        self.context_menu.post(event.x_root, event.y_root)

    # ── Save / Load Config ───────────────────────────────────
    def _save_config(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("BLE Config", "*.json"), ("All", "*.*")],
            title="Save BLE Configuration")
        if not path:
            return
        data = {
            "device_name":      self.config_data.device_name.get(),
            "adv_interval_min": self.config_data.adv_interval_min.get(),
            "adv_interval_max": self.config_data.adv_interval_max.get(),
            "tx_power":         self.config_data.tx_power.get(),
            "appearance":       self.config_data.appearance.get(),
            "mtu":              self.config_data.mtu.get(),
            "security_mode":    self.config_data.security_mode.get(),
            "services": []
        }
        for svc in self.config_data.services:
            sd = {
                "name": svc.name, "uuid": svc.uuid,
                "primary": svc.primary.get(),
                "characteristics": []
            }
            for ch in svc.characteristics:
                cd = {
                    "name": ch.name, "uuid": ch.uuid,
                    "description": ch.description.get(),
                    "prop_read":     ch.prop_read.get(),
                    "prop_write":    ch.prop_write.get(),
                    "prop_write_nr": ch.prop_write_nr.get(),
                    "prop_notify":   ch.prop_notify.get(),
                    "prop_indicate": ch.prop_indicate.get(),
                    "prop_broadcast":ch.prop_broadcast.get(),
                    "perm_read":     ch.perm_read.get(),
                    "perm_write":    ch.perm_write.get(),
                    "perm_read_enc": ch.perm_read_enc.get(),
                    "perm_write_enc":ch.perm_write_enc.get(),
                    "value_type":    ch.value_type.get(),
                    "value_len":     ch.value_len.get(),
                    "init_value":    ch.init_value.get(),
                    "has_cccd":      ch.has_cccd.get(),
                }
                sd["characteristics"].append(cd)
            data["services"].append(sd)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as exc:
            messagebox.showerror("Save Failed", f"Could not save configuration:\n{exc}")
            return
        self._status(f"Config saved to {path}")

    def _load_config(self):
        path = filedialog.askopenfilename(
            filetypes=[("BLE Config", "*.json"), ("All", "*.*")],
            title="Load BLE Configuration")
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Load Failed", f"Could not load configuration:\n{exc}")
            return
        if not isinstance(data, dict):
            messagebox.showerror("Load Failed", "Configuration file must contain a JSON object.")
            return
        services_data = data.get("services", [])
        if not isinstance(services_data, list):
            messagebox.showerror("Load Failed", "Configuration services must be a list.")
            return
        cfg = self.config_data
        try:
            new_services = []
            for sd in services_data:
                if not isinstance(sd, dict):
                    raise TypeError("Each service must be a JSON object.")
                svc = BLEService(sd.get("name", "New Service"), sd.get("uuid", "CUSTOM"))
                svc.primary.set(sd.get("primary", True))
                chars_data = sd.get("characteristics", [])
                if not isinstance(chars_data, list):
                    raise TypeError("Service characteristics must be a list.")
                for cd in chars_data:
                    if not isinstance(cd, dict):
                        raise TypeError("Each characteristic must be a JSON object.")
                    ch = BLECharacteristic(cd.get("name", "New Characteristic"), cd.get("uuid", "CUSTOM"))
                    ch.description.set(cd.get("description", ""))
                    ch.prop_read.set(cd.get("prop_read", False))
                    ch.prop_write.set(cd.get("prop_write", False))
                    ch.prop_write_nr.set(cd.get("prop_write_nr", False))
                    ch.prop_notify.set(cd.get("prop_notify", False))
                    ch.prop_indicate.set(cd.get("prop_indicate", False))
                    ch.prop_broadcast.set(cd.get("prop_broadcast", False))
                    ch.perm_read.set(cd.get("perm_read", False))
                    ch.perm_write.set(cd.get("perm_write", False))
                    ch.perm_read_enc.set(cd.get("perm_read_enc", False))
                    ch.perm_write_enc.set(cd.get("perm_write_enc", False))
                    ch.value_type.set(cd.get("value_type", "uint8_t"))
                    ch.value_len.set(cd.get("value_len", 1))
                    ch.init_value.set(cd.get("init_value", "0x00"))
                    ch.has_cccd.set(cd.get("has_cccd", False))
                    svc.characteristics.append(ch)
                new_services.append(svc)

            cfg.device_name.set(data.get("device_name", "ESP32_BLE"))
            cfg.adv_interval_min.set(data.get("adv_interval_min", 160))
            cfg.adv_interval_max.set(data.get("adv_interval_max", 320))
            cfg.tx_power.set(data.get("tx_power", "ESP_PWR_LVL_P9"))
            cfg.appearance.set(data.get("appearance", "0x0000"))
            cfg.mtu.set(data.get("mtu", 500))
            cfg.security_mode.set(data.get("security_mode", "None"))
            cfg.services = new_services
        except (AttributeError, TypeError, tk.TclError) as exc:
            messagebox.showerror("Load Failed", f"Configuration file is not valid:\n{exc}")
            return
        self._clear_selection()
        self._refresh_tree()
        self._status(f"Config loaded from {path}")

    # ── Code Generation ──────────────────────────────────────
    def _generate_code(self):
        try:
            code = self._build_c_code()
        except ValueError as exc:
            messagebox.showerror("Invalid Configuration", str(exc))
            return
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", code)
        self._highlight_code()
        self._status("Code generated successfully!")
        # Switch to code tab
        # (find the notebook with code preview)
        for widget in self.winfo_children():
            if isinstance(widget, tk.PanedWindow):
                for pane in widget.panes():
                    for child in widget.nametowidget(pane).winfo_children():
                        if isinstance(child, ttk.Notebook):
                            child.select(1)

    def _highlight_code(self):
        code = self.code_text.get("1.0", tk.END)
        for tag in ("kw", "comment", "string", "number", "preproc", "func", "type"):
            self.code_text.tag_remove(tag, "1.0", tk.END)
        keywords = r'\b(if|else|for|while|do|switch|case|break|return|void|static|const|extern|struct|typedef|enum|sizeof|NULL|true|false|uint8_t|uint16_t|uint32_t|int|char|unsigned|include|define|endif|ifdef|ifndef)\b'
        preproc  = r'(#\w+)'
        comments = r'(//[^\n]*|/\*.*?\*/)'
        strings  = r'(".*?")'
        numbers  = r'\b(0x[0-9a-fA-F]+|\d+)\b'
        funcs    = r'\b([a-z_][a-z0-9_]*)\s*\('

        for pattern, tag, flags in [
            (comments, "comment", re.DOTALL),
            (strings,  "string",  0),
            (preproc,  "preproc", 0),
            (keywords, "kw",      0),
            (numbers,  "number",  0),
            (funcs,    "func",    0),
        ]:
            for m in re.finditer(pattern, code, flags):
                start = f"1.0 + {m.start()} chars"
                end   = f"1.0 + {m.end()} chars"
                self.code_text.tag_add(tag, start, end)

    def _save_code_file(self):
        code = self.code_text.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(
            defaultextension=".c",
            initialfile="main.c",
            filetypes=[("C Source", "*.c"), ("All", "*.*")],
            title="Save main.c")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(code)
            except OSError as exc:
                messagebox.showerror("Save Failed", f"Could not save code:\n{exc}")
                return
            self._status(f"Saved to {path}")

    # ─────────────────────────────────────────────────────────
    #  C CODE GENERATOR
    # ─────────────────────────────────────────────────────────
    def _build_c_code(self):
        cfg = self.config_data
        svcs = cfg.services
        if not svcs:
            raise ValueError("Add at least one service before generating main.c.")

        def get_text(var, default=""):
            value = var.get() if hasattr(var, "get") else var
            value = str(value).strip()
            return value or default

        def get_int(var, label, min_value=None, max_value=None):
            try:
                value = int(var.get() if hasattr(var, "get") else var)
            except (tk.TclError, TypeError, ValueError):
                raise ValueError(f"{label} must be a whole number.")
            if min_value is not None and value < min_value:
                raise ValueError(f"{label} must be at least {min_value}.")
            if max_value is not None and value > max_value:
                raise ValueError(f"{label} must be no more than {max_value}.")
            return value

        def hex_u16(value, label):
            text = str(value).strip()
            if text.lower().startswith("0x"):
                text = text[2:]
            if not re.fullmatch(r"[0-9a-fA-F]{1,4}", text):
                raise ValueError(f"{label} must be a 16-bit hex value, for example 0x0000.")
            return f"0x{int(text, 16):04X}"

        def c_string(value):
            return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

        def c_comment(value):
            return str(value).replace("/*", "/ *").replace("*/", "* /").replace("\n", " ")

        def to_c_ident(value, fallback):
            ident = re.sub(r"\W+", "_", str(value).strip()).strip("_").upper()
            if not ident:
                ident = fallback
            if ident[0].isdigit():
                ident = f"{fallback}_{ident}"
            return ident

        def unique_ident(base, used):
            ident = base
            suffix = 2
            while ident in used:
                ident = f"{base}_{suffix}"
                suffix += 1
            used.add(ident)
            return ident

        def compact_uuid(value, label):
            text = str(value).strip().strip("{}")
            if text.lower().startswith("0x"):
                text = text[2:]
            compact = text.replace("-", "").upper()
            if not re.fullmatch(r"[0-9A-F]+", compact or "") or len(compact) not in (4, 8, 32):
                raise ValueError(
                    f"{label} must be a 16-bit, 32-bit, or 128-bit BLE UUID "
                    "(4, 8, or 32 hex digits)."
                )
            return compact

        def uuid_info(raw_uuid, label, var_name):
            compact = compact_uuid(raw_uuid, label)
            if len(compact) == 4:
                return {
                    "decl": f"static const uint16_t {var_name} = 0x{compact};",
                    "len": "ESP_UUID_LEN_16",
                    "size": f"sizeof({var_name})",
                    "ptr": f"(uint8_t *)&{var_name}",
                }
            if len(compact) == 8:
                return {
                    "decl": f"static const uint32_t {var_name} = 0x{compact};",
                    "len": "ESP_UUID_LEN_32",
                    "size": f"sizeof({var_name})",
                    "ptr": f"(uint8_t *)&{var_name}",
                }
            pairs = [f"0x{compact[i:i+2]}" for i in range(30, -1, -2)]
            return {
                "decl": f"static const uint8_t {var_name}[16] = {{{', '.join(pairs)}}};",
                "len": "ESP_UUID_LEN_128",
                "size": f"sizeof({var_name})",
                "ptr": f"(uint8_t *){var_name}",
            }

        def props_macro(ch):
            props = []
            if ch.prop_broadcast.get(): props.append("ESP_GATT_CHAR_PROP_BIT_BROADCAST")
            if ch.prop_read.get():      props.append("ESP_GATT_CHAR_PROP_BIT_READ")
            if ch.prop_write_nr.get():  props.append("ESP_GATT_CHAR_PROP_BIT_WRITE_NR")
            if ch.prop_write.get():     props.append("ESP_GATT_CHAR_PROP_BIT_WRITE")
            if ch.prop_notify.get():    props.append("ESP_GATT_CHAR_PROP_BIT_NOTIFY")
            if ch.prop_indicate.get():  props.append("ESP_GATT_CHAR_PROP_BIT_INDICATE")
            return " | ".join(props) if props else "0"

        def perms_macro(ch):
            # Permissions are auto-derived from properties (no manual permission UI)
            perms = []
            if ch.prop_read.get():
                perms.append("ESP_GATT_PERM_READ")
            if ch.prop_write.get() or ch.prop_write_nr.get():
                perms.append("ESP_GATT_PERM_WRITE")
            # Encrypted variants are still respected if set programmatically or via config load
            if ch.perm_read_enc.get():
                perms.append("ESP_GATT_PERM_READ_ENCRYPTED")
            if ch.perm_write_enc.get():
                perms.append("ESP_GATT_PERM_WRITE_ENCRYPTED")
            return " | ".join(perms) if perms else "ESP_GATT_PERM_READ"

        dname = get_text(cfg.device_name, "ESP32_BLE")
        adv_min = get_int(cfg.adv_interval_min, "Advertising minimum interval", 16, 16000)
        adv_max = get_int(cfg.adv_interval_max, "Advertising maximum interval", 16, 16000)
        if adv_min > adv_max:
            raise ValueError("Advertising minimum interval cannot be greater than the maximum interval.")
        mtu = get_int(cfg.mtu, "MTU size", 23, 517)
        tx_pwr = get_text(cfg.tx_power, "ESP_PWR_LVL_P9")
        if not re.fullmatch(r"ESP_PWR_LVL_[A-Z0-9_]+", tx_pwr):
            raise ValueError("TX power level is not a valid ESP_PWR_LVL_* constant.")
        appearance = hex_u16(cfg.appearance.get(), "Appearance")

        svc_meta = []
        used_services = set()
        for si, svc in enumerate(svcs):
            svc_id = unique_ident(to_c_ident(svc.name, f"SVC_{si + 1}"), used_services)
            svc_var = f"{svc_id.lower()}_svc_uuid"
            meta = {
                "svc": svc,
                "id": svc_id,
                "uuid": uuid_info(svc.uuid, f"Service '{svc.name}' UUID", svc_var),
                "chars": [],
            }
            used_chars = set()
            for ci, ch in enumerate(svc.characteristics):
                ch_id = unique_ident(to_c_ident(ch.name, f"CHAR_{ci + 1}"), used_chars)
                ch_var = f"{svc_id.lower()}_{ch_id.lower()}_uuid"
                meta["chars"].append({
                    "ch": ch,
                    "id": ch_id,
                    "uuid": uuid_info(ch.uuid, f"Characteristic '{ch.name}' UUID", ch_var),
                    "value_len": get_int(ch.value_len, f"Characteristic '{ch.name}' max length", 1, 512),
                })
            svc_meta.append(meta)

        lines = []
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines += [
            "/*",
            " * ESP-IDF BLE GATT Server - Auto-generated by ESP BLE GATT Configurator",
            f" * Generated: {ts}",
            f" * Device Name: {c_comment(dname)}",
            " *",
            " * HOW TO USE:",
            " *   1. Copy this file to your ESP-IDF project's main/main.c",
            " *   2. Ensure your CMakeLists.txt lists main.c",
            " *   3. Add 'CONFIG_BT_ENABLED=y' to sdkconfig or via 'idf.py menuconfig'",
            " *   4. Run 'idf.py build flash monitor'",
            " */",
            "",
            "#include <stdbool.h>",
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <string.h>",
            "#include \"freertos/FreeRTOS.h\"",
            "#include \"freertos/task.h\"",
            "#include \"freertos/event_groups.h\"",
            "#include \"esp_system.h\"",
            "#include \"esp_err.h\"",
            "#include \"esp_log.h\"",
            "#include \"nvs_flash.h\"",
            "#include \"esp_bt.h\"",
            "#include \"esp_gap_ble_api.h\"",
            "#include \"esp_gatts_api.h\"",
            "#include \"esp_bt_main.h\"",
            "#include \"esp_gatt_common_api.h\"",
            "",
            f"#define TAG \"{c_string(dname)}\"",
            "#define PROFILE_NUM  1",
            "#define PROFILE_APP_IDX 0",
            "#define APP_ID       0x55",
            f"#define DEVICE_NAME  \"{c_string(dname)}\"",
            "#define SVC_INST_ID  0",
            "#define CHAR_DECLARATION_SIZE (sizeof(uint8_t))",
            "",
        ]

        lines.append("/* GATT handle indices */")
        lines.append("enum {")
        for svc_item in svc_meta:
            svc_id = svc_item["id"]
            lines.append(f"    IDX_SVC_{svc_id},")
            for char_item in svc_item["chars"]:
                ch_id = char_item["id"]
                lines.append(f"    IDX_{svc_id}_{ch_id}_DECL,")
                lines.append(f"    IDX_{svc_id}_{ch_id}_VAL,")
                if char_item["ch"].has_cccd.get():
                    lines.append(f"    IDX_{svc_id}_{ch_id}_CFG,")
        lines.append("    IDX_NB,")
        lines.append("};")
        lines.append("")
        lines.append("static uint16_t ble_handle_table[IDX_NB];")
        lines.append("")

        # Determine which standard UUIDs are actually needed to avoid
        # -Werror=unused-const-variable= compile errors in ESP-IDF.
        has_secondary_svc = any(not sm["svc"].primary.get() for sm in svc_meta)
        has_any_cccd = any(
            cm["ch"].has_cccd.get()
            for sm in svc_meta
            for cm in sm["chars"]
        )

        std_uuid_lines = [
            "/* Standard GATT UUIDs */",
            "static const uint16_t primary_service_uuid       = ESP_GATT_UUID_PRI_SERVICE;",
        ]
        if has_secondary_svc:
            std_uuid_lines.append(
                "static const uint16_t secondary_service_uuid     = ESP_GATT_UUID_SEC_SERVICE;"
            )
        std_uuid_lines.append(
            "static const uint16_t character_declaration_uuid = ESP_GATT_UUID_CHAR_DECLARE;"
        )
        if has_any_cccd:
            std_uuid_lines.append(
                "static const uint16_t character_client_config_uuid = ESP_GATT_UUID_CHAR_CLIENT_CONFIG;"
            )
        std_uuid_lines += ["", "/* Service and characteristic UUID values */"]
        lines += std_uuid_lines
        for svc_item in svc_meta:
            lines.append(svc_item["uuid"]["decl"])
            for char_item in svc_item["chars"]:
                lines.append(char_item["uuid"]["decl"])
        lines.append("")

        lines.append("/* Characteristic property bytes */")
        for svc_item in svc_meta:
            svc_id_l = svc_item["id"].lower()
            for char_item in svc_item["chars"]:
                ch = char_item["ch"]
                ch_id_l = char_item["id"].lower()
                lines.append(
                    f"static const uint8_t char_prop_{svc_id_l}_{ch_id_l} = {props_macro(ch)};"
                )
        lines.append("")

        lines.append("/* Characteristic value storage */")
        for svc_item in svc_meta:
            svc_id_l = svc_item["id"].lower()
            for char_item in svc_item["chars"]:
                ch = char_item["ch"]
                ch_id_l = char_item["id"].lower()
                init_raw = str(ch.init_value.get()).strip().replace("\n", " ") or "0x00"
                # BUG FIX: sanitise init_value — only allow hex/decimal numbers and commas/spaces
                import re as _re
                if not _re.fullmatch(r'[\s,0-9xa-fA-FxX\+\-]+', init_raw):
                    init_raw = "0x00"   # fall back to safe default if arbitrary text detected
                # Ensure at least one value token
                init = init_raw if init_raw.strip() else "0x00"
                vlen = char_item["value_len"]
                lines.append(f"static uint8_t {svc_id_l}_{ch_id_l}_val[{vlen}] = {{{init}}};")
                if ch.has_cccd.get():
                    lines.append(f"static uint8_t {svc_id_l}_{ch_id_l}_ccc[2] = {{0x00, 0x00}};")
        lines.append("")

        lines.append("/* Full GATT database */")
        lines.append("static const esp_gatts_attr_db_t gatt_db[IDX_NB] = {")
        for svc_item in svc_meta:
            svc = svc_item["svc"]
            svc_id = svc_item["id"]
            svc_id_l = svc_id.lower()
            svc_uuid = svc_item["uuid"]
            svc_decl_uuid = "primary_service_uuid" if svc.primary.get() else "secondary_service_uuid"
            svc_name = c_comment(svc.name)
            lines += [
                "",
                f"    /* Service: {svc_name} */",
                f"    [IDX_SVC_{svc_id}] =",
                "    {{ESP_GATT_AUTO_RSP},",
                f"      {{ESP_UUID_LEN_16, (uint8_t *)&{svc_decl_uuid}, ESP_GATT_PERM_READ,",
                f"        {svc_uuid['size']}, {svc_uuid['size']}, {svc_uuid['ptr']}}}}},",
            ]

            for char_item in svc_item["chars"]:
                ch = char_item["ch"]
                ch_id = char_item["id"]
                ch_id_l = ch_id.lower()
                props_var = f"char_prop_{svc_id_l}_{ch_id_l}"
                value_var = f"{svc_id_l}_{ch_id_l}_val"
                cccd_var = f"{svc_id_l}_{ch_id_l}_ccc"
                ch_uuid = char_item["uuid"]
                vlen = char_item["value_len"]
                lines += [
                    "",
                    f"    /* Characteristic: {c_comment(ch.name)} */",
                    f"    [IDX_{svc_id}_{ch_id}_DECL] =",
                    "    {{ESP_GATT_AUTO_RSP},",
                    "      {ESP_UUID_LEN_16, (uint8_t *)&character_declaration_uuid, ESP_GATT_PERM_READ,",
                    "        CHAR_DECLARATION_SIZE, CHAR_DECLARATION_SIZE,",
                    f"        (uint8_t *)&{props_var}}}}},",
                    "",
                    f"    [IDX_{svc_id}_{ch_id}_VAL] =",
                    "    {{ESP_GATT_AUTO_RSP},",
                    f"      {{{ch_uuid['len']}, {ch_uuid['ptr']},",
                    f"        {perms_macro(ch)},",
                    f"        {vlen}, sizeof({value_var}), {value_var}}}}},",
                ]
                if ch.has_cccd.get():
                    lines += [
                        "",
                        f"    [IDX_{svc_id}_{ch_id}_CFG] =",
                        "    {{ESP_GATT_AUTO_RSP},",
                        "      {ESP_UUID_LEN_16, (uint8_t *)&character_client_config_uuid,",
                        "        ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,",
                        f"        sizeof(uint16_t), sizeof({cccd_var}), {cccd_var}}}}},",
                    ]
        lines.append("};")
        lines.append("")

        lines += [
            "/* Advertising and connection parameter structs */",
            "static esp_ble_adv_data_t adv_data = {",
            "    .set_scan_rsp         = false,",
            "    .include_name         = true,",
            "    .include_txpower      = true,",
            f"    .min_interval         = {adv_min},",
            f"    .max_interval         = {adv_max},",
            f"    .appearance           = {appearance},",
            "    .manufacturer_len     = 0,",
            "    .p_manufacturer_data  = NULL,",
            "    .service_data_len     = 0,",
            "    .p_service_data       = NULL,",
            "    .service_uuid_len     = 0,",
            "    .p_service_uuid       = NULL,",
            "    .flag = (ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT),",
            "};",
            "",
            "static esp_ble_adv_params_t adv_params = {",
            f"    .adv_int_min        = {adv_min},",
            f"    .adv_int_max        = {adv_max},",
            "    .adv_type           = ADV_TYPE_IND,",
            "    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,",
            "    .channel_map        = ADV_CHNL_ALL,",
            "    .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,",
            "};",
            "",
        ]

        start_service_lines = []
        for svc_item in svc_meta:
            start_service_lines.append(
                f"            esp_ble_gatts_start_service(ble_handle_table[IDX_SVC_{svc_item['id']}]);"
            )

        lines += [
            "/* GAP event handler */",
            "static void gap_event_handler(esp_gap_ble_cb_event_t event,",
            "                              esp_ble_gap_cb_param_t *param) {",
            "    switch (event) {",
            "    case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:",
            "        esp_ble_gap_start_advertising(&adv_params);",
            "        break;",
            "    case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:",
            "        if (param->adv_start_cmpl.status != ESP_BT_STATUS_SUCCESS)",
            "            ESP_LOGE(TAG, \"Advertising start failed\");",
            "        else",
            "            ESP_LOGI(TAG, \"Advertising started\");",
            "        break;",
            "    case ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT:",
            "        ESP_LOGI(TAG, \"Advertising stopped\");",
            "        break;",
            "    case ESP_GAP_BLE_UPDATE_CONN_PARAMS_EVT:",
            "        ESP_LOGI(TAG, \"Connection params updated\");",
            "        break;",
            "    default:",
            "        break;",
            "    }",
            "}",
            "",
            "/* GATTS profile event handler */",
            "static void gatts_profile_event_handler(esp_gatts_cb_event_t event,",
            "        esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param) {",
            "    switch (event) {",
            "    case ESP_GATTS_REG_EVT:",
            "        esp_ble_gap_set_device_name(DEVICE_NAME);",
            "        esp_ble_gap_config_adv_data(&adv_data);",
            "        esp_ble_gatts_create_attr_tab(gatt_db, gatts_if, IDX_NB, SVC_INST_ID);",
            "        break;",
            "    case ESP_GATTS_READ_EVT:",
            "        ESP_LOGI(TAG, \"GATT Read, handle=%d\", param->read.handle);",
            "        break;",
            "    case ESP_GATTS_WRITE_EVT: {",
            "        ESP_LOGI(TAG, \"GATT Write, handle=%d, len=%d\",",
            "                 param->write.handle, param->write.len);",
            "        /* BUG FIX: bounds-check before touching any buffer */",
            "        if (param->write.len > sizeof(uint8_t) * 512) {",
            "            ESP_LOGE(TAG, \"Write too long (%d bytes), ignoring\", param->write.len);",
            "            break;",
            "        }",
            "        /* TODO: Add your write handler logic here */",
            "        if (param->write.need_rsp) {",
            "            esp_ble_gatts_send_response(gatts_if, param->write.conn_id,",
            "                    param->write.trans_id, ESP_GATT_OK, NULL);",
            "        }",
            "        break;",
            "    }",
            "    case ESP_GATTS_EXEC_WRITE_EVT:",
            "        esp_ble_gatts_send_response(gatts_if, param->exec_write.conn_id,",
            "                param->exec_write.trans_id, ESP_GATT_OK, NULL);",  # BUG FIX: exec_write union member, not write
            "        break;",
            "    case ESP_GATTS_CONNECT_EVT:",
            "        ESP_LOGI(TAG, \"Client connected, conn_id=%d\", param->connect.conn_id);",
            "        break;",
            "    case ESP_GATTS_DISCONNECT_EVT:",
            "        ESP_LOGI(TAG, \"Client disconnected, reason=0x%02x\",",  # BUG FIX: log reason code
            "                 param->disconnect.reason);",
            "        esp_ble_gap_start_advertising(&adv_params);",
            "        break;",
            "    case ESP_GATTS_CREAT_ATTR_TAB_EVT:",
            "        if (param->add_attr_tab.status != ESP_GATT_OK) {",
            "            ESP_LOGE(TAG, \"Create attr table failed, error=%d\",",
            "                     param->add_attr_tab.status);",
            "        } else if (param->add_attr_tab.num_handle != IDX_NB) {",
            "            ESP_LOGE(TAG, \"Handle count mismatch: %d != %d\",",
            "                     param->add_attr_tab.num_handle, IDX_NB);",
            "        } else {",
            "            memcpy(ble_handle_table, param->add_attr_tab.handles,",
            "                   sizeof(ble_handle_table));",
            *start_service_lines,
            "        }",
            "        break;",
            "    case ESP_GATTS_STOP_EVT:",
            "    case ESP_GATTS_OPEN_EVT:",
            "    case ESP_GATTS_CANCEL_OPEN_EVT:",
            "    case ESP_GATTS_CLOSE_EVT:",
            "    default:",
            "        break;",
            "    }",
            "}",
            "",
            "/* GATTS profile table */",
            "struct gatts_profile_inst {",
            "    esp_gatts_cb_t      gatts_cb;",
            "    uint16_t            gatts_if;",
            "    uint16_t            app_id;",
            "    uint16_t            conn_id;",
            "    uint16_t            service_handle;",
            "    esp_gatt_srvc_id_t  service_id;",
            "    uint16_t            char_handle;",
            "    esp_bt_uuid_t       char_uuid;",
            "    esp_gatt_perm_t     perm;",
            "    esp_gatt_char_prop_t property;",
            "    uint16_t            descr_handle;",
            "    esp_bt_uuid_t       descr_uuid;",
            "};",
            "",
            "static struct gatts_profile_inst ble_profile_tab[PROFILE_NUM] = {",
            "    [PROFILE_APP_IDX] = {",
            "        .gatts_cb = gatts_profile_event_handler,",
            "        .gatts_if = ESP_GATT_IF_NONE,",
            "    },",
            "};",
            "",
            "static void gatts_event_handler(esp_gatts_cb_event_t event,",
            "        esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param) {",
            "    if (event == ESP_GATTS_REG_EVT) {",
            "        if (param->reg.status == ESP_GATT_OK) {",
            "            ble_profile_tab[PROFILE_APP_IDX].gatts_if = gatts_if;",
            "        } else {",
            "            ESP_LOGE(TAG, \"Register app failed, app_id=%04x, status=%d\",",
            "                     param->reg.app_id, param->reg.status);",
            "            return;",
            "        }",
            "    }",
            "    for (int idx = 0; idx < PROFILE_NUM; idx++) {",
            "        if (gatts_if == ESP_GATT_IF_NONE ||",
            "            gatts_if == ble_profile_tab[idx].gatts_if) {",
            "            if (ble_profile_tab[idx].gatts_cb)",
            "                ble_profile_tab[idx].gatts_cb(event, gatts_if, param);",
            "        }",
            "    }",
            "}",
            "",
        ]

        # ── app_main
        lines += [
            "/* ─────────────────────────────────────────── */",
            "/*  app_main                                   */",
            "/* ─────────────────────────────────────────── */",
            "void app_main(void) {",
            "    esp_err_t ret;",
            "",
            "    /* Initialize NVS */",
            "    ret = nvs_flash_init();",
            "    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||",
            "        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {",
            "        ESP_ERROR_CHECK(nvs_flash_erase());",
            "        ret = nvs_flash_init();",
            "    }",
            "    ESP_ERROR_CHECK(ret);",
            "",
            "    /* Release BT classic memory */",
            "    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));",
            "",
            "    /* Initialize BT controller */",
            "    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();",
            "    ret = esp_bt_controller_init(&bt_cfg);",
            "    if (ret) { ESP_LOGE(TAG, \"bt_controller_init failed: %s\", esp_err_to_name(ret)); return; }",
            "",
            "    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);",
            "    if (ret) {",
            "        ESP_LOGE(TAG, \"bt_controller_enable failed: %s\", esp_err_to_name(ret));",
            "        esp_bt_controller_deinit();   /* BUG FIX: release controller on failure */",
            "        return;",
            "    }",
            "",
            "    /* Initialize Bluedroid */",
            "    ret = esp_bluedroid_init();",
            "    if (ret) {",
            "        ESP_LOGE(TAG, \"bluedroid_init failed: %s\", esp_err_to_name(ret));",
            "        esp_bt_controller_disable();  /* BUG FIX: unwind BT controller */",
            "        esp_bt_controller_deinit();",
            "        return;",
            "    }",
            "",
            "    ret = esp_bluedroid_enable();",
            "    if (ret) {",
            "        ESP_LOGE(TAG, \"bluedroid_enable failed: %s\", esp_err_to_name(ret));",
            "        esp_bluedroid_deinit();       /* BUG FIX: unwind bluedroid */",
            "        esp_bt_controller_disable();",
            "        esp_bt_controller_deinit();",
            "        return;",
            "    }",
            "",
            "    /* Register GATTS and GAP callbacks */",
            "    ret = esp_ble_gatts_register_callback(gatts_event_handler);",
            "    if (ret) { ESP_LOGE(TAG, \"gatts_register_callback failed: %s\", esp_err_to_name(ret)); return; }",
            "",
            "    ret = esp_ble_gap_register_callback(gap_event_handler);",
            "    if (ret) { ESP_LOGE(TAG, \"gap_register_callback failed: %s\", esp_err_to_name(ret)); return; }",
            "",
            "    ret = esp_ble_gatts_app_register(APP_ID);",
            "    if (ret) { ESP_LOGE(TAG, \"gatts_app_register failed: %s\", esp_err_to_name(ret)); return; }",
            "",
            f"    /* Set MTU */",
            f"    esp_ble_gatt_set_local_mtu({mtu});",
            "",
            f"    /* Set TX power */",
            f"    esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, {tx_pwr});",
            "",
            "    ESP_LOGI(TAG, \"BLE server started, advertising as: %s\", DEVICE_NAME);",
            "}",
            "",
            "/* ── End of generated file ── */",
        ]

        return "\n".join(lines)

# ─────────────────────────────────────────────────────────────
#  DIALOG: Add Service / Characteristic
# ─────────────────────────────────────────────────────────────
class _AddDialog(tk.Toplevel):
    def __init__(self, parent, title, options, kind):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_DARK)
        self.resizable(False, False)
        self.result = None
        self.grab_set()

        w, h = 480, 360
        px = parent.winfo_rootx() + (parent.winfo_width() - w)  // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        tk.Label(self, text=title, bg=BG_DARK, fg=ACCENT_BLUE,
            font=FONT_TITLE, padx=16, pady=12).pack(fill=tk.X)
        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X)

        body = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text=f"Select standard {kind} or choose Custom:",
            bg=BG_DARK, fg=TEXT_SEC, font=FONT_SMALL).pack(anchor="w")

        self._sel_var = tk.StringVar(value=options[-1])
        lb_frame = tk.Frame(body, bg=BG_MID)
        lb_frame.pack(fill=tk.BOTH, expand=True, pady=6)
        vsb = ttk.Scrollbar(lb_frame, style="Dark.Vertical.TScrollbar")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        lb = tk.Listbox(lb_frame, listvariable=tk.StringVar(value=options),
            bg=BG_MID, fg=TEXT_PRIMARY, selectbackground=SEL_BG,
            selectforeground=TEXT_PRIMARY, activestyle="none",
            font=FONT_NORMAL, bd=0, relief="flat",
            yscrollcommand=vsb.set, exportselection=False)
        lb.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=lb.yview)
        lb.selection_set(len(options)-1)
        lb.see(len(options)-1)

        tk.Label(body, text="Display Name:", bg=BG_DARK,
            fg=TEXT_SEC, font=FONT_SMALL).pack(anchor="w", pady=(6,2))
        self._name_var = tk.StringVar(value=f"My {kind.capitalize()}")
        name_entry = tk.Entry(body, textvariable=self._name_var,
            bg=BG_CARD, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief="flat", bd=4, font=FONT_NORMAL)
        name_entry.pack(fill=tk.X)
        name_entry.focus_set()

        def on_select(event=None):
            sel = lb.curselection()
            if sel:
                chosen = options[sel[0]]
                # Pre-fill name from selection if not custom
                if chosen != f"Custom {kind.capitalize()}":
                    # Strip UUID part
                    clean = re.sub(r'\s*\(0x[0-9A-Fa-f]+\)', '', chosen).strip()
                    self._name_var.set(clean)
        lb.bind("<<ListboxSelect>>", on_select)

        btn_row = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        btn_row.pack(fill=tk.X)

        def confirm():
            sel = lb.curselection()
            chosen_key = options[sel[0]] if sel else options[-1]
            self.result = (self._name_var.get().strip() or f"My {kind}", chosen_key)
            self.destroy()

        ok = tk.Label(btn_row, text="  Add  ", bg=ACCENT_BLUE, fg=BG_DARK,
            font=FONT_HEAD, padx=10, pady=6, cursor="hand2")
        ok.pack(side=tk.LEFT)
        ok.bind("<Button-1>", lambda e: confirm())
        self.bind("<Return>", lambda e: confirm())

        cancel = tk.Label(btn_row, text="  Cancel  ", bg=BG_CARD, fg=TEXT_SEC,
            font=FONT_NORMAL, padx=10, pady=6, cursor="hand2")
        cancel.pack(side=tk.LEFT, padx=8)
        cancel.bind("<Button-1>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())

class _RenameDialog(tk.Toplevel):
    def __init__(self, parent, title, current):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_DARK)
        self.resizable(False, False)
        self.result = None
        self.grab_set()

        w, h = 360, 160
        px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        tk.Label(self, text=title, bg=BG_DARK, fg=ACCENT_BLUE,
            font=FONT_HEAD, padx=16, pady=10).pack(fill=tk.X)

        body = tk.Frame(self, bg=BG_DARK, padx=16)
        body.pack(fill=tk.X)
        self._var = tk.StringVar(value=current)
        e = tk.Entry(body, textvariable=self._var, bg=BG_CARD,
            fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief="flat", bd=4, font=FONT_NORMAL)
        e.pack(fill=tk.X)
        e.focus_set()
        e.select_range(0, tk.END)

        btn_row = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        btn_row.pack(fill=tk.X)

        def confirm():
            self.result = self._var.get().strip()
            self.destroy()

        ok = tk.Label(btn_row, text="  Rename  ", bg=ACCENT_BLUE, fg=BG_DARK,
            font=FONT_HEAD, padx=10, pady=6, cursor="hand2")
        ok.pack(side=tk.LEFT)
        ok.bind("<Button-1>", lambda e: confirm())
        self.bind("<Return>", lambda e: confirm())

        cancel = tk.Label(btn_row, text="  Cancel  ", bg=BG_CARD, fg=TEXT_SEC,
            font=FONT_NORMAL, padx=10, pady=6, cursor="hand2")
        cancel.pack(side=tk.LEFT, padx=8)
        cancel.bind("<Button-1>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = BLEConfigurator()
    app.mainloop()