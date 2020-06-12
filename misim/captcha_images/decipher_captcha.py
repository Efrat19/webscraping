import time
from time import sleep

from bestcaptchasolverapi3.bestcaptchasolverapi import BestCaptchaSolverAPI

# !/usr/bin/python3.7

ACCESS_TOKEN = '22AE66A0BC7348D0B199995AF2DF8D18'


# for more details check https://bestcaptchasolver.com/captchabypass-api
def extract_captcha_from_processed_img(captcha_img_path):
    start = time.time()

    bcs = BestCaptchaSolverAPI(ACCESS_TOKEN)  # get access token from: https://bestcaptchasolver.com/account

    # check account balance
    # ---------------------------
    balance = bcs.account_balance()  # get account balance
    print('Balance: {}'.format(balance))  # print balance

    print('Solving image captcha ...')
    data = {}
    data['image'] = captcha_img_path

    # optional parameters
    # -------------------
    # data['is_case'] = True, default: False
    # data['is_phrase'] = True, default: False
    # data['is_math'] = True, default: False
    # data['alphanumeric'] = 1 (digits only) or 2 (letters only), default: all characters
    # data['minlength'] = minimum length of captcha text, default: any
    # data['maxlength'] = maximum length of captcha text, default: any
    # data['affiliate_id'] = '5ee37057c341572c523e4031'

    id = bcs.submit_image_captcha(data)  # submit image captcha (case_sensitive param optional)
    image_text = None
    # None is returned if completion is still in pending
    while image_text == None:
        image_text = bcs.retrieve(id)['text']  # get the image text using the ID
        sleep(5)

    print('Captcha text: {}'.format(image_text))
    end = time.time()
    print("took {} seconds for solving captcha".format(end - start))

    return image_text


# main method
def main():
    try:
        extract_captcha_from_processed_img(
            '/Users/idan.narotzki/PycharmProjects/webscraping/misim/captcha_images/screenshot_processed.png')
    except Exception as ex:
        print('[!] Error occured: {}'.format(ex))


if __name__ == "__main__":
    main()
