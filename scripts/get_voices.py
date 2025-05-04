# get_voices.py
from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

for voice in client.voices.get_all():
    print(f"{voice.name}: {voice.voice_id}")
