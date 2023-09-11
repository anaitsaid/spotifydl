from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_spotify, name='download_spotify'),
    path('downloaded-songs/', views.downloaded_songs, name='downloaded_songs'),
    path("<path:path>/", views.dl_song, name="dl_song")
]
