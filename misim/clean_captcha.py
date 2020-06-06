from PIL import Image
from PIL import ImageOps

image_path = 'captcha_original.png'


def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)

    borderImage = ImageOps.expand(image, border=20, fill='gray')
    borderImage.save('proccessed' + imagePath)


def cleanImage2(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 1 else 255, '0')
    # image = image.point(lambda x: 0 if x < 143 else 255)
    # borderImage = ImageOps.expand(image, border=20, fill='gray')
    image.save('proccessed_' + imagePath)


cleanImage2(image_path)
