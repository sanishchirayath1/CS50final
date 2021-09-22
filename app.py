from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re

# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints

# primary route


@app.route('/<string:url>')
def index(url):
    # url = request.form.get("url")
    # checks for valid url
    video_id = url
    # try:
    #     video_id = url.split("=")[1]
    # except:
    #     message = "Not a valid youTube url"
    #     return message

    #checks whether subtitiles are enabled for the video
    try:
        transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        message = "Subtitles are disabled for this video"
        return message

    # coverts transcript_dict into a string
    transcript = ""
    for dialogs in transcript_dict:
        transcript += " " + dialogs['text']
    message = "Summary: " + summarize(transcript)

    # To replace wierd symbols got generated
    message = re.sub(r"<pad>|</s>", "", message)

    return summarize(message)

# function returns summary for text given


def summarize(transcript):
    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")

    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize: " + transcript,
                              return_tensors="pt", max_length=512, truncation=True)

    # generate the summarization output
    outputs = model.generate(
        inputs,
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True)
    # just for debugging
    #  return outputs
    return tokenizer.decode(outputs[0])


# # server the app when this file is run
# if __name__ == '__main__':
#     app.run()