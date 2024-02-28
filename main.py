from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DG_API_KEY = os.getenv("DG_API_KEY")
url = 'https://api.deepgram.com/v1/listen?diarize=true&punctuate=true&utterances=true'

headers = {
    'Authorization': f'Token {DG_API_KEY}',
    'Content-Type': 'audio/mp3',
}

def convert_transcripts_to_json_objects(utterances):
    json_objects = []
    for utterance in utterances:
        role = 'assistant' if utterance['speaker'] == 0 else 'user'
        json_obj = {'role': role, 'content': utterance['transcript']}
        json_objects.append(json_obj)
    return json_objects

def json_to_jsonl_converter(json_data, output_path='output.jsonl'):
    with open(output_path, 'w') as jsonl_file:
        for item in json_data:
            jsonl_file.write(json.dumps(item) + '\n')
    return output_path

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith('.mp3'):
        return {"error": "Please upload an MP3 file."}

    audio_data = await file.read()
    response = requests.post(url, headers=headers, data=audio_data)

    if response.status_code == 200:
        utterances = response.json().get('results', {}).get('utterances', [])
        # we can combine both functions into one, but maybe we will use the normal json for something else
        transcript_json = convert_transcripts_to_json_objects(utterances)
        output_file_path = json_to_jsonl_converter(transcript_json)
        return FileResponse(path=output_file_path, filename="transcription.jsonl")
    else:
        return {"error": f"Failed to transcribe audio. Status code: {response.status_code}", "details": response.text}
