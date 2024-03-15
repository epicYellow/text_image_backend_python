import re
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tempfile
import base64

def parse_messages(decoded_string):
    dates = []
    times = []
    names = []
    messages = []

    pattern = r'\[(\d{4}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.+?): (.*)'

    lines = decoded_string.strip().split('\n')

    for line in lines:
        match = re.match(pattern, line)
        # print(match, line)
        if match:
            date, time, name, message = match.groups()
            dates.append(date)
            times.append(time)
            names.append(name)
            messages.append(message)

    data = {'Date': dates, 'Time': times, 'Name': names, 'Message': messages}

    return data

def get_words_from_messages(flat_list):
    message_words = []
    for word in flat_list:
        countWords = len(word.split())
        if countWords != 1:
            indwords = word.split()
            for indword in indwords:
                message_words.append(indword.lower())
        else:
            message_words.append(word.lower())
    return message_words

def create_plot_image(string, mask, size, max_words, colors):
    word_cloud = WordCloud(background_color='white', max_words=max_words, colormap=colors)
    word_cloud.generate(string)

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        plt.figure(figsize=size)
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(tmp_file.name, format='png')

    return encode_image_to_base64(tmp_file.name)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # Read the image file as binary data
        binary_data = img_file.read()

        # Encode the binary data as base64
        base64_encoded = base64.b64encode(binary_data)

        # Convert bytes to a string
        base64_string = base64_encoded.decode('utf-8')

        return base64_string