# app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
import matplotlib.pyplot as plt

st.title("Word to Image Generator")
# Step 1: Read URL query parameters
query_params = st.query_params
word_from_url = query_params.get('word', [''])[0]  # Default to empty string if not provided

# Step 2: Show text input with pre-filled value from URL (if available)
word = st.text_input("Enter a word:", value=word_from_url)

# Step 3: If the user enters a word or comes via URL
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_and_save_primes(start, end, filename="prime_numbers.txt"):
    prime_list = [num for num in range(start, end + 1) if is_prime(num)]
    
    with open(filename, "w") as file:
        for prime in prime_list:
            file.write(f"{prime}\n")
    
    # print(f"{len(prime_list)} prime numbers saved to '{filename}'.")

    # Create sublists using 1-based indexing
    odd_placed_primes = [prime_list[i] for i in range(len(prime_list)) if (i + 1) % 2 == 1]
    even_placed_primes = [prime_list[i] for i in range(len(prime_list)) if (i + 1) % 2 == 0]
    fifth_placed_primes = [prime_list[i] for i in range(len(prime_list)) if (i + 1) % 5 == 0]

    return prime_list, odd_placed_primes, even_placed_primes, fifth_placed_primes

# Example usage
primes, odd_placed, even_placed, fifth_placed = get_and_save_primes(5, 255)

# Create 5x6 array filled with zeros initially
matrix_with_values = np.zeros((5, 6), dtype=int)

# List all positions excluding corners
positions = [(i, j) for i in range(5) for j in range(6)
             if not ((i == 0 and j == 0) or  # Top-left
                     (i == 0 and j == 5) or  # Top-right
                     (i == 4 and j == 0) or  # Bottom-left
                     (i == 4 and j == 5))]   # Bottom-right

# Fill the remaining 26 positions with values 1 to 26
for val, (i, j) in enumerate(positions, start=1):
    matrix_with_values[i, j] = val

# Function to convert a letter to its alphabetical order (A=1, B=2, ..., Z=26)
def letter_to_number(letter):
    return ord(letter.lower()) - ord('a') + 1

# # Take input word from the user
# word = input("Enter a word: ")

# List of unique letters in the order they first appear, converted to numbers
unique_letters = []
for letter in word:
    # Check if the letter is not already in the unique_letters list (case-insensitive)
    if letter.lower() not in [l.lower() for l in unique_letters]:
        unique_letters.append(letter)

# Convert the unique letters to their alphabetical order numbers
unique_letters = [letter_to_number(letter) for letter in unique_letters]

# List of sequence of letters, converted to numbers
sequence_of_letters = [letter_to_number(letter) for letter in word]

# List of frequencies of each letter (in terms of alphabetical order)
letter_frequencies = [sequence_of_letters.count(letter_to_number(letter)) for letter in word]

# Sample matrix X with sequence values
X = matrix_with_values.copy()
# U and E lists
U = unique_letters  # Values that give indices for P
E = even_placed  # Final values to place in X

# Create a copy of X to hold results
resultR = X.copy()

# Iterate over X and apply logic
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        if X[i, j] != 0:
            seq_index = X[i, j]
            if seq_index > len(U):
                resultR[i, j] = 255
            else:
                index_for_E = U[seq_index-1]                    
                if index_for_E <= len(E):
                    resultR[i, j] = E[index_for_E-1]
                    
# Sample matrix X with sequence values
X = matrix_with_values.copy()
# S and O lists
S = sequence_of_letters  # Values that give indices for P
O = odd_placed  # Final values to place in X

# Create a copy of X to hold results
resultG = X.copy()

# Iterate over X and apply logic
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        if X[i, j] != 0:
            seq_index = X[i, j]
            if seq_index > len(S):
                resultG[i, j] = 255
            else:
                index_for_O = S[seq_index-1]                    
                if index_for_O <= len(O):
                    resultG[i, j] = O[index_for_O-1]
                    
# Sample matrix X with sequence values
X = matrix_with_values.copy()
# F and A lists
F = letter_frequencies  # Values that give indices for P
A = primes  # Final values to place in X

# Create a copy of X to hold results
resultB = X.copy()

# Iterate over X and apply logic
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        if X[i, j] != 0:
            seq_index = X[i, j]
            if seq_index > len(F):
                resultB[i, j] = 255
            else:
                index_for_A = F[seq_index-1]                    
                if index_for_A <= len(A):
                    resultB[i, j] = A[index_for_A-1]
                    
# Stack them to form an RGB image
rgb_image = np.stack((resultR, resultG, resultB), axis=-1)
img = Image.fromarray(rgb_image)
# Show the image
img.save("output.png")
st.image("output.png", caption=f"Generated Image for '{word}'")

