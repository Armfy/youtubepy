import os
import subprocess
import sys

REQUIRED_PACKAGES = ['yt-dlp']

for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in REQUIRED_PACKAGES:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    except subprocess.CalledProcessError:
        pass

import threading
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp

def download_video():
    link = entry_link.get().strip()

    if not link:
        messagebox.showerror("Error", "Please enter a valid YouTube link.")
        return

    def download():
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=1080]',  # Download best video up to 1080p only
                'outtmpl': '%(title)s.%(ext)s',        # Set output filename template
                'progress_hooks': [hook],               # Hook for progress tracking
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            messagebox.showinfo("Download Successful", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            progress_bar.stop()
            progress_bar['value'] = 0

            answer = messagebox.askyesno("Download Another Video", "Do you want to download another video?")
            if answer:
                entry_link.delete(0, tk.END)
            else:
                window.quit()

    def hook(d):
        if d['status'] == 'downloading':
            progress_bar['value'] = d['downloaded_bytes'] / d['total_bytes'] * 100

    download_thread = threading.Thread(target=download)
    download_thread.start()

    progress_bar.start()

window = tk.Tk()
window.title("YouTube Video Downloader")
window.configure(bg='black')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 400
window_height = 250
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

label_link = tk.Label(window, text="Enter YouTube Video Link:", bg='black', fg='white')
label_link.pack(pady=10)

style = ttk.Style()
style.configure('TEntry', background='black', foreground='black', fieldbackground='black', borderwidth=0, relief='solid', padding=5)

entry_link = ttk.Entry(window, width=50, style='TEntry')
entry_link.pack()

button_download = tk.Button(window, text="Download", command=download_video, bg='gray', fg='white', relief='solid', bd=0, padx=10, pady=5)
button_download.configure(borderwidth=0, highlightthickness=0)
button_download.pack(pady=10)

progress_bar = ttk.Progressbar(window, mode='determinate', maximum=100, style='TProgressbar')
progress_bar.pack(pady=10)

style.configure('TProgressbar', background='black', troughcolor='black', bordercolor='white')

window.mainloop()
