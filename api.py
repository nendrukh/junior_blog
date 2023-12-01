from googleapiclient.discovery import build
from config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)
videos = {"oQY1VouspmM": "Очень полезное видео по всяким айтишным фишкам/лайфхакам",
          "NEhB61CHDcM": "Крутой псевдо-собес, на котором задают неочевидные вопросы для джуна (но в целом база)"
          }

result = dict()
for id_video, description in videos.items():
    request = youtube.videos().list(part="snippet,contentDetails", id=id_video)
    response = request.execute()

    url = "https://www.youtube.com/watch?v=" + id_video
    result[url] = {"title": response["items"][0]["snippet"]["title"],
                   "description": description,
                   "channel_name": response["items"][0]["snippet"]["channelTitle"]
                   }
