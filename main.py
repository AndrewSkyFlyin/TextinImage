import sys, argparse
from PIL import Image

def bit_string_to_8bits(bit_string):
    preceding_zeroes = '0' * (8 - len(bit_string))
    full_string = preceding_zeroes + bit_string
    return full_string

def bit_string_to_32bits(bit_string):
    preceding_zeroes = '0' * (32 - len(bit_string))
    full_string = preceding_zeroes + bit_string
    return full_string

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

def extract_text_length(image_data, string_length_starting_pixel):
    binary_length = extract_Image(image_data, binary_message_length, string_length_starting_pixel)
    length2 = int(binary_length, 2)
    return length2

def embed_in_image(image_data, text):
    num_bits_to_embed = num_bits_in_string(text)
    num_bits_to_embed = format(num_bits_to_embed, 'b')
    num_bits_to_embed = bit_string_to_32bits(num_bits_to_embed)


binary_message_length = 32

def main(input_file, output_file, text, encrypt):
    image = Image.open(input_file)
    image_data = list(image.getdata())
    length, height = image.size
    maxSize = (length * height) - 1
    string_length_starting_pixel = maxSize
    string_text_starting_pixel = maxSize - 11

    if encrypt:
        print("Nothing")
        #Blank for now
    else:
        #print(num_bits_to_extract)
        num_bits_to_extract = extract_text_length(image_data, string_length_starting_pixel)
        message = extract_Image(image_data, num_bits_to_extract, string_text_starting_pixel)
        message = bin_to_string(message)
        print(message)

        #Debugging stuff
        print(maxSize)
        print("Number of arguments:", len(sys.argv))
        print("Arguments:", str(sys.argv))
        #print(image_data[maxSize])







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Embeds text inside an image.')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-e', action='store_true', default=False)
    group.add_argument('-d', action='store_true', default=False)

    parser.add_argument('-i', help='Image to embed text in')

    parser.add_argument('-t', help='Text to embed')
    parser.add_argument('-o', help='Name of output file', default=None)

    args = parser.parse_args()


    if args.e and not args.t:
        print('No message was inputted')
        sys.exit(0)

    if args.e and not args.o:
        print('No output file was specified')
        sys.exit(0)

    main(args.i, args.o, args.t, args.e)
