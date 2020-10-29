from api_methods.base_api import BaseAPI

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class MorseAPI:

    CHAR_TO_MORSE = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----."
    }

    MORSE_TO_CHAR = { v : k for k, v in CHAR_TO_MORSE.items() }

    MORSE_CHARS = [" ", "-", "."]

    def enc_dec_text(encode, text):
        
        # Encode/decode the text
        text = text.replace("%20", " ").upper()
        words = text.split(" ")
        converted = ""

        # If encoding the text, check to make sure the text does not consist of only Morse
        #   code characters
        if encode:
            if len([ char for char in text if char not in MorseAPI.MORSE_CHARS ]) == 0:
                return { "success": False, "error": "Cannot encode morse code" }, 400
            for word in words:
                for letter in word:
                    if letter in MorseAPI.CHAR_TO_MORSE:
                        converted += MorseAPI.CHAR_TO_MORSE[letter]
                    else:
                        converted += ""
                    converted += " "
                converted += " "
            return { "success": True, "value": converted.strip() }, 200
        
        # If the decoding the text, check to make sure all the text only consists 
        #   of Morse code character
        else:
            if len([ char for char in text if char not in MorseAPI.MORSE_CHARS ]) > 0:
                return { "success": False, "error": "Cannot decode regular text" }, 400
            for letter in words:
                if len(letter) == 0:
                    converted += " "
                elif letter in MorseAPI.MORSE_TO_CHAR:
                    converted += MorseAPI.MORSE_TO_CHAR[letter]
            return { "success": True, "value": converted.strip().lower() }, 200

    class Encode(BaseAPI):
        def get(self):
            parameters = super().get()
            text = parameters.get("text")

            # Check if the text exists
            if text:
                return MorseAPI.enc_dec_text(True, text)
            
            # The text does not exist
            return { "success": False, "error": "Cannot encode empty text" }, 400

        
    class Decode(BaseAPI):
        def get(self):
            parameters = super().get()
            text = parameters.get("text")

            # Check if the text exists
            if text:
                return MorseAPI.enc_dec_text(False, text)
            
            # The text does not exist
            return { "success": False, "error": "Cannot decode empty text" }, 400
