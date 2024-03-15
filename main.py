from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from functions import create_plot_image, get_words_from_messages, parse_messages
import models
import base64

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/createImage")
async def create_image(payload: models.FileAndList):
    file = base64.b64decode(payload.file)

    decoded_string = file.decode("utf-8")
    stopwords = payload.stopwords

    df = pd.DataFrame(parse_messages(decoded_string))

    flat_list = df['Message']
    word_list = stopwords.split(', ')
    lowercase_stopwords = [word.lower() for word in word_list]
    print(lowercase_stopwords[:100])
    filtered_words = [word.lower() for word in get_words_from_messages(flat_list) if word not in lowercase_stopwords]
    print(filtered_words[:100])

    str_ = ' '.join(filtered_words)

    return Response(content=create_plot_image(str_.capitalize(), None, size=[32,16], max_words=1000, colors='autumn'), media_type="application/json")