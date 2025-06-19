import streamlit as st
import requests
import tempfile
import base64

# Ambil API Key dari Streamlit Secrets
API_KEY = st.secrets["ELEVENLABS_API_KEY"]
API_URL = "https://api.elevenlabs.io/v1"

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🎙️ ElevenLabs Text to Speech")

# Mode Gelap Toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown(
        """<style>
        body { background-color: #1e1e1e; color: white; }
        textarea, input, select { background-color: #2e2e2e !important; color: white !important; }
        </style>""",
        unsafe_allow_html=True
    )

# Get voice list
def get_voices():
    headers = {"xi-api-key": API_KEY}
    r = requests.get(f"{API_URL}/voices", headers=headers)
    r.raise_for_status()
    voices = r.json().get("voices", [])
    return {f"{v['name']} ({v['voice_id']})": v["voice_id"] for v in voices}

with st.expander("📢 Pilih Voice"):
    voice_dict = get_voices()
    voice_name = st.selectbox("Voice:", list(voice_dict.keys()))
    voice_id = voice_dict[voice_name]

# Teks Input
text = st.text_area("📝 Masukkan Teks:", height=150)
word_count = len(text.split())
st.caption(f"Jumlah kata: {word_count}")

# Model ID
model_id = st.text_input("🧠 Model ID:", "eleven_multilingual_v2")

# Generate Suara
if st.button("🔊 Generate & Preview"):
    if not text:
        st.error("Teks tidak boleh kosong.")
    else:
        with st.spinner("Menghubungi ElevenLabs..."):
            headers = {
                "xi-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }

            url = f"{API_URL}/text-to-speech/{voice_id}/stream"
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                audio = r.content
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(audio)
                    audio_path = f.name

                # Audio Player
                st.audio(audio_path, format="audio/mp3")

                # Download Link
                b64 = base64.b64encode(audio).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">💾 Download MP3</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error(f"Gagal: {r.status_code} - {r.text}")

# Footer
st.markdown("---")
st.markdown(
    '<center><small>Build with ❤️ using ElevenLabs API • by TodTeam 2025</small></center>',
    unsafe_allow_html=True
)
