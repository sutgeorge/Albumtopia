import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL

class Controller:
    def __init__(self):
        pass

    def search_album(self, band_name, album_name):
        band_name, album_name = band_name.lower(), album_name.lower()
        search_string = band_name + " " + album_name + " full album"
        results = YoutubeSearch(search_string, max_results=10).to_dict()
        valid_results = []

        for result in results:
            lowercase_result_title = result['title'].lower().replace("̲", "")
            if band_name in lowercase_result_title and album_name in lowercase_result_title and "full album" in lowercase_result_title:
                valid_results.append(result)

        return valid_results

    def download_youtube_video(self, band_name, album_name):
        results = self.search_album(band_name, album_name)
        video_url = "https://www.youtube.com" + results[0]['url_suffix']
        video_info = YoutubeDL().extract_info(url=video_url, download=False)
        filename = band_name + " - " + album_name + ".mp3"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        }

        with YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])


    # search album on Youtube
    # download the album in mp4 format
    # convert mp4 to mp3
    # scrape track details from Discogs or Wikipedia
    # cut the mp3 at the right places