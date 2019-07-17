from bs4 import BeautifulSoup
from ._base64_converter import _base64_coverter


def replace_src_for_MIME(body):
    body_to_be_returned = body
    soup = BeautifulSoup(body_to_be_returned, 'html.parser')
    attachments = []

    for item in soup.find_all('img'):
        sample_in = item['src']
        name_of_the_image = sample_in.split("/")
        name_of_the_image = name_of_the_image[len(name_of_the_image) - 1]
        sample_out = _base64_coverter(sample_in)
        name = "cid: " + str(name_of_the_image)
        attachments.append({
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "Name": name_of_the_image,
                        "isInline": True,
                        "ContentId": name_of_the_image,
                        "ContentBytes": sample_out
                    })
        item['src'] = name

    return soup.prettify(), attachments
