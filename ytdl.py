import os
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtu(?:\.be\/|be\.com\/watch\?v=)([\w-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_title(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title_element = soup.find("meta", itemprop="name")
    if title_element:
        return title_element["content"]
    else:
        return None
    
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_txt(transcript, video_id, title):
    if transcript:
        if title is None:
            title = video_id
        filename = f"{title}_transcript.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for item in transcript:
                f.write(item['text'] + "\n")
        print(f"Transcript saved to {filename}")
    else:
        print("Could not save transcript.")

if __name__ == "__main__":
    while True:
        url = input("Please enter a YouTube video URL or type 'quit' to exit: ").strip()

        if url.lower() == 'quit':
            break

        video_id = extract_video_id(url)

        if video_id:
            title = get_video_title(video_id)
            if title:
                print(f"Video title: {title}")
            else:
                print("Could not fetch video title.")
            
            transcript = get_transcript(video_id)
            save_to_txt(transcript, video_id, title)
        else:
            print("Invalid YouTube URL. Please try again.")