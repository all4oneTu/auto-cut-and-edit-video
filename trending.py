from googleapiclient.discovery import build

def get_trending_music_videos(api_key, max_results=30):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode="VN",  # Mã quốc gia của Việt Nam (bạn có thể thay đổi nếu cần)
        videoCategoryId="10",  # ID của danh mục video "Âm nhạc"
        maxResults=max_results
    )

    response = request.execute()
    # print(response['items'][0])
    videos = []
    for item in response['items']:
        
        videos.append(item['snippet']['title'])

    return videos

# Thay thế 'YOUR_API_KEY' bằng khóa API YouTube của bạn
api_key = 'AIzaSyC_V4rnMFEdj05MLkyK0HhF0SjP9lokms4'
trending_music_videos = get_trending_music_videos(api_key)

print("Danh sách các video âm nhạc thịnh hành trên YouTube:")
for index, video_title in enumerate(trending_music_videos, start=1):
    print(f"{index}. {video_title}")
