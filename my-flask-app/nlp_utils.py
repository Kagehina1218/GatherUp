import speech_recognition as sp
import time

def nlp():
    rec = sp.Recognizer()

    with sp.Microphone() as source:
        
        rec.adjust_for_ambient_noise(source, duration=0.5)
        time.sleep(1)
        print("Speaking Now")
        rec.pause_threshold = 2.0
        audio = rec.listen(source, timeout = 10, phrase_time_limit = 25)

    print("moving to converting")

    try:
        audioInput = rec.recognize_google(audio)
        print ("you said: ", audioInput)
        return audioInput
    except sp.UnknownValueError:
        print("Could not understand audio")
    except sp.RequestError as e:
        print("Could not request results", e)