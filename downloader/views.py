from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import os
import logging

logger = logging.getLogger(__name__)

try:
    import yt_dlp
except ImportError:
    logger.error("yt-dlp is not installed")
    yt_dlp = None

def home(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        print(f"URL received: {url}")  # Debugging statement
        if url:
            if yt_dlp is None:
                return render(request, 'downloader/home.html', {'message': 'Error: yt-dlp is not installed. Please install it using "pip install yt-dlp"'})
            try:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return render(request, 'downloader/home.html', {'message': 'Download successful!'})
            except Exception as e:
                print(f"Error: {str(e)}")  # Debugging statement
                return render(request, 'downloader/home.html', {'message': f'Error: {str(e)}'})
    return render(request, 'downloader/home.html')
