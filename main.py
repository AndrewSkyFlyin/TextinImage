import os, sys
from PIL import Image

#Converts a binary string into a normal text string.
def bin_to_string(binary):
    #Splits the binary into an array by chunks of 8 characters long.
    binary_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''
    for chunk in binary_chunks:
        #Converts each binary chunk into the ascii decimal value.
        ascii_value = int(chunk, 2)
        #Converts the ascii decimal value into its character representation.
        #The char is then appended to the text string variable.
        text += chr(ascii_value)
    return text

#Extracts the least significant bit value of the passed bit string.
def extract_last_bit(byte):
    #Convert the passed value into binary format.
    last_bit = list(format(byte, 'b'))
    #Return the last element of the last_bit array, which is the least significant bit.
    return last_bit[-1]

#Calculates the number of bits required to embed/extract message.
def num_bits_in_string(string):
    return len(string) * 8

#The main message extraction function.
def extract_Image(image_data, number_of_bits, index):
    bit_string = ''
    #cut_off is where tge message extraction will stop at.
    cut_off = index - number_of_bits
    while index >= cut_off:
        #Extract the least significant bit of each RGB value and append to bit_string
        red, green, blue = image_data[index]
        index -= 1
        bit_string += extract_last_bit(red)
        bit_string += extract_last_bit(green)
        bit_string += extract_last_bit(blue)
    return bit_string[:number_of_bits]

def extract_text_length(image_data):
    binary_length = extract_Image(image_data, binary_message_length, string_length_starting_pixel)
    length2 = int(binary_length, 2)
    return length2

binary_message_length = 32
image = Image.open('testImage.png')
image_data = list(image.getdata())
length, height = image.size
maxSize = (length * height) - 1
string_length_starting_pixel = maxSize
string_text_starting_pixel = maxSize - 11

#Debugging stuff
print(maxSize)
print("Number of arguments:", len(sys.argv))
print("Arguments:", str(sys.argv))
#print(image_data[maxSize])

num_bits_to_extract = extract_text_length(image_data)
#print(num_bits_to_extract)
message = extract_Image(image_data, num_bits_to_extract, string_text_starting_pixel)
message = bin_to_string(message)
print(message)
