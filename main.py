# NOTE: Some of the functions were created referencing Reza Nikoopour's version of this project.
# url: https://github.com/rnikoopour/TextInImage

import sys
import argparse
from PIL import Image


# Expands a binary number to 8-bits if it isn't already.
# Based on Reza Nikoopour's function
def expand_to_8_bits(bit_string):
    zeroes = '0' * (8 - len(bit_string))
    full_string = zeroes + bit_string
    return full_string


# Expands a binary number to 32-bits if it isn't already.
# Based on Reza Nikoopour's function
def expand_to_32_bits(bit_string):
    zeroes = '0' * (32 - len(bit_string))
    full_string = zeroes + bit_string
    return full_string


# Converts a string of text into a binary string.
# Based on Reza Nikoopour's function
def string_to_bin(string):
    binary_string = ''
    for letter in string:
        letter_as_int = ord(letter)  # Convert to ascii number
        letter_as_binary = format(letter_as_int, 'b')   # Convert ascii number to binary
        letter_as_binary = expand_to_8_bits(letter_as_binary)  # Expands binary number to 8 bits
        binary_string += letter_as_binary
    return binary_string


# Converts a binary string into a normal text string.
# Based on Reza Nikoopour's function
def bin_to_string(binary):
    # Splits the binary into an array by chunks of 8 characters long.
    binary_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''
    for chunk in binary_chunks:
        # Converts each binary chunk into the ascii decimal value.
        ascii_value = int(chunk, 2)
        # Converts the ascii decimal value into its character representation.
        # The char is then appended to the text string variable.
        text += chr(ascii_value)
    return text


# Extracts the least significant bit value of the passed bit string.
def extract_last_bit(integer):
    # Convert the passed value into binary format.
    last_bit = list(format(integer, 'b'))
    # Return the last element of the last_bit array, which is the least significant bit.
    return last_bit[-1]


# Calculates the number of bits required to embed/extract message.
def num_bits_in_string(string):
    return len(string) * 8


# The main message extraction function.
def extract_image(image_data, number_of_bits, index):
    bit_string = ''
    # cut_off is where the message extraction will stop at.
    cut_off = index - number_of_bits
    while index >= cut_off:
        # Extract the least significant bit of each RGB value and append to bit_string
        # Referenced from Reza Nikoopour's bit extraction method.
        red, green, blue = image_data[index]
        index -= 1
        bit_string += extract_last_bit(red)
        bit_string += extract_last_bit(green)
        bit_string += extract_last_bit(blue)
    # print(bit_string[:number_of_bits])  # Debug line
    return bit_string[:number_of_bits]  # Returns everything in the bit_string up until the element equal to the
                                         # number_of_bits variable.


# Calculates the length of the message in number of bits.
def extract_text_length(image_data, string_length_starting_pixel):
    binary_length = extract_image(image_data, binary_message_length, string_length_starting_pixel)
    length2 = int(binary_length, 2)  # Binary to int conversion.
    return length2


# The main function for embedding messages into images.
def embed_in_image(image_data, text, index, max_pixel_capacity):
    num_bits_to_embed = num_bits_in_string(text)  # Calculates number of bits required to embed message.

    if num_bits_to_embed > max_pixel_capacity:
        print('Inputted text to too large to embed.')
        sys.exit(0)

    num_bits_to_embed = format(num_bits_to_embed, 'b')  # Convert to binary format.
    num_bits_to_embed = expand_to_32_bits(num_bits_to_embed)  # Expand binary number to 32 bits.
    # print(num_bits_to_embed) #Debug line

    text_in_binary = string_to_bin(text)   # Works
    # print(text_in_binary)  #Debug line

    # The binary message will be split into individual numbers and placed into an array sequentially.
    binary_string = []
    binary_string += list(num_bits_to_embed)  # Appends num_bits_to_embed to array
    binary_string.extend('0')   # Appends a filler '0' to the empty 33rd bit string, due to alignment reasons.
    binary_string += list(text_in_binary)  # Appends the binary of the actually message to the array.
    updated_image_data = image_data  # Creates a local version of image_data.

    # This while loop will execute while binary_string is not empty.
    # As this loop runs, certain lines will pop the first element of the array until the array empties.
    # This looping termination method reference Reza Nikoopour's embed in binary function.
    while binary_string:
        red, green, blue = image_data[index]
        index -= 1

        temp_var = list(format(red, 'b'))     # Retrieve the bit string value of red into a temp_var array.
        temp_var[-1] = binary_string[0]        # Replace the last element of temp_var with the new bit value.
        binary_string.pop(0)                   # Pop the first element of the binary_string array.
        temp_var = ''.join(temp_var)           # Joins all the elements of the temp_var array back into a single string.
        red = int(temp_var, 2)
        if not binary_string:
            updated_image_data[index+1] = (red, green, blue)
            break

        temp_var = list(format(green, 'b'))
        temp_var[-1] = binary_string[0]
        binary_string.pop(0)
        temp_var = ''.join(temp_var)
        green = int(temp_var, 2)
        if not binary_string:
            updated_image_data[index+1] = (red, green, blue)
            break

        temp_var = list(format(blue, 'b'))
        temp_var[-1] = binary_string[0]
        binary_string.pop(0)
        temp_var = ''.join(temp_var)
        blue = int(temp_var, 2)
        updated_image_data[index+1] = (red, green, blue)

    return updated_image_data


binary_message_length = 32


def main(input_file, output_file, text, encrypt, text_path):
    image = Image.open(input_file)
    image_data = list(image.getdata())
    length, height = image.size
    max_size = (length * height) - 1
    max_pixel_capacity = (max_size * 3) - 33
    string_length_starting_pixel = max_size
    string_text_starting_pixel = max_size - 11

    if text_path:
        with open (text_path, "r") as myfile:
            text2 = myfile.read()

    if encrypt:
        if text_path:
            updated_image = embed_in_image(image_data, text2, max_size, max_pixel_capacity)
        else:
            updated_image = embed_in_image(image_data, text, max_size, max_pixel_capacity)
        image.putdata(updated_image)
        image.save(output_file, 'PNG')
    else:
        num_bits_to_extract = extract_text_length(image_data, string_length_starting_pixel)
        # print(num_bits_to_extract) #
        message = extract_image(image_data, num_bits_to_extract, string_text_starting_pixel)
        message = bin_to_string(message)
        print(message)

        # Debugging stuff
        # print(max_size)
        # print("Number of arguments:", len(sys.argv))
        # print("Arguments:", str(sys.argv))
        # print(image_data[max_size])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Embeds text inside an image.')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-e', action='store_true', help='To specify encrypt', default=False)
    group.add_argument('-d', action='store_true', help='To specify decrypt', default=False)

    parser.add_argument('-i', help='Image to embed text in')
    parser.add_argument('-g', help='Text from text file to embed from')

    parser.add_argument('-t', help='Text to embed')
    parser.add_argument('-o', help='Name of output file', default=None)

    args = parser.parse_args()

    if args.e and not args.t and not args.g:
        print('No message was inputted')
        sys.exit(0)

    if args.e and not args.o:
        print('No output file was specified')
        sys.exit(0)

    main(args.i, args.o, args.t, args.e, args.g)
