import json
import requests
import pytesseract
import cv2
import pyocr
import pyocr.builders
import sys
from PIL import Image

def get_text_from_captcha(img_path):
    payload = {'isOverlayRequired': False,
                   'apikey': "1b7dda232088957",
                   'language': "eng",
               'OCREngine' : 2
                   }

    with open(img_path, 'rb') as fp:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={img_path: fp},
                              data=payload)

    x = json.loads(response.content.decode())

    y = x["ParsedResults"][0]["ParsedText"]
    return str(y)

def resolve(img_path):
    enhancedImage = enhance1(img_path)
    #cv2.imwrite("inhanced_image.jpg", enhancedImage)
    #print(enhancedImage)
    #captcha_text = pytesseract.image_to_string(enhancedImage)
    #print(pytesseract.image_to_string(enhancedImage))
    return pytesseract.image_to_string(enhancedImage)
    #text = captcha_text.replace(" ", "")
    #print(captcha_text)
    #return str(captcha_text)
def enhance1(img_path):
    image1 = cv2.imread(img_path)
    #print(image1)
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) 
    #thresh = 50
    #im_bw = cv2.threshold(thresh3, thresh, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 2))
    erosion = cv2.erode(thresh1, kernel, iterations = 1)
    return erosion

def resolve1(img_path):
    im = Image.open(img_path)
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    langs = tool.get_available_languages()
    lang = langs[langs.index('eng')]

    #file_path = './image/downloadedpng.png'
    #txt = tool.image_to_string(Image.open(file_path),lang=lang,builder=pyocr.builders.TextBuilder())
    txt = tool.image_to_string(im,lang=lang,builder=pyocr.builders.TextBuilder())
    return txt
