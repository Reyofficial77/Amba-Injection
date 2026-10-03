import tkinter as tk
from PIL import Image, ImageTk
import pygame
import threading
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
IMAGE_PATH = ASSETS / "ambatukam.png"
AUDIO_PATH = ASSETS / "ambatukam.mp3"

running = True
MAX_WINDOWS = 22
SPAWN_INTERVAL = 700

root = tk.Tk()
root.title("Amba Injection")
root.attributes("-fullscreen", True)
root.configure(bg="#1686d9")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

desktop = tk.Canvas(
    root,
    bg="#1686d9",
    highlightthickness=0
)
desktop.pack(fill="both", expand=True)

# Fake desktop wallpaper / taskbar. Everything here is inside the app.
desktop.create_text(
    screen_w // 2,
    45,
    text="AMBA INJECTION",
    fill="white",
    font=("Arial", 30, "bold")
)

taskbar_h = 48
desktop.create_rectangle(
    0, screen_h - taskbar_h,
    screen_w, screen_h,
    fill="#000000",
    outline=""
)
desktop.create_text(
    18, screen_h - 24,
    anchor="w",
    text="⊞  Amba Desktop",
    fill="white",
    font=("Arial", 14, "bold")
)
desktop.create_text(
    screen_w - 18, screen_h - 24,
    anchor="e",
    text="AMBATUKAMM!",
    fill="#dddddd",
    font=("Arial", 10)
)

try:
    source = Image.open(IMAGE_PATH).convert("RGB")
    source.thumbnail((230, 180))
    source_photo = ImageTk.PhotoImage(source)
except Exception:
    source_photo = None

fake_windows = []

def close_fake_window(frame):
    if frame in fake_windows:
        fake_windows.remove(frame)
    try:
        frame.destroy()
    except tk.TclError:
        pass

def make_fake_window():
    if not running or len(fake_windows) >= MAX_WINDOWS:
        return

    width = random.randint(270, 390)
    height = random.randint(220, 310)
    x = random.randint(10, max(10, screen_w - width - 10))
    y = random.randint(70, max(70, screen_h - height - taskbar_h - 10))

    frame = tk.Frame(
        root,
        bg="#eeeeee",
        bd=2,
        relief="raised"
    )
    frame.place(x=x, y=y, width=width, height=height)
    fake_windows.append(frame)

    titlebar = tk.Frame(frame, bg="#0758a6", height=32)
    titlebar.pack(fill="x")
    titlebar.pack_propagate(False)

    tk.Label(
        titlebar,
        text="Amba.exe",
        bg="#0758a6",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=8)

    close = tk.Button(
        titlebar,
        text="X",
        command=lambda f=frame: close_fake_window(f),
        bg="#d92727",
        fg="white",
        activebackground="#ff5555",
        activeforeground="white",
        bd=0,
        font=("Arial", 10, "bold"),
        width=3
    )
    close.pack(side="right", padx=2, pady=2)

    content = tk.Frame(frame, bg="#eeeeee")
    content.pack(fill="both", expand=True)

    if source_photo:
        label = tk.Label(content, image=source_photo, bg="#eeeeee")
        label.image = source_photo
        label.pack(expand=True, pady=(8, 0))
    else:
        tk.Label(
            content,
            text="AMBATUKAM!",
            bg="#eeeeee",
            fg="#111111",
            font=("Arial", 28, "bold")
        ).pack(expand=True)

    tk.Label(
        content,
        text="YOU ARE AMBATUKAM!",
        bg="#eeeeee",
        fg="#111111",
        font=("Arial", 11, "bold")
    ).pack(pady=8)

    # Make fake windows draggable, but only inside this app.
    drag = {"x": 0, "y": 0}

    def start_drag(event):
        drag["x"] = event.x
        drag["y"] = event.y

    def do_drag(event):
        nx = frame.winfo_x() + event.x - drag["x"]
        ny = frame.winfo_y() + event.y - drag["y"]
        nx = max(0, min(nx, screen_w - frame.winfo_width()))
        ny = max(0, min(ny, screen_h - taskbar_h - frame.winfo_height()))
        frame.place(x=nx, y=ny)

    titlebar.bind("<Button-1>", start_drag)
    titlebar.bind("<B1-Motion>", do_drag)

def spawn_loop():
    if not running:
        return
    make_fake_window()
    root.after(SPAWN_INTERVAL, spawn_loop)

def stop_app():
    global running
    if not running:
        return
    running = False

    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception:
        pass

    try:
        root.destroy()
    except tk.TclError:
        pass

    print("\n[!] Amba Injection dihentikan.")

def cmd_listener():
    print("=" * 55)
    print(" AMBA INJECTION - FAKE DESKTOP PRANK")
    print("=" * 55)
    print("[*] Ini adalah fake desktop di dalam aplikasi.")
    print("[*] Ketik 'stop' lalu Enter untuk keluar.")
    print("[*] Ctrl+C juga dapat digunakan.")

    while running:
        try:
            command = input("Amba> ").strip().lower()
            if command == "stop":
                root.after(0, stop_app)
                break
            elif command:
                print("[!] Gunakan: stop")
        except (EOFError, KeyboardInterrupt, OSError):
            root.after(0, stop_app)
            break

# Start with a few windows.
for _ in range(4):
    make_fake_window()

try:
    pygame.mixer.init()
    pygame.mixer.music.load(str(AUDIO_PATH))
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"[!] Audio tidak dapat diputar: {e}")

threading.Thread(target=cmd_listener, daemon=True).start()
spawn_loop()

try:
    root.mainloop()
except KeyboardInterrupt:
    stop_app()
