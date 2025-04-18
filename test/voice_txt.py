import whisper
import openai
from fastapi import FastAPI, UploadFile, Form
from googletrans import Translator
import pyttsx3

openai.api_key = "your-openai-api-key"

app = FastAPI()
model = whisper.load_model("base")
translator = Translator()
engine = pyttsx3.init()

@app.post("/ask")
async def ask(file: UploadFile = None, text: str = Form(None)):
    if file:
        audio = await file.read()
        with open("audio.wav", "wb") as f:
            f.write(audio)
        result = model.transcribe("audio.wav")
        text_input = result["text"]
    else:
        text_input = text

    detected_lang = translator.detect(text_input).lang
    if detected_lang != "en":
        text_input = translator.translate(text_input, dest="en").text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text_input}]
    )
    reply = response["choices"][0]["message"]["content"]

    if detected_lang != "en":
        reply = translator.translate(reply, dest=detected_lang).text

    engine.say(reply)
    engine.runAndWait()

    return {"response": reply}
