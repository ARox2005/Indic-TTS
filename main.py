from fastapi import FastAPI, File, Query
from fastapi.responses import StreamingResponse
from sarvamai import SarvamAI
import numpy as np
import librosa
import soundfile as sf
import io
import base64

app = FastAPI()
SARVAM_API_KEY = "<API-KEY-HERE>"

MALE_VOICE_ID = "hitesh"
FEMALE_VOICE_ID = "anushka"

LANG_MAP = {
    "english": "en-IN",
    "gujarati": "gu-IN",
    "hindi": "hi-IN",
    "bengali": "bn-IN",
}

def normalize_lang(lang):
    lang = lang.strip().lower()
    if lang in LANG_MAP:
        return LANG_MAP[lang]
    raise ValueError("Unsupported language")

def extract_pitch(file_bytes):
    wav, sr = sf.read(io.BytesIO(file_bytes))
    if len(wav.shape) > 1:
        wav = librosa.to_mono(wav.T)

    pitches, mags = librosa.piptrack(y=wav, sr=sr)
    mags_thresh = np.median(mags)
    pitch_vals = pitches[mags > mags_thresh]

    if len(pitch_vals) == 0:
        return 140.0

    return float(np.mean(pitch_vals))

def convert_f0_to_sarvam_pitch(f0):
    mean = 190.0
    spread = 110.0
    norm = (f0 - mean) / spread
    return max(-1.0, min(1.0, float(norm)))

def choose_voice(f0):
    if f0 > 170:
        return FEMALE_VOICE_ID, "female"
    return MALE_VOICE_ID, "male"

def reconstruct_wav_from_chunks(audio):
    chunks = audio.audios
    combined = b""

    for i, chunk in enumerate(chunks):
        raw = base64.b64decode(chunk)
        if i == 0:
            combined = raw
        else:
            pos = raw.find(b"data")
            if pos != -1:
                combined += raw[pos+8:]

    if len(chunks) > 1:
        total = len(combined) - 8
        combined = combined[:4] + total.to_bytes(4,"little") + combined[8:]

        pos = combined.find(b"data")
        if pos != -1:
            size = len(combined) - pos - 8
            combined = (combined[:pos+4] +
                        size.to_bytes(4,"little") +
                        combined[pos+8:])
    return combined


@app.post("/Get_Inference")
async def get_inference(
    text: str = Query(...),
    lang: str = Query(...),
    speaker_wav: bytes = File(...)
):
    try:
        lang_code = normalize_lang(lang)

        # 1. Extract pitch
        f0 = extract_pitch(speaker_wav)
        pitch_norm = convert_f0_to_sarvam_pitch(f0)

        # 2. Choose speaker based on pitch
        voice_id, gender = choose_voice(f0)

        client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

        # 3. Call Sarvam TTS WITH pitch
        result = client.text_to_speech.convert(
            text=text,
            target_language_code=lang_code,
            speaker=voice_id,
            pitch=pitch_norm,
            enable_preprocessing=True,
        )

        # 4. Reconstruct WAV back from chunked base64
        wav_bytes = reconstruct_wav_from_chunks(result)

        return StreamingResponse(
            io.BytesIO(wav_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=output.wav"}
        )

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}
