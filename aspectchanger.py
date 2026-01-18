import ctypes
import tkinter as tk
from tkinter import messagebox

user32 = ctypes.windll.user32
dwmapi = ctypes.windll.dwmapi

# -------------------- NATIVE RES --------------------

def get_native_resolution():
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

NATIVE_W, NATIVE_H = get_native_resolution()

# -------------------- DISPLAY LOGIC --------------------

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong),
    ]

DM_PELSWIDTH = 0x80000
DM_PELSHEIGHT = 0x100000

def set_resolution(w, h):
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth = w
    dm.dmPelsHeight = h
    dm.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT

    if user32.ChangeDisplaySettingsW(ctypes.byref(dm), 0) != 0:
        messagebox.showerror("Error", "Resolution not supported")

def restore_native():
    set_resolution(NATIVE_W, NATIVE_H)

def apply_custom():
    try:
        set_resolution(int(w_entry.get()), int(h_entry.get()))
    except:
        messagebox.showerror("Invalid Input", "Enter valid numbers")

# -------------------- UI --------------------

BG = "#0f0f12"
BTN = "#1e1e24"
ACCENT = "#6b5cff"
TEXT = "#e5e5e5"
SUB = "#888888"
TOP = "#15151b"

root = tk.Tk()
root.geometry("360x500")

root.overrideredirect(True)
root.configure(bg=BG)

# Rounded corners (Windows 11+)
DWMWA_WINDOW_CORNER_PREFERENCE = 33
DWMWCP_ROUND = 2
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
dwmapi.DwmSetWindowAttribute(
    hwnd,
    DWMWA_WINDOW_CORNER_PREFERENCE,
    ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
    ctypes.sizeof(ctypes.c_int)
)

# -------------------- DRAGGING --------------------

def start_drag(e):
    root.x = e.x
    root.y = e.y

def drag(e):
    root.geometry(f"+{e.x_root - root.x}+{e.y_root - root.y}")

# -------------------- TITLE BAR --------------------

title_bar = tk.Frame(root, bg=TOP, height=40)
title_bar.pack(fill="x")
title_bar.bind("<Button-1>", start_drag)
title_bar.bind("<B1-Motion>", drag)

tk.Label(
    title_bar,
    text="ASPECT CHANGER",
    fg=TEXT,
    bg=TOP,
    font=("Segoe UI", 11, "bold")
).pack(side="left", padx=12)

tk.Button(
    title_bar,
    text="✕",
    bg=TOP,
    fg=SUB,
    bd=0,
    command=root.destroy,
    font=("Segoe UI", 11)
).pack(side="right", padx=10)

# -------------------- CONTENT --------------------

content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, pady=10)

tk.Label(
    content,
    text=f"Native Resolution: {NATIVE_W} x {NATIVE_H}",
    fg=SUB,
    bg=BG,
    font=("Segoe UI", 9)
).pack(pady=6)

def btn(text, cmd):
    return tk.Button(
        content, text=text, command=cmd,
        bg=BTN, fg=TEXT,
        activebackground=ACCENT,
        activeforeground="white",
        relief="flat",
        font=("Segoe UI", 10),
        width=28, height=2
    )

btn("NATIVE", restore_native).pack(pady=8)
btn("16:9  •  1920 x 1080", lambda: set_resolution(1920, 1080)).pack(pady=4)
btn("4:3   •  1440 x 1080", lambda: set_resolution(1440, 1080)).pack(pady=4)
btn("21:9 •  2560 x 1080", lambda: set_resolution(2560, 1080)).pack(pady=4)

tk.Label(content, text="CUSTOM RESOLUTION", fg=SUB, bg=BG,
         font=("Segoe UI", 9)).pack(pady=12)

frame = tk.Frame(content, bg=BG)
frame.pack()

w_entry = tk.Entry(frame, width=8, bg=BTN, fg=TEXT,
                   insertbackground=TEXT, relief="flat")
h_entry = tk.Entry(frame, width=8, bg=BTN, fg=TEXT,
                   insertbackground=TEXT, relief="flat")

w_entry.grid(row=0, column=0, padx=8, ipady=6)
h_entry.grid(row=0, column=1, padx=8, ipady=6)

btn("APPLY CUSTOM", apply_custom).pack(pady=12)

# -------------------- FOOTER --------------------

tk.Label(
    root,
    text="devs: lemmy, glock",
    fg=SUB,
    bg=BG,
    font=("Segoe UI", 8)
).pack(side="bottom", pady=6)

root.mainloop()
