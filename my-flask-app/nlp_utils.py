import speech_recognition as sp

def nlp():
    rec = sp.Recognizer()

    with sp.Microphone() as source:
        print("Speaking Now")
        rec.adjust_for_ambient_noise(source)
        rec.pause_threshold = 1.5

        audio = rec.listen(source, timeout = 10, phrase_time_limit = 20)

    print("moving to converting")

    try:
        audioInput = rec.recognize_google(audio)
        print ("you said: ", audioInput)
        return audioInput
    except sp.UnknownValueError:
        print("Could not understand audio")
    except sp.RequestError as e:
        print("Could not request results", e)