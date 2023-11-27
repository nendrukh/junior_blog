from googleapiclient.discovery import build
from config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)
video_id = "oQY1VouspmM"

request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
response = request.execute()

print(response["items"][0]["snippet"]["title"])
print(response["items"][0]["snippet"]["channelTitle"])
print(response)
