from django.db import models

class DownloadedSong(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    file = models.FileField(upload_to='songs/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

