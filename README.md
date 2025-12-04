# ⭐ Syspin TTS – Voice-Adapted Indic Text-to-Speech API

A FastAPI-based Text-to-Speech service powered by **SarvamAI's TTS API**, enriched with:
- Reference speech **pitch extraction**
- Automatic **male/female voice selection**
- Normalized **pitch shaping**
- **Gujarati / English / Hindi / Bengali** language support
- Returns **output.wav** directly  
- Compatible with an **unchangeable external client script**

This project turns raw text + reference audio into natural TTS output.

---

## 🚀 Features

- **Upload reference WAV**
- **Extract speaker pitch (F0)**
- **Normalize pitch → [-1,1]**
- **Auto-select speaker based on pitch**
- Synthesizes speech via **Sarvam TTS API**
- Reconstructs **WAV chunks** from Sarvam’s chunked response
- Returns a **downloadable WAV file**
- Works with unmodifiable client scripts (POST + query + raw bytes)

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Environment Setup
Add your Sarvam API key inside main.py:
```python
SARVAM_API_KEY = "your_sarvam_api_key_here"
```
## ▶️ Running the Server
Start the FastAPI server:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
You should see:
```bash
Running on http://127.0.0.1:8000
```

## 🧪 Using /Get_Inference
### Endpoint
```nginx
POST /Get_Inference
```
### Query Params
|Name|Type	| Required|	Description                                          |
|----|------|---------|------------------------------------------------------|
|text|string|	YES	    |Text to convert to speech                             |
|lang|string|	YES	    |Full language name (english, gujarati, hindi, bengali)|

### File Upload
|Name       |Type|Required|Description                                |
|-----------|----|--------|-------------------------------------------|
|speaker_wav|file|YES     |Reference WAV file used for pitch detection|

## 🌍 Language Support
|Input Language|Sarvam Code|
|--------------|-----------|
|english       |	en-IN    | 
|gujarati      |	gu-IN    |
|hindi         |	hi-IN    |
|bengali       |	bn-IN    |

Extendable via ```LANG_MAP```.
