# from epitran import Epitran
from subprocess import check_output, CalledProcessError
import time
# Initialize Epitran for Hindi Devanagari once
# hindi_epi = Epitran('hin-Deva')

def english_to_ipa(text):
    """Converts English text to IPA using espeak-ng."""
    try:
        ipa = check_output(['espeak-ng', '-q', '--ipa', text], universal_newlines=True).strip()
        return ipa
    except CalledProcessError as e:
        return f"Error: {e}"

# def hindi_to_ipa(text):
#     """Converts Hindi text to IPA using epitran."""
#     try:
#         return hindi_epi.transliterate(text)
#     except Exception as e:
#         return f"Error: {e}"

# Example Usage
# names_to_test = [
#     ('noel', 'नोएल'),
#     ('Krishna', 'कृष्ण'),
#     ('Aarav', 'आरव'),
#     ('Venkatesh', 'वेंकटेश'),
#     ('Ankit', 'अंकित'),
#     ('Rahul', 'राहुल'),
#     ('alia', 'आलिया'),
#     ('srimoney', 'श्रीमनी'),
# ]

# # Process and print results
# a = time.time()

# for eng, hindi in names_to_test:

#     print(f"English IPA for '{eng}': {english_to_ipa(eng)}")
#     # print(f"Hindi IPA for '{hindi}': {hindi_to_ipa(hindi)}")
# print(time.time() - a)