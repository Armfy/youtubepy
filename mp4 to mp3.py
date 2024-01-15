import importlib
import subprocess
import os
from tkinter import filedialog, Tk

try:
    importlib.import_module('moviepy')
except ImportError:
    subprocess.check_call(['pip', 'install', 'moviepy'])
    importlib.import_module('moviepy')

from moviepy.editor import VideoFileClip

def convert_to_mp3(file_path, save_path):
    video = VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile(save_path)
    audio.close()
    video.close()

root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[('MP4', '*.mp4')])
if file_path:
    default_save_path = os.path.splitext(file_path)[0] + '.mp3'
    
    save_path = filedialog.asksaveasfilename(defaultextension='.mp3', initialfile=default_save_path)

    if save_path:
        if os.path.exists(file_path):
            convert_to_mp3(file_path, save_path)
            print('Conversion completed successfully.')
        else:
            print('The specified input file does not exist.')
    else:
        print('No output file path selected.')
else:
    print('No file selected.')
