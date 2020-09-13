from controller import Controller

class Console:
    def __init__(self, controller):
        self.controller = controller


    def __display_banner(self): 
        banner_file = open("res/banner.txt", "r")
        banner_file_lines = banner_file.readlines()
        for line in banner_file_lines:
            print(line, end="")
        print("Welcome!")


    def __display_options_message(self):
        print("Choose one of the following options: ")
        print("1. Download a full album as an mp3 and split it in separate tracks")
        print("2. Download each track of an album")
        print("There are 2 options because sometimes an album cannot be found as a full album in mp3.")
        print("Sometimes the separate tracks of the album cannot be found, but the full album in mp3 exists.")
        print("If you are dissatisfied with the result of an option, you can try the other.")
        print("In any case, you can create an issue at https://github.com/Calandrinon/Albumtopia/issues")


    def run(self):
        self.__display_banner()

        band_name = input("Type the artist name: ")
        album_title = input("Type the album title: ")

        self.__display_options_message()

        option = int(input("Enter the option number: "))
        print("Be patient. It can last a while... (2 minutes, in the worst case)")
        if option == 1:
            print("Option 1 running...")
            self.controller.split_audio_in_tracks(band_name, album_title)
        else:
            print("Option 2 running...")
            self.controller.download_tracks_separately(band_name, album_title)

