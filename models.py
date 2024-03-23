from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from typing import List

class FileAndList(BaseModel):
    textfile64: str
    imagefile64: str
    stopwords: str
