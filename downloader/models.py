from django.db import models
from django.utils import timezone

class Download(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
    ]
    
    QUALITY_CHOICES = [
        ('best', 'Best Quality'),
        ('worst', 'Lowest Quality'),
        ('720p', '720p HD'),
        ('480p', '480p SD'),
        ('360p', '360p'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    url = models.URLField(max_length=1000)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    title = models.CharField(max_length=500, blank=True)
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='best')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    file_path = models.CharField(max_length=1000, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=20, blank=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.platform.title()} - {self.title[:50] or self.url[:50]}"
