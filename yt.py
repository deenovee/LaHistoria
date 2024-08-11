from pytubefix import YouTube
from sys import argv

def download_video():
    url = argv[1]
    country = argv[2]
    yt = YouTube(url)
    title = yt.title
    account = yt.author
    date = yt.publish_date
    yt.streams.get_highest_resolution().download(output_path=f"Media/Videos/{country}/")
    print(f"Downloaded {yt.title} from {country}")
    print(f"Title: {title}, Account: {account}, Date: {date}")

if __name__ == "__main__":
    download_video()