import math

from fastapi import FastAPI, Response, status
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from fastapi.middleware.cors import CORSMiddleware

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
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        captions = []
        for caption in transcript:
            end = caption['start'] + caption['duration']
            captions.append(
                {
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
