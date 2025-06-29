from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
import os
import logging
import re
import json
from urllib.parse import urlparse

# Import models but handle if migrations haven't run yet
try:
    from .models import Download
    models_available = True
except Exception:
    models_available = False

logger = logging.getLogger(__name__)

try:
    import yt_dlp
except ImportError:
    logger.error("yt-dlp is not installed")
    yt_dlp = None

def detect_platform(url):
    """Detect which platform the URL belongs to"""
    print(f"Detecting platform for URL: {url}")
    
    domain_patterns = {
        'youtube': [r'youtube\.com', r'youtu\.be', r'youtube-nocookie\.com'],
        'instagram': [r'instagram\.com', r'instagr\.am'],
        'tiktok': [r'tiktok\.com', r'vm\.tiktok\.com'],
        'twitter': [r'twitter\.com', r'x\.com', r't\.co'],
        'facebook': [r'facebook\.com', r'fb\.watch', r'fb\.me'],
        'pinterest': [r'pinterest\.com', r'pin\.it'],
    }
    
    parsed_url = urlparse(url.lower())
    domain = parsed_url.netloc.replace('www.', '')
    print(f"Parsed domain: {domain}")
    
    for platform, patterns in domain_patterns.items():
        for pattern in patterns:
            if re.search(pattern, domain):
                print(f"Platform detected: {platform}")
                return platform
    
    print("Platform not detected, defaulting to youtube")
    return 'youtube'

def get_video_info(url, platform):
    """Get video information without downloading"""
    print(f"Getting video info for {platform} URL: {url}")
    
    if yt_dlp is None:
        return {'error': 'yt-dlp is not installed'}
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'writeinfojson': False,
            'writedescription': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Video info extracted: {info.get('title', 'No title')}")
            
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': str(info.get('duration', 0)) + 's' if info.get('duration') else 'Unknown',
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'formats': [
                    {
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'quality': f.get('height', 0),
                        'filesize': f.get('filesize', 0)
                    }
                    for f in info.get('formats', []) if f.get('height')
                ][:5]  # Limit to 5 formats
            }
    except Exception as e:
        print(f"Error getting video info: {str(e)}")
        return {'error': str(e)}

def home(request):
    print("Home view accessed")
    return render(request, 'downloader/home.html')

@csrf_exempt
@require_http_methods(["POST"])
def get_info(request):
    """AJAX endpoint to get video information"""
    print("Get info endpoint called")
    
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        print(f"URL received for info: {url}")
        
        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)
        
        platform = detect_platform(url)
        info = get_video_info(url, platform)
        
        if 'error' in info:
            return JsonResponse({'error': info['error']}, status=400)
        
        print(f"Returning info for: {info.get('title', 'Unknown')}")
        return JsonResponse({
            'platform': platform,
            'title': info['title'],
            'duration': info['duration'],
            'thumbnail': info['thumbnail'],
            'uploader': info['uploader'],
            'view_count': info['view_count'],
            'formats': info['formats']
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error in get_info: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  
@require_http_methods(["POST"])
def download_video(request):
    """AJAX endpoint to download video"""
    print("Download video endpoint called")
    
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        quality = data.get('quality', 'best')
        print(f"Download request - URL: {url}, Quality: {quality}")
        
        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)
        
        if yt_dlp is None:
            return JsonResponse({'error': 'yt-dlp is not installed'}, status=500)
        
        platform = detect_platform(url)
        
        # Save to database if available
        download_record = None
        if models_available:
            try:
                download_record = Download.objects.create(
                    url=url,
                    platform=platform,
                    quality=quality,
                    status='processing',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                print(f"Download record created with ID: {download_record.id}")
            except Exception as e:
                print(f"Failed to create download record: {str(e)}")
        
        try:
            # Create downloads directory if it doesn't exist
            os.makedirs('downloads', exist_ok=True)
            
            ydl_opts = {
                'format': quality if quality != 'best' else 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'restrictfilenames': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                print(f"Starting download: {title}")
                
                # Update database record
                if download_record:
                    download_record.title = title
                    download_record.thumbnail_url = info.get('thumbnail', '')
                    download_record.duration = str(info.get('duration', 0)) + 's' if info.get('duration') else ''
                    download_record.save()
                
                # Download the video
                ydl.download([url])
                
                # Update status to completed
                if download_record:
                    download_record.status = 'completed'
                    download_record.download_count += 1
                    download_record.save()
                
                print(f"Download completed: {title}")
                return JsonResponse({
                    'success': True,
                    'message': f'Successfully downloaded: {title}',
                    'title': title
                })
                
        except Exception as e:
            print(f"Download error: {str(e)}")
            
            # Update status to failed
            if download_record:
                download_record.status = 'failed'
                download_record.error_message = str(e)
                download_record.save()
            
            return JsonResponse({'error': f'Download failed: {str(e)}'}, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Unexpected error in download_video: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
