from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import requests

from utils import convert_transcripts_to_json_objects, convert_json_to_jsonl
from api_utils import url, headers

app = FastAPI()


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith('.mp3'):
        return {"error": "Please upload an MP3 file."}

    audio_data = await file.read()
    response = requests.post(url, headers=headers, data=audio_data)

    if response.status_code == 200:
        utterances = response.json().get('results', {}).get('utterances', [])
        # we can combine both functions into one
        # but we might use json for something else and it is easier to test and maintain
        transcript_json = convert_transcripts_to_json_objects(utterances)
        jsonl_output_file_path = convert_json_to_jsonl(transcript_json)
        return FileResponse(path=jsonl_output_file_path, filename="transcription.jsonl")
    else:
        return {"error": f"Failed to transcribe audio. Status code: {response.status_code}", "details": response.text}
    

