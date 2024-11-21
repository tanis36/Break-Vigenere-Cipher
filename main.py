import numpy as np
import string

# Global Variables

# Frequency of letters in alphabet
F = [.082, .015, .028, .043, .127, .022, .020, .061, .070, .002, .008, .040, .024, 
        .067, .075, .019, .001, .060, .063, .091, .028, .010, .023, .001, .020, .001]

# Maximum key length
L = 6

# Function to decrypt the vigenere cipher
def decrypt_vigenere(ciphertext, max_key_length):

    # Define the shift
    shift = 1

    # Define a variable for max coincidences
    max_coincidences = 0

    # Define a variable for possible key_length
    key_length = 0

    # While loop to find coincidences
    while (shift <= max_key_length):
        
        # Define a variable that represents the shifted ciphertext
        shifted_ciphertext = ciphertext[shift:]

        # Define the number of coincidences
        coincidences = 0

        # Find the coincidences
        for i in range(len(shifted_ciphertext)):
            if shifted_ciphertext[i] == ciphertext[i]:
                coincidences += 1

        # Update max_coincidences and possible key length if needed
        if (coincidences > max_coincidences):
            max_coincidences = coincidences
            key_length = shift

        # Increase the shift
        shift += 1
    
    # Initialize a list of shifts
    shifts = []

    # Find occurrences in each position separated by the key length, shifting each time
    for i in range(key_length):

        # Initialize a list of dot products
        dot_products = []

        # Initialize the list of occurrences
        v = [0] * 26

        # Find the letters in the desired positions
        letters = ciphertext[i::key_length]

        # For each letter, update the occurrence count for that letter in v
        for letter in letters:
            position = string.ascii_lowercase.find(letter)
            v[position] += 1

        # Find the normalized list
        w = [x / sum(v) for x in v]

        # Initialize a shift variable
        s = 0

        # Loop to find dot products
        while (s <= len(F)):
            shifted_F = F[-s:] + F[:-s]
            dot_product = np.dot(w, shifted_F)
            dot_products.append(dot_product)
            s += 1

        # Find the position of the max dot product, representing the shift
        pos_of_max_dot_product = dot_products.index(max(dot_products))

        # Append the shift to the shifts list
        shifts.append(pos_of_max_dot_product)

    # Extend the shifts list, which is the key, to be the length of the ciphertext
    key_extended = (shifts * ((len(ciphertext) // len(shifts)) + 1))[:len(ciphertext)]

    # Initialize a variable to reconstruct the plaintext
    plaintext = ""

    # Loop to decrypt the ciphertext
    for i in range(len(key_extended)):
        pos = string.ascii_lowercase.find(ciphertext[i])
        decrypted_pos = (pos - key_extended[i]) % 26
        original_letter = string.ascii_lowercase[decrypted_pos]
        plaintext += original_letter
    
    return key_length, shifts, plaintext

# Main function
def main():

    # Ask which file to open
    input_file = input("Enter the file containing the ciphertext: ")

    # Get the ciphertext
    with open(input_file, 'r') as f:
        ciphertext = f.read()
        key_length, shifts, plaintext = decrypt_vigenere(ciphertext, L)
        print(f'Key length: {key_length}')
        print(f'Shifts: {shifts}')
        print(f'Plaintext: {plaintext}')

# Run main
if __name__ == "__main__":
    main()