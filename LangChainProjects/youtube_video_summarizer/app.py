import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API Key not found. Please set it in your .env file as OPENAI_API_KEY.")
    st.stop()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=OPENAI_API_KEY)


# Prompt Template
prompt_template = PromptTemplate(
                    input_variables=["transcript"],
                    template="""
                        You are a professional content summarizer.  
                        Summarize the following YouTube video transcript into **main points** and a concise summary.  
                        Provide a structured summary with bullet points.

                        Transcript:
                        {transcript}

                        Summary:
                    """
                )

# Create Chain
chain = LLMChain(llm=llm, prompt=prompt_template)


# --- Function to extract YouTube video ID ---
def get_youtube_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    return None

# --- Function to fetch transcript ---
def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript_list])
        return transcript_text
    except Exception as e:
        st.error(f"❌ Could not fetch transcript: {e}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Video Summarizer", page_icon="🎬")

st.title("🎬 YouTube Video Summarizer")
st.write("Enter a YouTube URL to generate a summarized version of the video with main points.")

youtube_url = st.text_input("YouTube URL")

if st.button("Generate Summary"):
    if youtube_url:
        video_id = get_youtube_video_id(youtube_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL")
        else:
            transcript_text = fetch_transcript(video_id)

            if transcript_text:
                summary = chain.run({"transcript" : transcript_text})
                # Generate Summary
                with st.spinner("Generating summary..."):
                    summary = chain.run({"transcript": transcript_text})

                st.subheader("📝 Video Summary")
                st.write(summary)

                # Download option
                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name="video_summary.txt",
                    mime="text/plain"
                )
    else:
        st.warning("⚠️ Please enter a YouTube URL.")
