from controller import Controller
import os

class Tests:
    def __init__(self):
        self.controller = Controller()
        self.run_all_tests()

    def test_search_album(self):
        band_name = "Yes"
        album_title = "Close To The Edge"
        results = self.controller.search_album(band_name, album_title)
        assert(len(results) != 0)

        for result in results:
            lowercase_album_title = result['title'].lower().replace("̲", "")
            assert(band_name.lower() in lowercase_album_title and album_title.lower() in lowercase_album_title and "full album" in lowercase_album_title)

        print("Album search test passed.")

    def test_download_album(self):
        try:
            self.controller.download_youtube_video("Nails", "Unsilent Death")
            print("Album downloading test passed.")
        except Exception as e:
            print(e)
            assert(False)

    def test_create_search_query(self):
        search_query = self.controller.create_search_query("  Rush     ", "    Moving  pictures  ")
        assert(search_query == "https://www.discogs.com/search/?q=rush+moving+pictures&type=all")
        print("Search query creation test passed.")

    def test_get_album_link_from_discogs(self):
        album_link = self.controller.get_album_link_from_discogs(" Asylum party  ", "borderline  ")
        assert(album_link == "https://www.discogs.com/Asylum-Party-Borderline/master/11882")
        print("Album link scraping test passed.")

    def test_get_album_tracklist(self):
        link = self.controller.get_album_link_from_discogs("King Crimson", "Red")
        (song_titles, song_durations) = self.controller.get_album_tracklist(link)
        assert(song_titles == ['Red', 'Fallen Angel', 'One More Red Nightmare', 'Providence', 'Starless'])
        assert(song_durations == ['6:20', '6:00', '7:07', '8:08', '12:18'])
        print("Album tracklist extraction test passed.")

    def test_download_into_directory(self):
        self.controller.download_into_directory("Warsaw", "Joy Division")
        os.chdir("./downloads")
        assert("Warsaw - Joy Division" in os.listdir())
        print("Directory path download test passed.")

    def run_all_tests(self):
        self.test_search_album()
        #self.test_download_album()
        self.test_create_search_query()
        self.test_get_album_link_from_discogs()
        self.test_get_album_tracklist()
        self.test_download_into_directory()