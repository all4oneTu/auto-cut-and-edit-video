from pytube import YouTube
from moviepy.editor import *
from pychorus import find_and_output_chorus
from pydub import AudioSegment
import re

video_title = ""
# Hàm tải video từ URL
def download_video(video_url):
    print("Đang tải video...")
    try:
        yt = YouTube(video_url)
        yt.streams.filter(progressive=True, file_extension='mp4').first().download(output_path="./", filename ="video.mp4")
        global video_title 
        video_title = yt.title
        print(f"Đã tải video thành công: {video_title}")
        return "video"
    except Exception as e:
        print("Đã xảy ra lỗi trong quá trình tải video:", e)

#Chuyển đổi video thành mp3
def convert_video_to_mp3(mp4_file, mp3_file):
    print("Đang chuyển đổi video sang mp3...")
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(mp3_file)
    audio.close()
    video.close()
    print(f"Đã chuyển đổi video thành công: {mp3_file}")

#Tim chorus
def find_chorus(mp3_file, video_name):
    print("Đang tìm chorus...")
    chorus_start_sec = find_and_output_chorus(mp3_file, video_name + ".wav", 20)
    return chorus_start_sec

#Cat file mp3 tu chorus_start dai 30s
def cut_mp3(mp3_file, chorus_start, output_file):
    print("Đang cắt mp3...")
    audio = AudioSegment.from_mp3(mp3_file)
    start_time = chorus_start * 1000
    end_time = start_time + 40000
    cut_audio = audio[start_time:end_time]
    cut_audio.export(output_file, format="mp3")
    print(f"Đã cắt mp3 thành công: {output_file}")


#Xoa file wav
def remove_wav(wav_file):
    os.remove(wav_file)
    print("Đã xóa file wav thành công")

#Chuyen doi file mp3 sang m4a
def convert_mp3_to_m4a(input_file, output_dir):
    try:
        # Kiểm tra xem thư mục đầu ra tồn tại không
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        input_filename = os.path.basename(input_file)
        output_file_path = os.path.join(output_dir, os.path.splitext(input_filename)[0] + ".m4a")
        
        # Kiểm tra xem file đã được chuyển đổi chưa
        if not os.path.exists(output_file_path):
            # Sử dụng ffmpeg để chuyển đổi từ MP3 sang M4A
            command = ['ffmpeg', '-i', f'"{input_file}"', '-acodec', 'aac', '-strict', 'experimental', f'"{output_file_path}"']
            os.system(" ".join(command))
            print(f"Chuyển đổi {input_filename} thành công.")
    
    except Exception as e:
        print("Đã xảy ra lỗi trong quá trình chuyển đổi:", e)

#Xoa file mp4 va mp3 voi ten video
def remove_files(video):
    mp4_file = video + ".mp4"
    mp3_file = video + ".mp3"
    os.remove(mp4_file)
    os.remove(mp3_file)
    print("Đã xóa file thành công")

#Loai bo cac ki tu dac biet
def normalize_filename(filename):
    # Loại bỏ các ký tự không hợp lệ từ tên file
    normalized_string = re.sub(r'[^\w\s]', ' ', filename)

     # Loại bỏ các khoảng trắng kép (nếu có)
    normalized_string = re.sub(r'\s+', ' ', normalized_string)

    # Loại bỏ khoảng trắng ở đầu và cuối chuỗi
    normalized_string = normalized_string.strip()

    return normalized_string

# URL của video cần tải
# video_url = "https://www.youtube.com/watch?v=s-lY9BEAnUM"

# Nhap url video
video_url = input("Nhập URL của video cần tải: ")
#Download video
video_name = download_video(video_url)

#Chuyển đổi video thành mp3
mp4_file = video_name + ".mp4"
mp3_file = video_name + ".mp3"
convert_video_to_mp3(mp4_file, mp3_file)

#Tìm chorus
chorus_start = find_chorus(mp3_file, "output")
print("Chorus bắt đầu từ:", chorus_start)

#Chinh sua ten file
video_title = normalize_filename(video_title)

#Cắt mp3 từ chorus_start đến 30s
cut_mp3(mp3_file, chorus_start, video_title + ".mp3")

# Xóa file wav
remove_wav("output.wav")

#Chuyển đổi file mp3 sang m4a
convert_mp3_to_m4a(video_title+".mp3", "output")

#Xóa file mp4 và mp3
remove_files("video")

