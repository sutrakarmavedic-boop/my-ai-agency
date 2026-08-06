import streamlit as st
import os
import urllib.parse
import random
from langchain_groq import ChatGroq

# --- APP UI SETUP ---
st.set_page_config(page_title="AI Business Empire", layout="wide")
st.title("🎬 My 8-Employee AI Business & Video App")

# --- SIDEBAR (Key वाला ऑप्शन यहाँ है, पर खाली है) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    # यह पहले Secrets में चाबी ढूंढेगा, अगर नहीं मिली तो खाली रहेगा
    saved_key = st.secrets.get("GROQ_API_KEY", "")
    groq_key = st.text_input("Enter Groq API Key:", type="password", value=saved_key)
    st.write("---")
    if groq_key:
        st.success("API Key Active 🟢")
    else:
        st.warning("Please enter API Key")

# इमेज और वीडियो जनरेट करने का फंक्शन
def generate_ai_content(name, topic, content_type="image"):
    seed = random.randint(1, 999999)
    clean_name = name.replace(" ", "-")
    prompt = f"Professional-3D-cinematic-visual-for-{clean_name}-in-{topic}-industry-high-quality-4k"
    encoded_prompt = urllib.parse.quote(prompt)
    if content_type == "video":
        return f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=video"
    else:
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"

# --- MAIN LOGIC ---
if groq_key:
    try:
        llm = ChatGroq(groq_api_key=groq_key, model_name="llama-3.3-70b-versatile")
        
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name:")
        with col2:
            biz_topic = st.text_input("Topic/Industry:")

        if st.button("Activate Agents & Generate Content"):
            if biz_name and biz_topic:
                with st.status("CEO Agent is working...") as status:
                    # 1. Text
                    res_text = llm.invoke(f"Business: {biz_name}. Topic: {biz_topic}. Write a short viral script and email.").content
                    # 2. Media
                    img_url = generate_ai_content(biz_name, biz_topic, "image")
                    video_url = generate_ai_content(biz_name, biz_topic, "video")

                    st.divider()
                    st.subheader("📬 Business Strategy")
                    st.info(res_text)
                    st.subheader("🎬 AI Motion Clip")
                    st.video(video_url)
                    st.subheader("🖼️ Reel Thumbnail")
                    st.image(img_url, use_container_width=True)
                    status.update(label="Complete!", state="complete")
            else:
                st.error("Fill all boxes")
    except Exception as e:
        st.error(f"Error: {e}")