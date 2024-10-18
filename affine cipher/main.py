english_dictionary = {"the", "of", "and", "to", "in", "it", "is", "was", "for", "on", "that", "by", "this", "with", "you", "not", "or", "be", "are", "from"}

def is_sentence_valid(decrypted_message):
    for word in english_dictionary:
        if word in decrypted_message:
            return True
    return False

def nwd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a):
    # Zwraca modularną odwrotność liczby a względem m, jeśli istnieje
    for x in range(1, 26):
        if (a * x) % 26 == 1:
            return x
    return None

def decrypt_affine_cipher(encrypted_text, a, b):
    decrypted_text = ""
    
    # Znajdź modularną odwrotność a
    a_inv = mod_inverse(a)
    
    if a_inv is None:
        return None

    # Dla każdej litery w zaszyfrowanym tekście
    for letter in encrypted_text:
        if letter.isalpha():  # ignorujemy inne znaki niż litery
            y = ord(letter) - ord('a')

            # Odszyfruj: x = a_inv * (y - b) % 26
            x = (a_inv * (y - b)) % 26

            decrypted_letter = chr(x + ord('a'))
            decrypted_text += decrypted_letter
        else:
            # W przypadku znaków nie będących literami, po prostu je dodajemy
            decrypted_text += letter
    
    return decrypted_text

def determiningAandB(dictionary, letters, encrypted):
    encrypted_letters = list(dictionary.keys())

    for i in range(len(encrypted_letters)):
        for j in range(i + 1, len(encrypted_letters)):
            for k in range(len(letters) - 1):
                for l in range(k + 1, len(letters)):
                    y1 = encrypted_letters[i]
                    y2 = encrypted_letters[j]

                    x1 = letters[k]
                    x2 = letters[l]

                    y1_index = ord(y1) - ord('a')
                    y2_index = ord(y2) - ord('a')
                    x1_index = ord(x1) - ord('a')
                    x2_index = ord(x2) - ord('a')

                    # Równanie dla a:
                    delta_y = (y1_index - y2_index) % 26
                    delta_x = (x1_index - x2_index) % 26

                    # Znajdź modularną odwrotność delta_x mod 26
                    inv_delta_x = mod_inverse(delta_x)

                    if inv_delta_x is not None:
                        # a = (delta_y * inv_delta_x) % 26
                        a = (delta_y * inv_delta_x) % 26

                        # Sprawdzenie, czy a jest względnie pierwsze z 26 (czyli NWD(a, 26) == 1)
                        if nwd(a, 26) != 1:
                            continue
                        
                        # Równanie dla b:
                        # y1 = (a * x1 + b) % 26
                        # b = (y1 - a * x1) % 26
                        b = (y1_index - a * x1_index) % 26

                        decrypted_message = decrypt_affine_cipher(encrypted, a, b)

                        if is_sentence_valid(decrypted_message):
                            print(f"Found values a: {a}, b: {b}, \nDecrypted sentence: {decrypted_message}")
                            return a, b

    return None, None
    
if __name__ == "__main__":
    encrypted_message = "hzkedhktteukdhpibsmeaotgjmynkfirkxhzktqlgvxiwdfiuhweak"
    letters = ['e','t','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
    dictionary_letters = {}
    for letter in encrypted_message:
        if letter in dictionary_letters:
            dictionary_letters[letter] += 1
        else:
            dictionary_letters[letter] = 1
    sorted_dictionary = dict(sorted(dictionary_letters.items(), key=lambda item: item[1], reverse=True))
    determiningAandB(sorted_dictionary, letters, encrypted_message)
