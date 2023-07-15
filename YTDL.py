from pytube import YouTube, Playlist
import os
import unicodedata


def to_ascii(string):
    """
    Convert string to ASCII, replacing non-ASCII characters with their closest ASCII equivalents.
    """
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode()


def rename_filename(txt, file_format):
    """
    Convert a string to a valid filename
    :param txt: the string to be renamed
    :param file_format: a suffix to be added at the end of the filename (e.g. ".mp3")
    :return: the transformed filename
    """
    if len(txt) >= 10:
        txt = txt[:10]
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.']
    filename = to_ascii(txt)
    for c in illegal_chars:
        filename = filename.replace(c, "")
    filename += "." + file_format
    return filename


def download_from_url(url, file_format, out_path, _yt=None):
    """
    :param url: (str) Link to the YouTube video
    :param file_format: (str) file format, either "mp3" or "mp4"
    :param out_path: (str) local output path
    :param _yt: (Optional) a Pytube YouTube object, to skip an obsolete step if needed
    :return: 0 if successful, -1 if there was an error
    """
    try:
        if _yt is None:
            _yt = YouTube(url)
    except Exception as e:
        print("Error getting video from playlist")
        print(e)
        return -1
    if file_format == "mp3":
        video = _yt.streams.filter(only_audio=True).first()
    if file_format == "mp4":
        video = _yt.streams.filter().first()

    print(f"Found {video.title}")
    filename = rename_filename(video.title, file_format)

    if os.path.exists(out_path + "\\" + filename):
        print("Already exists, skipping")
        return

    print(f"Downloading \"{filename}\"...")
    video.download(filename=filename, output_path=out_path)
    abs_path = os.path.abspath(out_path)
    print(f"Downloaded {filename} to {abs_path}\\{filename}")
    return 0


print("###############################################")
print("#                                             #")
print("#           Youtube video downloader          #")
print("#                                             #")
print("###############################################")

while True:
    download_format = ""
    output_path = "downloads/out_"
    download_url = ""
    yt = None

    while "youtube" not in download_url:
        download_url = input("\n\nPlease input the video/playlist URL:\n")

        try:
            if "playlist" in download_url:
                playlist = Playlist(download_url)
                playlist.title

            if "video" in download_url:
                yt = YouTube(download_url)

        except Exception as e:
            print("The link you entered is wrong, or the video/playlist is unavailable/private")
            print(f"ERROR: {e}")
            download_url = ""

    valid_responses = ["1", "2", "mp3", "mp4"]
    while download_format not in valid_responses:
        download_format = input("Do you want to save the video as an mp3, or mp4?:\n"
                                "[1] mp4\n"
                                "[2] mp3\n")
        download_format = download_format.lower()

    if download_format == "1" or download_format == "mp4":
        download_format = "mp4"

    if download_format == "2" or download_format == "mp3":
        download_format = "mp3"

    output_path += download_format

    if "playlist" in download_url:
        output_path += "_playlist"
        video_urls = playlist.video_urls
        count = 0
        playlist_length = playlist.length
        for i in playlist:
            count += 1
            download_from_url(i, download_format, output_path)
            print(f"{count}/{playlist_length}")

    if "watch" in download_url:
        download_from_url(download_url, download_format, output_path, yt)
