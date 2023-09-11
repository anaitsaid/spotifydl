from django import forms

class SpotifyDownloadForm(forms.Form):
    url = forms.URLField(label='Spotify Song URL')
