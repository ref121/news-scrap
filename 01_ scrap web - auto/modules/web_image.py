import requests
import os
import subprocess
from pprint import pprint

'''
class image in chourch of the image object 
the class contain a static variable to count the imgages to name each one of image object
'''

class Image:
    image_num = 0
    def __init__(self, image_url_path):
        self.url_path = image_url_path
        self.path_to_save = f'{os.getcwd()}/static/images/'
        self.image_num = Image.image_num
        Image.image_num += 1
        self.image_name = f'image_{self.image_num}.png'

    # use requests library to download the image giving url
    def download_image(self)-> object:
        response = requests.get(self.url_path, stream=True)
        if response.status_code == 200:
            with open(self.path_to_save + self.image_name, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to retrieve the image. Status code: {response.status_code}")
        return self


    def to_dict(self)-> dict:
        return {'url': self.url_path,
                'image_name': self.image_name,
                'image_number': self.image_num,
                'saved_path': self.path_to_save}






