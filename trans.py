from googletrans import Translator

# Initialize the Translator
translator = Translator()

def trans_hindi_to_english(hindi_text):
    result = translator.translate(hindi_text, src='hi', dest='en')
    return result.text

def trans_english_to_hindi(english_text):
    result = translator.translate(english_text, src='en', dest='hi')
    return result.text
print(trans_english_to_hindi("noel"))