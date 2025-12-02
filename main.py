import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas, font as tkfont, filedialog
from PIL import Image, ImageTk, ImageDraw
import colorsys
import json
import os
import sys
import base64
import tempfile
import re
import shutil
import time  # Added missing import
from datetime import datetime

# =============================================================================
# --- ASSETS: EMBEDDED FALLBACK ICON ---
# =============================================================================
ICON_BASE64 = """
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABMLAAATCwAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAABwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAA
AAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAA
AAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAH
BwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcH
BwcHBwcHBwcHBwcHBwcHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""

# =============================================================================
# --- PATH MANAGEMENT ---
# =============================================================================

def get_app_data_path():
    app_data = os.getenv('APPDATA')
    path = os.path.join(app_data, "PaliaTimer")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def generate_temp_icon():
    try:
        temp_dir = tempfile.gettempdir()
        icon_path = os.path.join(temp_dir, "palia_timer_default.ico")
        if not os.path.exists(icon_path):
            with open(icon_path, "wb") as f:
                f.write(base64.b64decode(ICON_BASE64))
        return icon_path
    except:
        return None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_FILE = os.path.join(get_app_data_path(), "config.json")
DEFAULT_ICON_TEMP = generate_temp_icon()
BUNDLED_ICON = resource_path("icon.ico")

# =============================================================================
# --- CUSTOM WIDGETS ---
# =============================================================================

class PopupBase(ctk.CTkToplevel):
    def __init__(self, parent, title, w, h):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.resizable(False, False)
        
        self.transient(parent)
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        
        try:
            icon = parent.get_current_icon()
            if icon and os.path.exists(icon): self.iconbitmap(icon)
        except: pass
        
        self.after(100, self.safe_grab)

    def safe_grab(self):
        try: self.grab_set()
        except: pass

class GradientSlider(ctk.CTkCanvas):
    def __init__(self, master, width=200, height=20, command=None, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.bind("<B1-Motion>", self._on_click)
        self.bind("<Button-1>", self._on_click)
        self.draw_gradient()

    def draw_gradient(self):
        w = int(self.cget("width"))
        h = int(self.cget("height"))
        self.img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(self.img)
        for x in range(w):
            hue = x / w
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            draw.line((x, 0, x, h), fill=(int(r*255), int(g*255), int(b*255)))
        self.photo = ImageTk.PhotoImage(self.img)
        self.create_image(0, 0, anchor="nw", image=self.photo)

    def _on_click(self, event):
        w = self.winfo_width()
        x = max(0, min(event.x, w))
        hue = x / w
        if self.command: self.command(hue)

class AdvancedColorPicker(PopupBase):
    def __init__(self, parent, initial_color, callback):
        super().__init__(parent, "Select Color", 400, 520)
        self.callback = callback
        
        self.current_hue = 0.0
        self.current_sat = 1.0
        self.current_val = 1.0

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.sv_size = 250
        self.sv_canvas = Canvas(self.main_frame, width=self.sv_size, height=self.sv_size, 
                                highlightthickness=1, highlightbackground="gray", cursor="crosshair")
        self.sv_canvas.pack(pady=(0, 10))
        self.sv_canvas.bind("<B1-Motion>", self._on_sv_click)
        self.sv_canvas.bind("<Button-1>", self._on_sv_click)

        self.hue_slider = GradientSlider(self.main_frame, width=self.sv_size, height=25, command=self._on_hue_change)
        self.hue_slider.pack(pady=(0, 15))

        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", pady=5)
        
        self.preview_box = ctk.CTkLabel(self.info_frame, text="", width=60, height=30, corner_radius=5)
        self.preview_box.pack(side="left", padx=10, pady=5)
        
        self.hex_entry = ctk.CTkEntry(self.info_frame, width=120, placeholder_text="#RRGGBB")
        self.hex_entry.insert(0, initial_color)
        self.hex_entry.pack(side="left", padx=10)
        self.hex_entry.bind("<Return>", self._manual_hex)
        
        ctk.CTkButton(self.info_frame, text="Apply", width=80, command=self._confirm).pack(side="right", padx=10)

        self.preset_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.preset_frame.pack(fill="x", pady=10)
        presets = ["#FFFFFF", "#000000", "#FF5555", "#55FF55", "#5555FF", "#FFFF55", "#FF55FF", "#1A1A1A", "#2B2B2B", "#FF9900", "#00AAFF", "#AA00FF", "#FF0055"]
        for i, color in enumerate(presets):
            btn = ctk.CTkButton(self.preset_frame, text="", width=25, height=25, fg_color=color, hover_color=color, corner_radius=12, command=lambda c=color: self._set_hex(c))
            btn.grid(row=i//7, column=i%7, padx=3, pady=3)

        self._update_sv_map()
        self._set_hex(initial_color)

    def _update_sv_map(self):
        small_size = 64
        small_img = Image.new("RGB", (small_size, small_size))
        small_pixels = small_img.load()
        for x in range(small_size):
            for y in range(small_size):
                sat = x / small_size
                val = 1.0 - (y / small_size)
                r, g, b = colorsys.hsv_to_rgb(self.current_hue, sat, val)
                # FIX: Variable name mismatch fixed here
                small_pixels[x, y] = (int(r*255), int(g*255), int(b*255))
        self.sv_img = small_img.resize((self.sv_size, self.sv_size), Image.Resampling.BILINEAR)
        self.sv_photo = ImageTk.PhotoImage(self.sv_img)
        self.sv_canvas.create_image(0, 0, anchor="nw", image=self.sv_photo)

    def _on_hue_change(self, hue):
        self.current_hue = hue
        self._update_sv_map()
        self._update_color()

    def _on_sv_click(self, event):
        x = max(0, min(event.x, self.sv_size))
        y = max(0, min(event.y, self.sv_size))
        self.current_sat = x / self.sv_size
        self.current_val = 1.0 - (y / self.sv_size)
        self._update_color()

    def _update_color(self):
        r, g, b = colorsys.hsv_to_rgb(self.current_hue, self.current_sat, self.current_val)
        hex_col = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, hex_col)
        self.preview_box.configure(fg_color=hex_col)

    def _manual_hex(self, event): self._set_hex(self.hex_entry.get())
    def _set_hex(self, hex_col):
        if len(hex_col) == 7 and hex_col.startswith("#"):
            self.hex_entry.delete(0, "end")
            self.hex_entry.insert(0, hex_col)
            self.preview_box.configure(fg_color=hex_col)
    def _confirm(self):
        self.callback(self.hex_entry.get())
        self.destroy()

class FontSearchPopup(PopupBase):
    def __init__(self, parent, callback):
        super().__init__(parent, "Select Font", 350, 450)
        self.callback = callback
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._update_list)
        
        self.header = ctk.CTkFrame(self)
        self.header.pack(fill="x", padx=10, pady=10)
        ctk.CTkEntry(self.header, textvariable=self.search_var, placeholder_text="Search...").pack(fill="x")

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.all_fonts = sorted(list(tkfont.families()))
        self.buttons = []
        self._populate(self.all_fonts[:30])

    def _populate(self, font_list):
        for btn in self.buttons: btn.destroy()
        self.buttons = []
        for f in font_list:
            try:
                btn = ctk.CTkButton(self.scroll, text=f, font=(f, 16), fg_color="transparent", 
                                    text_color=("black", "white"), anchor="w", height=35,
                                    command=lambda val=f: self._select(val))
                btn.pack(fill="x", pady=1)
                self.buttons.append(btn)
            except: pass

    def _update_list(self, *args):
        term = self.search_var.get().lower()
        filtered = [f for f in self.all_fonts if term in f.lower()]
        self._populate(filtered[:50])

    def _select(self, f):
        self.callback(f)
        self.destroy()

# =============================================================================
# --- MAIN SETTINGS ---
# =============================================================================

class PaliaTimerSettings(PopupBase):
    def __init__(self, parent):
        super().__init__(parent, "Settings", 450, 600)
        self.parent = parent
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.setup_visuals(self.tabview.add("Visuals"))
        self.setup_window(self.tabview.add("Window"))
        self.setup_help(self.tabview.add("Help"))

    def setup_visuals(self, t):
        # Removed Theme Selector to prevent Bricking
        
        ctk.CTkLabel(t, text="Colors & Font", font=("Arial", 13, "bold")).pack(anchor="w", pady=(15, 5))
        self.font_btn = ctk.CTkButton(t, text=f"Font: {self.parent.config['font_family']}", command=self.open_font_picker)
        self.font_btn.pack(fill="x", pady=5)
        
        row = ctk.CTkFrame(t, fg_color="transparent")
        row.pack(fill="x")
        ctk.CTkButton(row, text="Text Color", command=self.pick_text_color, fg_color=self.parent.config["text_color"]).pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkButton(row, text="Background", command=self.pick_bg_color, fg_color=self.parent.config["bg_color"]).pack(side="right", fill="x", expand=True, padx=2)

        ctk.CTkLabel(t, text="Style", font=("Arial", 13, "bold")).pack(anchor="w", pady=(15, 5))
        self.invis_var = ctk.BooleanVar(value=self.parent.config["invisible_bg"])
        ctk.CTkSwitch(t, text="Invisible Background", variable=self.invis_var, command=self.update_toggles).pack(pady=5, anchor="w")
        self.outline_var = ctk.BooleanVar(value=self.parent.config["text_outline"])
        ctk.CTkSwitch(t, text="Text Outline (Stroke)", variable=self.outline_var, command=self.update_toggles).pack(pady=5, anchor="w")

    def setup_window(self, t):
        ctk.CTkLabel(t, text="App Icon", font=("Arial", 13, "bold")).pack(anchor="w", pady=(10, 5))
        
        icon_frame = ctk.CTkFrame(t, fg_color="transparent")
        icon_frame.pack(fill="x", pady=5)
        
        self.preview_lbl = ctk.CTkLabel(icon_frame, text="", width=40, height=40, fg_color="#333333", corner_radius=5)
        self.preview_lbl.pack(side="left", padx=5)
        self.load_preview()

        ctk.CTkButton(icon_frame, text="Choose Icon (.ico/.png)", command=self.choose_icon).pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(icon_frame, text="Reset", width=50, fg_color="#555555", command=self.reset_icon).pack(side="right", padx=5)

        ctk.CTkLabel(t, text="Opacity & Behavior", font=("Arial", 13, "bold")).pack(anchor="w", pady=(15, 5))
        self.op_slider = ctk.CTkSlider(t, from_=0.1, to=1.0, command=self.update_opacity)
        self.op_slider.set(self.parent.config["opacity"])
        self.op_slider.pack(fill="x", pady=5)
        
        self.lock_var = ctk.BooleanVar(value=self.parent.config["locked"])
        ctk.CTkSwitch(t, text="Lock Position", variable=self.lock_var, command=self.update_toggles).pack(pady=10, anchor="w")
        self.top_var = ctk.BooleanVar(value=self.parent.config["always_on_top"])
        ctk.CTkSwitch(t, text="Always On Top", variable=self.top_var, command=self.update_toggles).pack(pady=10, anchor="w")

        ctk.CTkButton(t, text="Reset All Settings", fg_color="#AA3333", hover_color="#772222", command=self.reset_app).pack(pady=40)

    def setup_help(self, t):
        info = "Right-Click for Menu.\n\nPALIA SETUP:\nSet Graphics > Window Mode to 'Windowed Fullscreen'.\n\nINVISIBLE MODE:\nRemoves the background box. Click the text to drag.\n\nRESIZING:\nDrag the bottom-right corner."
        ctk.CTkLabel(t, text=info, justify="left", font=("Arial", 14), anchor="nw", wraplength=350).pack(pady=20, padx=10, fill="both")

    def load_preview(self):
        path = self.parent.get_current_icon()
        if path and os.path.exists(path):
            try:
                img = Image.open(path).resize((30, 30))
                ctk_img = ctk.CTkImage(img, size=(30, 30))
                self.preview_lbl.configure(image=ctk_img)
            except: pass
        else:
            self.preview_lbl.configure(image=None)

    def choose_icon(self):
        path = tk.filedialog.askopenfilename(filetypes=[("Images", "*.ico;*.png")])
        if path:
            dest_folder = os.path.join(get_app_data_path(), "icons")
            if not os.path.exists(dest_folder): os.makedirs(dest_folder)
            
            # Use timestamp to prevent file locking issues
            unique_name = f"icon_{int(time.time())}.ico"
            final_path = os.path.join(dest_folder, unique_name)
            
            try:
                if path.lower().endswith(".png"):
                    img = Image.open(path)
                    img.save(final_path, format='ICO', sizes=[(256, 256)])
                else:
                    shutil.copy(path, final_path)
            except Exception as e:
                print(e)
                return

            self.parent.config["custom_icon_path"] = final_path
            self.parent.update_icon()
            self.parent.save_config()
            self.load_preview()

    def reset_icon(self):
        self.parent.config["custom_icon_path"] = None
        self.parent.update_icon()
        self.parent.save_config()
        self.load_preview()

    def open_font_picker(self): FontSearchPopup(self, self.set_font)
    def set_font(self, f):
        self.parent.config["font_family"] = f
        self.font_btn.configure(text=f"Font: {f}")
        self.parent.rebuild_visuals()
        self.parent.save_config()

    def pick_text_color(self): AdvancedColorPicker(self, self.parent.config["text_color"], self.set_text_color)
    def set_text_color(self, c):
        self.parent.config["text_color"] = c
        self.parent.rebuild_visuals()
        self.parent.save_config()

    def pick_bg_color(self): AdvancedColorPicker(self, self.parent.config["bg_color"], self.set_bg_color)
    def set_bg_color(self, c):
        self.parent.config["bg_color"] = c
        self.parent.rebuild_visuals()
        self.parent.save_config()

    def update_opacity(self, val):
        self.parent.config["opacity"] = val
        self.parent.attributes("-alpha", val)
        self.parent.save_config()

    def update_toggles(self):
        self.parent.config["invisible_bg"] = self.invis_var.get()
        self.parent.config["text_outline"] = self.outline_var.get()
        self.parent.config["locked"] = self.lock_var.get()
        self.parent.config["always_on_top"] = self.top_var.get()
        self.parent.attributes("-topmost", self.parent.config["always_on_top"])
        self.parent.rebuild_visuals()
        self.parent.save_config()

    def reset_app(self):
        try: os.remove(CONFIG_FILE)
        except: pass
        self.parent.destroy()
        os._exit(0)

# =============================================================================
# --- MAIN CONTROLLER ---
# =============================================================================

class PaliaTimerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_config = {
            "geometry": "240x80+100+100",
            "bg_color": "#1A1A1A",
            "text_color": "#FFFFFF",
            "font_family": "Arial",
            "opacity": 0.85,
            "locked": False,
            "always_on_top": True,
            "invisible_bg": False,
            "text_outline": False,
            "show_welcome": True,
            "theme": "Dark",
            "custom_icon_path": None
        }
        self.config = self.default_config.copy()
        self.load_config()

        # LOCKED TO DARK MODE
        ctk.set_appearance_mode("Dark")

        self.overrideredirect(True)
        self.attributes("-topmost", self.config["always_on_top"])
        self.attributes("-alpha", 0.0) 
        self.geometry(self.config["geometry"])
        self.minsize(40, 20)
        
        self.update_icon()

        self.canvas = Canvas(self, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.bg_rect = self.canvas.create_rectangle(0,0,1,1, fill="black", outline="")
        self.outline_ids = []
        self.text_id = self.canvas.create_text(0,0, text="--:--", fill="white")
        self.grip_text = self.canvas.create_text(0,0, text="⇲", font=("Arial", 14), fill="gray")

        self.bind_events()
        self.is_running = True
        self.last_time_str = ""
        
        self.bind("<Configure>", self.on_configure)

        if self.config["show_welcome"]:
            self.withdraw()
            WelcomeWindow(self)
        else:
            self.animate_fade_in()
            self.run_timer()

    def get_current_icon(self):
        # 1. Custom
        custom = self.config.get("custom_icon_path")
        if custom and os.path.exists(custom): return custom
        # 2. Bundled (PyInstaller)
        if os.path.exists(BUNDLED_ICON): return BUNDLED_ICON
        # 3. Generated Temp
        return DEFAULT_ICON_TEMP

    def update_icon(self):
        try:
            icon = self.get_current_icon()
            if icon: self.iconbitmap(icon)
        except: pass

    def animate_fade_in(self):
        cur = self.attributes("-alpha")
        tgt = self.config["opacity"]
        if cur < tgt:
            self.attributes("-alpha", min(cur+0.05, tgt))
            self.after(20, self.animate_fade_in)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config.update(json.load(f))
            except: pass

    def save_config(self):
        self.config["geometry"] = self.geometry()
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.canvas.tag_bind(self.grip_text, "<Enter>", lambda e: self.canvas.itemconfig(self.grip_text, fill="white"))
        self.canvas.tag_bind(self.grip_text, "<Leave>", lambda e: self.canvas.itemconfig(self.grip_text, fill="#666666"))

    def on_configure(self, event):
        if self.is_running:
            self.rebuild_visuals()

    def rebuild_visuals(self):
        w = self.winfo_width()
        h = self.winfo_height()

        if self.config["invisible_bg"]:
            chroma = "#000001"
            self.attributes("-transparentcolor", chroma)
            self.canvas.configure(bg=chroma)
            self.canvas.itemconfig(self.bg_rect, fill=chroma)
        else:
            self.attributes("-transparentcolor", "")
            self.canvas.configure(bg=self.config["bg_color"])
            self.canvas.itemconfig(self.bg_rect, fill=self.config["bg_color"])

        size = min(int(h * 0.75), int(w / 3.5))
        if size < 6: size = 6
        font_spec = (self.config["font_family"], size, "bold")
        
        display_text = self.last_time_str if self.last_time_str else "Loading"
        
        for oid in self.outline_ids: self.canvas.delete(oid)
        self.outline_ids = []
        if self.config["text_outline"]:
            for i in range(8):
                oid = self.canvas.create_text(0,0, text=display_text, font=font_spec, fill="black")
                self.canvas.tag_lower(oid)
                self.outline_ids.append(oid)
        
        self.canvas.itemconfig(self.text_id, font=font_spec, fill=self.config["text_color"], text=display_text)
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.grip_text)
        
        cx, cy = w/2, h/2
        self.canvas.coords(self.bg_rect, 0, 0, w, h)
        self.canvas.coords(self.text_id, cx, cy)
        self.canvas.coords(self.grip_text, w-10, h-10)
        offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
        for i, oid in enumerate(self.outline_ids):
            if i < len(offsets):
                ox, oy = offsets[i]
                self.canvas.coords(oid, cx+ox, cy+oy)

    def run_timer(self):
        if not self.is_running: return
        try:
            now = datetime.utcnow()
            total_sec = ((now.minute * 60) + now.second + (now.microsecond / 1e6)) * 24
            ph = int(total_sec // 3600)
            pm = int((total_sec % 3600) // 60)
            
            target_min = (pm // 4) * 4 + 1
            if target_min <= pm: target_min += 4
            target_h = ph
            if target_min >= 60:
                target_min -= 60
                target_h = (target_h + 1) % 24
            
            dis_h = target_h if target_h <= 12 else target_h - 12
            if dis_h == 0: dis_h = 12
            suffix = "AM" if target_h < 12 else "PM"
            time_str = f"{dis_h}:{target_min:02d} {suffix}"
            
            if time_str != self.last_time_str:
                self.last_time_str = time_str
                self.canvas.itemconfig(self.text_id, text=time_str)
                for oid in self.outline_ids:
                    self.canvas.itemconfig(oid, text=time_str)
        except: pass
        self.after(100, self.run_timer)

    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_w = self.winfo_width()
        self.start_h = self.winfo_height()
        self.win_x = self.winfo_x()
        self.win_y = self.winfo_y()
        w, h = self.start_w, self.start_h
        if event.x > w - 25 and event.y > h - 25:
            self.mode = "resize"
            self.canvas.configure(cursor="size_nw_se")
        else:
            self.mode = "drag"
            if not self.config["locked"]: self.canvas.configure(cursor="fleur")

    def on_drag(self, event):
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y
        if self.mode == "drag":
            if self.config["locked"]: return
            self.geometry(f"+{self.win_x + dx}+{self.win_y + dy}")
        elif self.mode == "resize":
            new_w = max(40, self.start_w + dx)
            new_h = max(20, self.start_h + dy)
            self.geometry(f"{new_w}x{new_h}")

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="⚙ Settings", command=self.open_settings)
        menu.add_separator()
        menu.add_command(label="❌ Quit", command=self.close_app)
        menu.post(event.x_root, event.y_root)

    def open_settings(self):
        self.settings = PaliaTimerSettings(self)

    def close_app(self):
        self.save_config()
        self.destroy()
        os._exit(0)

class WelcomeWindow(PopupBase):
    def __init__(self, parent):
        super().__init__(parent, "Welcome", 400, 450)
        self.parent = parent
        
        ctk.CTkLabel(self, text="Palia Timer", font=("Arial", 24, "bold"), text_color="#00AAFF").pack(pady=(30, 10))
        info = "1. IN-GAME:\nSet 'Windowed Fullscreen'.\n\n2. CUSTOMIZE:\nRight-Click to change Colors/Fonts.\n\n3. CONTROLS:\nDrag to move. Drag bottom-right to resize."
        ctk.CTkLabel(self, text=info, font=("Arial", 14), justify="left", wraplength=350).pack(pady=20)
        self.chk = ctk.CTkCheckBox(self, text="Don't show this again")
        self.chk.pack(pady=20)
        ctk.CTkButton(self, text="Start Timer", height=40, command=self.start_app).pack(pady=10, fill="x", padx=40)

    def start_app(self):
        if self.chk.get() == 1:
            self.parent.config["show_welcome"] = False
            self.parent.save_config()
        self.destroy()
        self.parent.deiconify()
        self.parent.update_idletasks() 
        self.parent.rebuild_visuals()
        self.parent.animate_fade_in()
        self.parent.run_timer()

if __name__ == "__main__":
    app = PaliaTimerApp()
    app.mainloop()