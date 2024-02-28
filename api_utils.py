import os
from dotenv import load_dotenv

load_dotenv()

DG_API_KEY = os.getenv("DG_API_KEY")

url = 'https://api.deepgram.com/v1/listen?diarize=true&punctuate=true&utterances=true'

headers = {
    'Authorization': f'Token {DG_API_KEY}',
    'Content-Type': 'audio/mp3',
}