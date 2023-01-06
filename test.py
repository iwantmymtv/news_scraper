from googletrans import Translator
translator = Translator()

def translate_to_english(sentence:str) -> str:
    translated = translator.translate(sentence, dest="en")
    print(translated.text)
    print(sentence)
    return 

translate_to_english("Villámgyorsan tölthető, és a kormány eltűnik a műszerfalban a Peugeot 680 lóerős jövőautójában")