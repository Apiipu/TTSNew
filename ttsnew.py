import streamlit as st
import requests
import tempfile
import time

# Fungsi kirim request ke ElevenLabs
def send_request(api_key, text, model, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "xi-model-id": model
    }
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.content

# ============================
# ============ UI ============
# ============================

# Dark mode toggle (simulasi: theme switcher manual)
st.set_page_config(page_title="ElevenLabs TTS Web", layout="centered")

mode = st.sidebar.selectbox("🌗 Mode Tampilan", ["Light", "Dark"])
if mode == "Dark":
    st.markdown(
        """
        <style>
        body { background-color: #1e1e1e; color: #f1f1f1; }
        .stTextInput, .stTextArea, .stButton { background-color: #333; color: white; }
        </style>
        """, unsafe_allow_html=True
    )

st.title("🎙️ ElevenLabs TTS Web")

# Input API
api_key = st.text_input("API Key", type="password")
text = st.text_area("📝 Masukkan Teks untuk Dibacakan", height=150)
model_id = st.text_input("Model ID", value="eleven_multilingual_v2")
voice_id = st.text_input("Voice ID", value="EXAVITQu4vr4xnSDxMaL")

# Hitung kata
word_count = len(text.strip().split())
st.caption(f"🔤 Jumlah kata: {word_count} kata")

# Tombol preview
if st.button("🎧 Preview"):
    if not all([api_key, text, model_id, voice_id]):
        st.error("Harap lengkapi semua input.")
    else:
        try:
            with st.spinner("🔄 Menghasilkan audio..."):
                audio_data = send_request(api_key, text, model_id, voice_id)
                temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_data)
                time.sleep(1)
            st.success("✅ Audio siap diputar")
            st.audio(temp_audio_path, format="audio/mp3")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# Tombol download
if st.button("💾 Simpan sebagai MP3"):
    if not all([api_key, text, model_id, voice_id]):
        st.error("Harap lengkapi semua input.")
    else:
        try:
            with st.spinner("🔄 Menghasilkan file..."):
                audio_data = send_request(api_key, text, model_id, voice_id)
            st.download_button(
                label="⬇️ Klik untuk Unduh MP3",
                data=audio_data,
                file_name="tts_output.mp3",
                mime="audio/mpeg"
            )
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

# ============================
# ========== FOOTER ==========
# ============================

st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 13px; color: gray;'>
    Dibuat oleh <b>[Pipuplan]</b> · Powered by <a href="https://www.elevenlabs.io/" target="_blank">ElevenLabs API</a><br>
    Streamlit WebApp TTS – v1.0 · 2025
</div>
""", unsafe_allow_html=True)
