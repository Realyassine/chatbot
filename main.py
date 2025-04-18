import requests
import pygame
from gtts import gTTS
import os
from requests.exceptions import RequestException

h
def get_gemini_response(question):
    url = f"https://jsonplaceholder.typicode.com/posts/1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("title", "No title found.")
    except RequestException as e:
        return f"Error: Unable to connect to the API. Details: {e}"

def speak(text):
    tts = gTTS(text=text, lang='en')  
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("output.mp3")

def main():
    while True:
        try:
            question = input("Ask Something: ")
            if question.lower() == 'exit':
                break
            response_text = get_gemini_response(question)
            print("Answer (text):", response_text)
            speak(response_text)
        except KeyboardInterrupt:
            print("\nCanceled.")
            break
        except Exception as e:
            print("There is an error:", e)
            print("Sorry, an error occurred. Please try again.")

if __name__ == "__main__":
    main()