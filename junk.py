import os, sys, binascii
from PIL import Image

def bit_string_to_8bits(bit_string):
    preceding_zeroes = '0' * (8 - len(bit_string))
    full_string = preceding_zeroes + bit_string
    return full_string

def string_to_bin(string):
    binary_string = ''
    for letter in string:
        letter_as_int = ord(letter)
        letter_as_binary = format(letter_as_int, 'b')
        letter_as_binary = bit_string_to_8bits(letter_as_binary)
        binary_string += letter_as_binary
    return binary_string

def bin_to_string(binary):
    binary_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''
    for chunk in binary_chunks:
        ascii_value = int(chunk, 2)
        text += chr(ascii_value)
    return text

def extract_last_bit(byte):
    last_bit = list(format(byte, 'b'))
    print(last_bit)
    print(last_bit[0])
    print(last_bit[1])
    print(last_bit[2])
    print(last_bit[3])
    print(last_bit[4])
    print(last_bit[5])
    return last_bit[-1]


binary_string = string_to_bin("I want it HARD AND RAW!")
print(binary_string)
normal_string = bin_to_string(binary_string)
print(normal_string)
extract_last_bit(41)
