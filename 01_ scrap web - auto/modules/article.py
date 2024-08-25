from web_image import Image
import os

'''
class article is the main class thats unite the all articles objects
'''

class Article:
    def __init__(self, header, sub_header, Image, author = None):
        self.header = header
        self.sub_header = sub_header
        self.author = author
        self.image = Image

    def to_dict(self)-> dict:
        self_dic = {'header':self.header,
                    'sub_header':self.sub_header,
                    'image': self.image.to_dict()}
        if self.author is not None:
            self_dic['author'] = self.author
        
        return self_dic
    

    