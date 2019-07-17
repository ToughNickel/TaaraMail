import base64
from TaaraMail.settings import BASE_DIR


def _base64_coverter(path):
    image = open(BASE_DIR + path, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    image_64_encode_string = image_64_encode.decode('utf-8')
    return image_64_encode_string
