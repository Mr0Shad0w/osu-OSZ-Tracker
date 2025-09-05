import os
from getpass import getuser
from time import sleep
import threading
from PIL import Image, ImageDraw
import pystray


user_name = getuser()
downloads_dir = f"C:/Users/{user_name}/Downloads/"


def osz_tracker():
    while True:
        try:
            osz_files = os.listdir(downloads_dir)
            for i in osz_files:
                try:
                    if i.split('.')[-1] == "osz":
                        os.startfile(f"{downloads_dir}{i}")
                except:
                    pass
        except:
            pass
        sleep(3)


def make_icon_image(size: int = 64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((2, 2, size-2, size-2), fill=(255, 105, 180, 255))
    d.arc((6, 6, size-6, size-6), 20, 160, width=3, fill=(255, 255, 255, 255))
    d.arc((10, 10, size-10, size-10), 200, 340, width=3, fill=(255, 255, 255, 255))
    d.arc((14, 14, size-14, size-14), 110, 250, width=3, fill=(255, 255, 255, 255))
    return img


def run_tray(stop_event: threading.Event, watcher_thread: threading.Thread) -> None:
    def on_exit(icon: pystray.Icon, item):
        stop_event.set()
        icon.visible = False
        icon.stop()

    menu = pystray.Menu(pystray.MenuItem("Exit", on_exit))
    icon = pystray.Icon("osu_osz_tracker", make_icon_image(),
                        title="osu! OSZ Tracker", menu=menu)
    icon.run()


def main():
    stop_event = threading.Event()
    watcher = threading.Thread(target=osz_tracker, daemon=True)
    watcher.start()
    try:
        run_tray(stop_event, watcher)
    finally:
        stop_event.set()
        watcher.join(timeout=3)


if __name__ == "__main__":
    main()
