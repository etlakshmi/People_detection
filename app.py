import streamlit as st
from tracker import process_video


st.set_page_config(page_title="Zone-wise People Counter", layout="centered")

st.title("👥 Zone-wise Unique People Counter")

video_file = st.file_uploader("Upload CCTV Video", type=["mp4", "avi"])

if video_file:
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.read())

    st.video("temp_video.mp4")

    if st.button("Run Analysis"):
        with st.spinner("Processing video..."):
            zone_a, zone_b = process_video("temp_video.mp4")

        st.success("Analysis Complete")

        col1, col2 = st.columns(2)
        col1.metric("Zone A (Top)", zone_a)
        col2.metric("Zone B (Bottom)", zone_b)
