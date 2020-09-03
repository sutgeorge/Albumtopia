from controller import Controller

class Console:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        print("Welcome!")
        band_name = input("Type the artist name: ")
        album_title = input("Type the album title: ")

        self.controller.split_audio_in_tracks(band_name, album_title)
