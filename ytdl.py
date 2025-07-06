import yt_dlp

video_url = 'https://www.youtube.com/shorts/RRDhGHcun-0'

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',     # 同時選擇最佳影片+音訊
    'outtmpl': '%(title)s.%(ext)s',           # 儲存檔名為影片標題
    'merge_output_format': 'mp4',             # 合併輸出為 mp4 檔    
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])


#yt-dlp https://www.youtube.com/watch?v=Bu4D4lef9KM -f bestvideo+bestaudio --merge-output-format mp4