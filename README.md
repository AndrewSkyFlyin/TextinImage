# TextinImage

This program embeds a text message inside an image.
It uses jpg/jpeg images to embed messages and saves as a png file.
The message is stored in each pixel starting from the bottom right side of the image.

Example:
```
$ python main.py -e -i "cat.jpg" -o "cat.png" -t "I am hidden in the shadow of pixels."
$ python main.py -d -i "cat.png"
I am hidden in the shadow of pixels."
```
Arguments:
-e: Specifies embedding a message into an image.
-d: Specifies extracting a message from an image.
-i: The input jpeg file.
-o: The output png file.
-t: The contents of the message you wish to embed.
