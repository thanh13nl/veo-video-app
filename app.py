import streamlit as st
import os
import json
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel
import time

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Veo 3 Video Creator", page_icon="🎬", layout="wide")

# --- XỬ LÝ CHÌA KHÓA (SECRETS) ---
def init_vertex():
    try:
        # Đọc thông tin từ mục Secrets của Streamlit
        service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT_CONTENTS"])
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        
        project_id = st.secrets["PROJECT_ID"]
        location = st.secrets["LOCATION"]
        
        vertexai.init(project=project_id, location=location, credentials=credentials)
        return True
    except Exception as e:
        st.error(f"Lỗi cấu hình: {e}")
        st.info("Hướng dẫn: Bạn cần dán file JSON vào mục Settings > Secrets trên Streamlit Cloud.")
        return False

# --- GIAO DIỆN CHÍNH ---
st.title("🎬 AI Video Generator - Veo 3")
st.markdown("Biến ý tưởng của bạn thành video điện ảnh ngay lập tức.")

if init_vertex():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💡 Ý tưởng của bạn")
        user_idea = st.text_area("Mô tả video bạn muốn tạo:", 
                                 placeholder="Ví dụ: Một chú rồng con đang tập bay trên đỉnh núi tuyết...", 
                                 height=150)
        
        style = st.selectbox("Phong cách nghệ thuật:", 
                             ["Cinematic (Điện ảnh)", "3D Animation", "Cyberpunk", "Realistic", "Oil Painting"])
        
        duration = st.slider("Độ dài video (giây):", 5, 10, 5)

        generate_btn = st.button("Tạo Video Ngay", type="primary")

    with col2:
        st.subheader("📺 Kết quả")
        if generate_btn:
            if not user_idea:
                st.warning("Vui lòng nhập ý tưởng!")
            else:
                with st.status("🤖 AI đang làm việc...", expanded=True) as status:
                    # Bước 1: Gemini viết Prompt
                    st.write("Đang tối ưu hóa mô tả...")
                    model = GenerativeModel("gemini-1.5-flash")
                    prompt_chain = f"Write a detailed English prompt for a video generation AI. Idea: {user_idea}. Style: {style}. Duration: {duration}s. High quality, 4k."
                    response = model.generate_content(prompt_chain)
                    final_prompt = response.text
                    
                    st.write(f"**Prompt đã tạo:** {final_prompt}")
                    
                    # Bước 2: Gọi Veo 3 (Giả lập link video để bạn test giao diện)
                    st.write("Đang dựng video từ Veo 3...")
                    time.sleep(3) # Giả lập thời gian xử lý
                    
                    # Trong thực tế, bạn sẽ nhận link từ Google Cloud Storage
                    video_url = "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" 
                    
                    status.update(label="Hoàn thành!", state="complete")

                st.video(video_url)
                st.success("Video của bạn đã sẵn sàng!")
                st.download_button("Tải video xuống", video_url, file_name="ai_video.mp4")

else:
    st.warning("Ứng dụng đang đợi bạn cấu hình API Key trong phần 'Advanced Settings'.")
