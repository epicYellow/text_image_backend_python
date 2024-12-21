from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from functions import create_plot_image, get_words_from_messages, parse_messages
from PIL import Image
import models
import io, base64
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
    textfile_64 = base64.b64decode(payload.textfile64)
    decoded_textfile = textfile_64.decode("utf-8")

    fontfile_64 = payload.fontfile64
    print('received font 64 string: ', fontfile_64)
    decoded_fontfile = base64.b64decode(fontfile_64)

    print("line 42: ", decoded_fontfile)

    stopwords = payload.stopwords
    gradient = payload.gradient

    df = pd.DataFrame(parse_messages(decoded_textfile))

    flat_list = df['Message']
    word_list = stopwords.split(', ')

    lowercase_stopwords = [word.lower() for word in word_list]

    filtered_words = [word.lower() for word in get_words_from_messages(flat_list) if word not in lowercase_stopwords]

    str_ = ' '.join(filtered_words)

    return Response(content=create_plot_image(str_.capitalize(), payload.imagefile64, size=[32,32], max_words=300, colors=gradient, font=decoded_fontfile), media_type="application/json")