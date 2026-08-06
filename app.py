import streamlit as st
import os
import urllib.parse
import random
from langchain_groq import ChatGroq

# --- APP UI SETUP ---
st.set_page_config(page_title="AI Video Agency", layout="wide")
st.title("🎬 My 8-Employee AI Video Agency")

# --- SIDEBAR (Key Option) ---
with st.sidebar:
    st.header("⚙️ Settings")
    saved_key = st.secrets.get("GROQ_API_KEY", "")
    groq_key = st.text_input("Enter Groq API Key:", type="password", value=saved_key)
    st.write("---")
    st.success("Video Dept: Active 🎥")

# इमेज और वीडियो जनरेट करने का पक्का तरीका
def get_content_url(name, topic, mode="video"):
    seed = random.randint(1, 999999)
    # प्रॉम्ट को ऐसा बनाना कि मोशन (Video) अच्छा आए
    prompt = f"Cinematic 3D motion animation of {name} in {topic} industry, ultra high quality, 4k, moving lights"
    encoded_prompt = urllib.parse.quote(prompt)
    
    if mode == "video":
        # Pollinations का असली वीडियो जनरेटर लिंक
        return f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=video"
    else:
        # इमेज जनरेटर लिंक
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"

# --- MAIN LOGIC ---
if groq_key:
    try:
        llm = ChatGroq(groq_api_key=groq_key, model_name="llama-3.3-70b-versatile")
        
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name:", placeholder="e.g. Hitesh AI")
        with col2:
            biz_topic = st.text_input("Topic:", placeholder="e.g. Social Media")

        if st.button("Activate Agents & Create Video"):
            if biz_name and biz_topic:
                with st.status("CEO is generating your Viral Content...") as status:
                    # 1. Text Generation
                    st.write("📝 Copywriter is working...")
                    res_text = llm.invoke(f"Business: {biz_name}. Topic: {biz_topic}. Task: Write a short viral script for a Reel.").content
                    
                    # 2. URLs Generate करना
                    video_url = get_content_url(biz_name, biz_topic, "video")
                    img_url = get_content_url(biz_name, biz_topic, "image")

                    # --- RESULTS ---
                    st.divider()
                    st.subheader("📬 Viral Reel Script")
                    st.info(res_text)

                    st.subheader("🎬 AI Generated Motion Clip (Wait for Load)")
                    # वीडियो दिखाने का पक्का तरीका
                    st.video(video_url)
                    st.markdown(f"[🔗 Link to Video (अगर ऊपर लोड न हो)]({video_url})")

                    st.subheader("🖼️ Reel Thumbnail")
                    st.image(img_url, use_container_width=True)
                    
                    status.update(label="All Done!", state="complete")
            else:
                st.error("Please fill both boxes.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your Groq Key in the sidebar.")