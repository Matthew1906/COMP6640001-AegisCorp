from base64 import b64encode
from imagekitio import ImageKit
from os import getenv

imagekit = ImageKit(
    private_key = getenv('IMAGEKIT_PRIVATE_KEY'),
    public_key = getenv('IMAGEKIT_PUBLIC_KEY'),
    url_endpoint = 'https://ik.imagekit.io/matthew1906'
)

def get_image_url(file, filename):
    res = imagekit.upload_file(
        file=b64encode(file),
        file_name=filename,
        options={
            'folder':'/aegisCorp/',
            'use_unique_file_name':False,
        }
    )
    return imagekit.url({
        "path":f'/aegisCorp/{filename}',
        'url_endpoint':"https://ik.imagekit.io/matthew1906/"
    })