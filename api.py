from googleapiclient.discovery import build, Resource
from config import API_KEY


def get_video_info(video_id: str, description: str) -> dict:
    youtube: Resource = build("youtube", "v3", developerKey=API_KEY)

    result = dict()
    request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
    response = request.execute()

    url: str = "https://www.youtube.com/watch?v=" + video_id
    result["url"] = url
    result["title"] = response["items"][0]["snippet"]["title"]
    result["description"] = description
    result["channel_name"] = response["items"][0]["snippet"]["channelTitle"]

    return result
