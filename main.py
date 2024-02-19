import math

from fastapi import FastAPI, Response, status
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from fastapi.middleware.cors import CORSMiddleware
from exceptions import EnglishCaptionsAreNotAvailable

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/captions/{video_id}")
async def get_caption(video_id: str, response: Response):
    try:
        transcript = get_transcript(video_id)
        captions = []
        for index, caption in enumerate(transcript):
            end = caption['start'] + caption['duration']
            next_caption_index = None if len(transcript) - 1 == index else index + 1
            captions.append(
                {
                    "index": index,
                    "next_caption_index": next_caption_index,
                    "text": caption['text'],
                    "start": round_half_up(caption['start'] * 10) * 100,
                    "end": round_half_up(end * 10) * 100
                })

        return {"transcript": captions, "duration": captions[-1]['end']}
    except TranscriptsDisabled:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"message": TranscriptsDisabled.CAUSE_MESSAGE}


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier


def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    for transcript in transcript_list:
        language_code = transcript.language_code
        if language_code == 'en' or language_code.startswith('en-'):
            return transcript.fetch()
    raise EnglishCaptionsAreNotAvailable.EnglishCaptionsAreNotAvailable()
