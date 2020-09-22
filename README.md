# Albumtopia
A simple Python program which automatically downloads a full album from Youtube and scrapes album and track details from discogs.com to tag the tracks with proper metadata (track title, album name, artist name, album cover etc.) 

## Dependencies

* ffmpeg
    - Linux

        Good tutorial: https://www.hostinger.com/tutorials/how-to-install-ffmpeg

    - Windows
        
        For Windows, download these executables and place the directory in the PATH environment variable: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.zip

* Modules 

    To install the modules, type this in the terminal:

    ```
    pip install -r requirements.txt
    ```

    ...or if there's any issue with pip, use pip3:

    ```
    pip3 install -r requirements.txt
    ```

## Current state
![Demo](https://github.com/Calandrinon/Albumtopia/blob/master/res/demo.gif)


## Features to implement
- [X] Add automatic Youtube download
- [X] Extract song lengths from discogs.com
- [X] Split mp3 album properly in separate tracks
- [X] Validate discogs.com links to extract correct song lengths
- [X] Add metadata to each track
- [X] Create a simple console UI
- [X] Implement separate track downloading
- [ ] Manually plugging a link instead of searching automatically 
- [ ] Use rateyourmusic.com as a back-up tracklist source 
