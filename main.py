import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit as kit
import requests
import musicLibrary

r = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

newsapi = ""

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]
            if song in musicLibrary.music:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.music[song])
            else:
                speak(f"Playing {song} on YouTube")
                kit.playonyt(song)
        except IndexError:
            speak("Please say the song name after play")
    elif "play news" in c:
        speak("Playing latest news on YouTube")
        kit.playonyt("latest news India")
    elif "tell me news" in c:
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                if articles:
                    speak("Here are the top 3 headlines:")
                    for i, article in enumerate(articles[:3], 1):
                        headline = article['title'].split(" - ")[0]
                        speak(f"News {i}: {headline}")
                     
                else:
                    speak("No news found right now.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak("Error fetching news.")
            print("News Error:", e)
    else :
        pass


# Main loop
speak("Initializing Jarvis ...")
while True:
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening for wake word...")
            audio = r.listen(source, timeout=6, phrase_time_limit=5)
            word = r.recognize_google(audio).lower()
            print("You said:", word)

            if "jarvis" in word:
                speak("Yes, I am listening.")
                print("🎤 Jarvis Active ... say your command")
                audio = r.listen(source, timeout=6, phrase_time_limit=10)
                try:
                    command = r.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I did not understand that.")
                except sr.RequestError:
                    speak("Could not request results from Google.")

    except sr.WaitTimeoutError:
        print("⌛ Listening timed out, retrying...")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye!")
        break
    except Exception as e:
        print("⚠️ Error:", e)
