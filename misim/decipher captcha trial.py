import subprocess
from urllib.request import urlretrieve

from PIL import Image
from PIL import ImageOps


def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='gray')
    borderImage.save(imagePath)

    # image = Image.open(imagePath)
    # out = image.point(lambda i: i * 1.1)

    # enh = ImageEnhance.Contrast(image)
    # enh.enhance(1.3).show("30% more contrast")


# Gather prepopulated form values
# imageLocation = bsObj.find("img", {"title": "Image CAPTCHA"})["src"]
# formBuildId = bsObj.find("input", {"name": "form_build_id"})["value"]
# captchaSid = bsObj.find("input", {"name": "captcha_sid"})["value"]
# captchaToken = bsObj.find("input", {"name": "captcha_token"})["value"]
captchaUrl = 'https://www.misim.gov.il/svinfonadlan2010/Telerik.Web.UI.WebResource.axd?type=rca&isc=true&guid=be93139d-cee0-4689-a3d9-35c5556d3cbf'

print(captchaUrl)
pic_name = "11.jpg"
urlretrieve(captchaUrl, pic_name)

# cleanImage(pic_name)

p = subprocess.Popen(["tesseract", pic_name, "captcha"], stdout=
subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
f = open("captcha.txt", "r")

# Clean any whitespace characters
captchaResponse = f.read().replace(" ", "").replace("\n", "")
print("Captcha solution attempt: " + captchaResponse)

# if len(captchaResponse) == 5:
#     params = {"captcha_token": captchaToken, "captcha_sid": captchaSid,
#               "form_id": "comment_node_page_form", "form_build_id": formBuildId,
#               "captcha_response": captchaResponse, "name": "Ryan Mitchell",
#               "subject": "I come to seek the Grail",
#               "comment_body[und][0][value]":
#                   "...and I am definitely not a bot"}
#     r = requests.post("http://www.pythonscraping.com/comment/reply/10",
#                       data=params)
#     responseObj = BeautifulSoup(r.text)
#     if responseObj.find("div", {"class": "messages"}) is not None:
#         print(responseObj.find("div", {"class": "messages"}).get_text())
#     else:
#         print("There was a problem reading the CAPTCHA correctly!")
