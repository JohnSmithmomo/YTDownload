import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import configparser
import threading
import os

# config.ini 初始設定
config_path = 'config.ini'
config = configparser.ConfigParser()
config.read(config_path)

quality_default = config.get('Settings', 'video_audio_quality', fallback='bestvideo+bestaudio/best')
path_default = config.get('Settings', 'download_path', fallback='')
subtitle_lang_default = config.get('Settings', 'subtitle_lang', fallback='en')

def hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0.0%')
        try:
            #percent = float(d['_percent_str'].replace('%','').strip())
            percent = float(percent_str.replace('%', '').strip())
        except Exception:
            #progressbar['value'] = 0
            percent = 0.0

        progressbar['value'] = percent
        progressbar.update_idletasks()  # 讓 GUI 即時刷新
        speed = d.get('_speed_str', '')
        eta = d.get('eta', '')
        status_label.config(text=f"下載中：{percent} | 速度：{speed} | 剩餘：{eta}s")

def save_config():
    config['Settings'] = {
        'video_audio_quality': quality_var.get(),
        'download_path': path_entry.get(),
        'subtitle_lang': subtitle_var.get()
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def threaded_download():
    url = url_entry.get()
    quality = quality_var.get()
    path = path_entry.get()
    subtitle_lang = subtitle_var.get()

    ydl_opts = {
        'format': quality,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'writesubtitles': True,
        'writeautomaticsub': True,          # 如果只用自動字幕
        'subtitleslangs': [subtitle_lang],  # 語言清單，如 ['en']
        'embedsubtitles': True,             # 內嵌字幕到 mp4（需 ffmpeg）
        'progress_hooks': [hook],
        'merge_output_format': 'mp4',
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="✅ 下載完成")
        save_config()
    except Exception as e:
        status_label.config(text=f"❌ 下載失敗：{e}")
def threaded_start_download():
    threading.Thread(target=threaded_download).start()
    
# GUI 設定
root = tk.Tk()
root.title("YouTube Downloader")

#建立元件
progressbar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progressbar.grid(row=5, column=1, columnspan=2, pady=10)

# URL 輸入欄
tk.Label(root, text="影片網址：").grid(row=0, column=0, sticky='e')
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# 畫質選項
tk.Label(root, text="畫質選擇：").grid(row=1, column=0, sticky='e')
quality_var = tk.StringVar(value=quality_default)
quality_menu = tk.OptionMenu(root, quality_var,
    'bestvideo+bestaudio/best',
    'best[height<=720]',
    'worst')
quality_menu.grid(row=1, column=1, sticky='w')

# 字幕選擇
tk.Label(root, text="字幕語言：").grid(row=1, column=2, sticky='e')
subtitle_var = tk.StringVar(value=subtitle_lang_default)
subtitle_menu = tk.OptionMenu(root, subtitle_var, 'en', 'zh-Hant', 'ja', 'es')
subtitle_menu.grid(row=1, column=3, sticky='w')

# 儲存路徑選擇
tk.Label(root, text="儲存路徑：").grid(row=2, column=0, sticky='e')
path_entry = tk.Entry(root, width=40)
path_entry.insert(0, path_default)
path_entry.grid(row=2, column=1, columnspan=2, sticky='w', padx=5)
browse_btn = tk.Button(root, text="瀏覽", command=browse_folder)
browse_btn.grid(row=2, column=3)


# 下載按鈕
download_btn = tk.Button(root, text="下載", width=20, command=threaded_start_download)
download_btn.grid(row=3, column=1, pady=10)

#status
status_label = tk.Label(root, text="", fg='blue')
status_label.grid(row=4, column=1, columnspan=2)

# 在下載成功後：
#status_label.config(text="下載完成")

root.mainloop()
