import os
import pandas as pd
import re
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# === Load API key ===
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise ValueError("Missing ELEVENLABS_API_KEY in .env")

# === Initialize ElevenLabs client ===
client = ElevenLabs(api_key=api_key)

# === File paths ===
INPUT_CSV = r"C:\Users\Henri\Documents\GitHub\Saudi_Arabic_Flash_Cards\data\vocab.csv"
OUTPUT_DIR = r"C:\Users\Henri\Documents\GitHub\Saudi_Arabic_Flash_Cards\audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Voice config ===
VOICE_ID = "u0TsaWvt0v8migutHM3M"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"

# === Load vocab ===
df = pd.read_csv(INPUT_CSV)
print(f"df head looks like : {df.head()}")

if "audio_path" not in df.columns:
    df["audio_path"] = ""
else:
    df["audio_path"] = df["audio_path"].astype(str)

# === Sanitize for filenames ===
def sanitize_filename(text):
    return re.sub(r'[^\w\-_.]', '_', text)

# === Loop and generate audio ===
MAX_FILES = 20
count = 0

for index, row in df.iterrows():
    #if count >= MAX_FILES:
        #print(f"count >= MAX_FILES")
        #break

    arabic = row['arabic_word']
    print(f"arabic word : {arabic}")

    # Get audio_path as string and clean it
    audio_path = str(row.get("audio_path", "")).strip().lower()

    # Check whether to skip
    if pd.isnull(arabic) or audio_path not in ["", "nan", "none", "null"]:
        print(f"⏩ Skipping {arabic} (audio_path: '{audio_path}')")
        continue

    filename = sanitize_filename(arabic) + ".mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"🔊 Generating audio for: {arabic} → {filename}")

    try:
        audio_generator = client.text_to_speech.convert(
            text=arabic,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
        )
        
        audio = b"".join(audio_generator)

        with open(filepath, "wb") as f:
            f.write(audio)
        
        df.at[index, "audio_path"] = filepath
        print(f"✅ Saved: {filepath}")
        #count += 1

    except Exception as e:
        print(f"⚠️ Error generating audio for '{arabic}': {e}")
        df.at[index, "audio_path"] = ""

# === Save updated CSV ===
df.to_csv(INPUT_CSV, index=False)
print("✅ Audio generation complete. Updated vocab.csv with audio paths.")
