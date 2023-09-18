import pytube
import os
from tqdm import tqdm


def progress_bar(stream, chunk, bytes_remaining):
    global pbar
    current = stream.filesize - bytes_remaining
    pbar.update(current - pbar.n)


# Set the download location to the user's desktop
user_home = os.path.expanduser("~")
desktop_loc = os.path.join(user_home, "Desktop")

# List the existing folders on the desktop
print("Existing folders:")
folders = [folder for folder in os.listdir(desktop_loc) if os.path.isdir(os.path.join(desktop_loc, folder))]
for folder in folders:
    print(f"- {folder}")

# Ask the user to enter the desired folder name or choose an existing one
folder_name = input("Enter the folder name for the downloaded video or choose from the list above: ")

# Create the chosen folder on the desktop if it doesn't exist
download_loc = os.path.join(desktop_loc, folder_name)
if not os.path.exists(download_loc):
    os.makedirs(download_loc)

# ask the user to enter url of youTube video
video_url = input('Enter url: ')

# Create an instance of youtube video
try:
    video_instance = pytube.YouTube(video_url)
except pytube.exceptions.RegexMatchError:
    print("The provided URL is not a valid YouTube video URL. Please try again.")
    exit(1)

try:
    # Get the highest resolution stream
    stream = video_instance.streams.get_highest_resolution()
except KeyError as e:
    print(f"An error occurred while extracting video information: {e}")
    exit(1)


# get the highest resolution
stream = video_instance.streams.get_highest_resolution()

# Create the progress bar
with tqdm(total=stream.filesize, unit='B', unit_scale=True, ncols=100) as pbar:
    video_instance.register_on_progress_callback(progress_bar)
    stream.download(download_loc)

