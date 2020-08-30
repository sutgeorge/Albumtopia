import requests
import datetime
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
        filename = (band_name + " - " + album_name + ".mp3").replace(" ", "_")
        options = {
            'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': filename,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]}

        with YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

    def download_into_directory(self, band_name, album_title):
        if not os.path.exists("./downloads"):
            os.mkdir("downloads")
        os.chdir("./downloads")
        self.new_directory_name = ("./" + band_name + " - " + album_title + "/").replace(" ", "_")
        if not os.path.exists(self.new_directory_name):
            os.mkdir(self.new_directory_name)
        os.chdir(self.new_directory_name)
        self.download_youtube_video(band_name, album_title)
        os.chdir("../../")

    def create_search_query(self, band_name, album_title):
        search_term = (band_name + " " + album_title).strip().lower()
        search_term = re.sub(" \s+", " ", search_term).replace(" ", "+")
        request_url = "https://www.discogs.com/search/?q=" + search_term + "&type=all"
        return request_url

    def get_album_links_from_discogs(self, band_name, album_title):
        search_query = self.create_search_query(band_name, album_title)
        result = requests.get(search_query)
        page_source = result.content
        soup = BeautifulSoup(page_source, "lxml")
        links = soup.find_all("a", "search_result_title")
        if len(links) == 0:
            print("No search found!")
            return 404

        valid_links = []
        for index in range(0, len(links)):
            tokens = album_title.strip().lower().split(" ")
            valid = True
            for token in tokens:
                if token not in links[index].attrs["href"].lower():
                    valid = False
                    break

            if valid:
                valid_links.append("https://www.discogs.com" + links[index].attrs["href"])

        return valid_links

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

    def check_tracklength_validity(self, song_durations):
        for song_duration in song_durations:
            if len(song_duration) > 0:
                return True
        return False

    def sanitize_filename(self, filename):
        characters = [' ', '(', ')', ',', ';', ':', '"', '\'', '&', '.']
        for char in characters:
            if char in filename:
                filename = filename.replace(char, "_")
        filename += ".mp3"
        return filename

    def split_audio_in_tracks(self, band_name, album_title):
        filename = band_name + "_-_" + album_title
        filename = self.sanitize_filename(filename)
        self.download_into_directory(band_name, album_title)
        os.chdir("./downloads/" + self.new_directory_name[2:])
        total_time = datetime.timedelta(minutes=0, seconds=0)
        invalid_song_durations = True
        album_links = self.get_album_links_from_discogs(band_name, album_title)

        while invalid_song_durations:
            album_link = album_links[0]
            (song_titles, song_durations) = self.get_album_tracklist(album_link)
            if self.check_tracklength_validity(song_durations) == False:
                del album_links[0]
                continue

            invalid_song_durations = False
            for song_index in range(0, len(song_titles)):
                song_length_tokens = song_durations[song_index].split(":")
                song_length_tokens = list(map(lambda x: int(x), song_length_tokens))
                song_duration_in_seconds = song_length_tokens[0] * 60 + song_length_tokens[1]

                timestamp = self.convert_timestamp_string_to_ints(song_durations[song_index])
                current_duration = datetime.timedelta(minutes=timestamp["minutes"], seconds=timestamp["seconds"])
                start_time = total_time.total_seconds()
                total_time += current_duration

                song_title = self.sanitize_filename(song_titles[song_index])
                os.system("ffmpeg -t {} -ss {} -i {} {}".format(song_duration_in_seconds, start_time, filename, song_title))

        os.remove(filename)
        os.chdir("../../")
