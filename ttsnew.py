import streamlit as st
import requests
import tempfile
import base64

# ====== Konfigurasi Streamlit ======
st.set_page_config(
    page_title="ElevenLabs TTS Web",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 13px;
        color: gray;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ====== Sidebar (Mode Gelap / Terang) ======
theme_mode = st.sidebar.radio("🌓 Theme", ["Light", "Dark"])
if theme_mode == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )

# ====== Judul ======
st.title("🎙️ ElevenLabs TTS Generator")

# ====== Form Input ======
with st.form("tts_form"):
    api_key = st.text_input("🔑 ElevenLabs API Key", type="password")
    text = st.text_area("📄 Text to Convert", height=150)
    model_id = st.text_input("🧠 Model ID", value="eleven_multilingual_v2")
    voice_id = st.text_input("🗣️ Voice ID", value="EXAVITQu4vr4xnSDxMaL")

    word_count = len(text.split())
    st.caption(f"📝 Word Count: {word_count}")

    submitted = st.form_submit_button("🔊 Preview Audio")

# ====== Fungsi Kirim Request ======
def generate_tts(api_key, text, model_id, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {
        "xi-api-key": api_key,
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

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.content

# ====== Preview Audio ======
if submitted:
    if not api_key or not text or not model_id or not voice_id:
        st.error("❌ Semua input wajib diisi.")
    else:
        try:
            audio_data = generate_tts(api_key, text, model_id, voice_id)
            st.success("✅ Audio berhasil dibuat!")

            # Preview audio
            st.audio(audio_data, format="audio/mp3")

            # Simpan sementara buat tombol download
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name

            # Convert to base64 for download button
            with open(tmp_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Download MP3</a>'
                st.markdown(href, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error: {e}")

# ====== Footer ======
st.markdown('<div class="footer">© 2025 TTS by pipuplan — Powered by ElevenLabs API</div>', unsafe_allow_html=True)
