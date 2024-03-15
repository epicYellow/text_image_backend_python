import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import models
import re

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/createImage")
async def create_image(payload: models.FileAndList):
    print('lets go')
    file = payload.file
    stopwords = payload.stopwords
    
    lines = []

    dates = []
    times = []
    names = []
    messages = []

    pattern = r'[(\d{4}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})] (.+?): (.*)'

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only TXT files allowed")

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        match = re.match(pattern, line)
        if match:
            date, time, name, message = match.groups()
            dates.append(date)
            times.append(time)
            names.append(name)
            messages.append(message)
    
    data = {'Date': dates, 'Time': times, 'Name': names, 'Message': messages}
    df = pd.DataFrame(data)

    message_words = []
    flat_list = df['Message']

    for word in flat_list:
        countWords = len(word.split())
        if countWords != 1:
            indwords = word.split()
            for indword in indwords:
                if indword not in stopwords:
                    message_words.append(indword)
        else:
            if word not in stopwords:
                message_words.append(word)

    str_ = ''.join(message_words)

    word_cloud = WordCloud(background_color='white', max_words=500, colormap='winter')
    word_cloud.generate(str_)

    buffer = io.BytesIO()

    plt.figure(figsize=[16,8])
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buffer, format='png')

    buffer.seek(0)

    plt.close()

    return FileResponse(buffer, media_type='image/png')