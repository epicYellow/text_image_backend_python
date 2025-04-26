from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from functions import create_plot_image, get_words_from_messages, parse_messages
from PIL import Image
import models
import io, base64
import base64
import re

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
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

@app.post("/api/newWordCloud")
async def get_word_cloud(text_file: UploadFile = File(...), image_file: UploadFile = File(...)):
    filenames = [text_file.filename, image_file.filename]
    print(f"Received file: {filenames}")
    return {"filenames": filenames}

@app.post("/api/getTopHundredWords")
async def get_top_hundred_words(text_file: UploadFile = File(...)):
    lines = []
    chatData= []

    pattern = r'\[(\d{4}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.+?): (.*)'

    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            match = re.match(pattern, line)
            if match and 'https' not in line and 'omitted' not in line and 'missed' not in line:
                date, time, name, message = match.groups()
                chatData.append({'date': date, 'name': name, 'message': message})


    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
