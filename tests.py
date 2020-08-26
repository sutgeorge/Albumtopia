from controller import Controller

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

    def run_all_tests(self):
        self.test_search_album()