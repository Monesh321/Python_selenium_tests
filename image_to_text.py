# import the following libraries 
# will convert the image to text string 
import pytesseract

# adds image processing capabilities 
from PIL import Image

# converts the text to speech
# import pyttsx3

# translates into the mentioned language
# from googletrans import Translator

# opening an image from the source path
img = Image.open('test_03_verify_get_a_quote_list0.png')

# describes image format in the output 
print(img)
# path where the tesseract module is installed 
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# converts the image to result and saves it into result variable 
result = pytesseract.image_to_string(img)
# write text in a text file and save it to source path    
with open('abc2.txt', mode='w') as file:
    if result != ' ':
        file.write(result)
        # print(result)

with open('abc2.txt', mode='r') as file:
    result = [result.strip() for result in file.readlines() if len(result.strip()) != 0]

for res in result:
    print(res.strip())
