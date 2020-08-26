import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch

class Controller:
    def __init__(self):
        pass


    def search_album(self, band_name, album_name):
        search_string = band_name + " " + album_name + " full album"
        results = YoutubeSearch(search_string, max_results=10).to_dict()
        valid_results = []

        for result in results:
            lowercase_result_title = result['title'].lower().replace("̲", "")
            if band_name in lowercase_result_title and album_name in lowercase_result_title and "full album" in lowercase_result_title:
                valid_results.append(result)

        return valid_results


    # search album on Youtube
    # download the album in mp4 format
    # convert mp4 to mp3
    # scrape track details from Discogs or Wikipedia
    # cut the mp3 at the right places