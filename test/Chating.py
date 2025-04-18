import speech_recognition as sr
import pyttsx3
import pyaudio
from datetime import datetime
import sys
import wikipediaapi
import webbrowser


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


wiki_wiki = wikipediaapi.Wikipedia(
    language='fr',
    user_agent='AlexaPythonApp/1.0 (contact: sfnkhaddi@gmail.com)'
)

def parler(texte):
    engine.say(texte)
    engine.runAndWait()

def ecouter():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Écoute...")
            parler("Je suis prête, que puis-je faire pour toi ?")
            audio = recognizer.listen(source)
            commande = recognizer.recognize_google(audio, language='fr-FR')  # Français
            commande = commande.lower()
            print("Tu as dit : " + commande)
            return commande
    except sr.UnknownValueError:
        parler("Je n'ai pas compris, pouvez-vous répéter ?")
        return ""
    except sr.RequestError as e:
        parler("Je ne peux pas accéder au service de reconnaissance vocale.")
        print("Erreur de reconnaissance vocale : ", e)
        return ""

def lancer_alexa():
    commande = ecouter()
    if 'heure' in commande:
        maintenant = datetime.now()
        heure = maintenant.strftime('%H:%M')
        parler("Il est actuellement " + heure)
    elif 'bonjour' in commande:
        parler("Bonjour à vous ! Comment puis-je vous aider ?")
    elif 'stoper la synthèse vocale' in commande:
        parler("La synthèse vocale est terminée.")
        sys.exit()  # Quitte le programme
    elif 'recherche sur wikipédia' in commande:
        parler("Que voulez-vous rechercher sur Wikipédia ?")
        recherche = ecouter()
        if recherche:
            page = wiki_wiki.page(recherche)
            if page.exists():
                parler(f"Voici ce que j'ai trouvé sur {recherche} : {page.summary[:500]}...")
            else:
                parler(f"Désolée, je n'ai rien trouvé sur {recherche}.")
    elif 'recherche sur google' in commande:
        parler("Que voulez-vous rechercher sur Google ?")
        recherche = ecouter()
        if recherche:
            url = f"https://www.google.com/search?q={recherche}"
            webbrowser.open(url)
            parler(f"Voici les résultats de la recherche pour {recherche} sur Google.")
    else:
        parler("Désolée, je n'ai pas encore appris cette commande.")

while True:
    lancer_alexa()