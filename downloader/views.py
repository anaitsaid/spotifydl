import os
from django.shortcuts import render, redirect
from .forms import SpotifyDownloadForm
from .models import DownloadedSong
import subprocess
from django.http import FileResponse
from django.conf import settings

def download_song(url):
    try:
        # Run spotdl to download the song to the "songs" folder
        subprocess.run(["spotdl", "--output", "songs/", url], check=True)

        # Get the list of filenames in the "songs" directory
        song_files = os.listdir("songs")

        # Create a list of tuples containing filename and modification time
        file_and_time = [(filename, os.path.getmtime(os.path.join("songs", filename))) for filename in song_files]

        # Sort the list based on modification time (newest first)
        file_and_time.sort(key=lambda x: x[1], reverse=True)

        # Extract sorted filenames
        sorted_song_files = [filename for filename, _ in file_and_time]

        # Get the last downloaded file
        if song_files:
            last_downloaded_file = sorted_song_files[0]
            print(last_downloaded_file)

            # Use the last downloaded file name as the song title
            song_title, _ = os.path.splitext(last_downloaded_file)

            # Construct the destination file path
            destination_path = os.path.join("songs", last_downloaded_file)
            print(destination_path)

            return song_title, destination_path
        else:
            print("Error: No song files found in the 'songs' folder")
            return None, None

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def download_spotify(request):
    if request.method == 'POST':
        form = SpotifyDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # Download the song
            song_title, destination_path= download_song(url)

            os.rename(destination_path, destination_path.replace(' ', '_'))
            destination_path = destination_path.replace(' ', '_')

            # Save the downloaded song to the database
            DownloadedSong.objects.create(title=song_title, url=url, file=destination_path)

            return redirect('downloaded_songs')
    else:
        form = SpotifyDownloadForm()

    return render(request, 'downloader/download_spotify.html', {'form': form})

def downloaded_songs(request):
    songs = DownloadedSong.objects.all()
    return render(request, 'downloader/downloaded_songs.html', {'songs': songs})

def dl_song(request, path):
    response = FileResponse(open(str(settings.BASE_DIR) + path.replace("/", "\\"), "rb"), as_attachment=True)
    return response
