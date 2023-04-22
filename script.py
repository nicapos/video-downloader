import streamlit as st
from pytube import YouTube
import ssl, io, requests

ssl._create_default_https_context = ssl._create_unverified_context

def get_video_title(url):
    page = requests.get(url)
    inner_html = page.text

    start_index = inner_html.find('<title>') + 7
    end_index = inner_html.find('</title')

    return inner_html[start_index:end_index][:-10]

def download(url, download_type):
    video = YouTube(url)
    filename = get_video_title(url)
    data = None

    if download_type == 'Audio':
        data = video.streams.get_audio_only()
        filename += ".mp3"
    elif download_type == 'Highest Resolution':
        data = video.streams.get_highest_resolution()
        filename += ".mp4"
    elif download_type == 'Lowest Resolution':
        data = video.streams.get_lowest_resolution()
        filename += ".mp4"

    buffer = io.BytesIO()
    data.stream_to_buffer(buffer)

    return filename, buffer


def main():
    st.title("Video Downloader")
    video_url = st.text_input('Enter video URL')

    dl_types = ('Audio', 'Highest Resolution', 'Lowest Resolution')
    download_type = st.selectbox('Select download type', dl_types)

    btn_slot = st.empty()
    msg_slot = st.empty()

    download_btn = btn_slot.button('Convert')

    if video_url:
        st.video(video_url)
        msg_slot.empty()

    if download_btn:
        msg_slot.text("Converting video...")
        filename, data = download(video_url, download_type)
        msg_slot.text("Converted video. Ready for download.")

        btn_slot.download_button("Download", data, filename)

if __name__ == '__main__':
    main()