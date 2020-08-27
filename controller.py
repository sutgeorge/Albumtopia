import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL
import re, os

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
            'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': filename,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]}

        with YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

    def download_into_directory(self, band_name, album_title):
        os.chdir("./downloads")
        new_directory_name = "./" + band_name + " - " + album_title + "/"
        os.mkdir(new_directory_name)
        os.chdir(new_directory_name)
        self.download_youtube_video(band_name, album_title)
        os.chdir("../../")

    def create_search_query(self, band_name, album_title):
        search_term = (band_name + " " + album_title).strip().lower()
        search_term = re.sub(" \s+", " ", search_term).replace(" ", "+")
        request_url = "https://www.discogs.com/search/?q=" + search_term + "&type=all"
        return request_url

    def get_album_link_from_discogs(self, band_name, album_title):
        search_query = self.create_search_query(band_name, album_title)
        result = requests.get(search_query)
        page_source = result.content
        soup = BeautifulSoup(page_source, "lxml")
        links = soup.find_all("a", "search_result_title")
        if len(links) == 0:
            print("No search found!")
            return 404

        return "https://www.discogs.com" + links[0].attrs["href"]

    def get_album_tracklist(self, album_link):
        result = requests.get(album_link)
        tracklist_page = result.content
        soup = BeautifulSoup(tracklist_page, "lxml")
        tracklist_span_titles = soup.find_all("span", "tracklist_track_title")
        tracklist_durations = soup.find_all("td", "tracklist_track_duration")
        song_titles = list(map(lambda x: x.getText(), tracklist_span_titles))
        song_durations = list(map(lambda x: x.find("span").getText(), tracklist_durations))
        return (song_titles, song_durations)

    def convert_timestamp_string_to_ints(self, timestamp):
        timestamp_dictionary = {}
        time_units = list(map(lambda x: int(x), timestamp.split(":")))
        if len(time_units) == 3:
            timestamp_dictionary["hours"] = time_units[0]
            timestamp_dictionary["minutes"] = time_units[1]
            timestamp_dictionary["seconds"] = time_units[2]
        elif len(time_units) == 2:
            timestamp_dictionary["minutes"] = time_units[0]
            timestamp_dictionary["seconds"] = time_units[1]
        return timestamp_dictionary

    def split_audio_in_tracks(self):
        pass

    # search album on Youtube                                X
    # download the album in mp4 format                       X
    # convert mp4 to mp3                                     X
    # scrape track details from Discogs or Wikipedia         X
    # cut the mp3 at the right places