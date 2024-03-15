from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from typing import List

class FileAndList(BaseModel):
    file: UploadFile
    stopwords: List[str]
