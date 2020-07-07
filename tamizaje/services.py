import base64
from random import randint

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from datetime import datetime

from .constants import DNI_DOCUMENT
from .models import Person


class ReniecClient:

    @classmethod
    def search_and_create(cls, document_number, birthdate, mock=True):
        if mock:
            data_person = ReniecClient.mock_person(document_number)
            return Person.objects.create(**data_person), None
        # integration with MPI or scrapping reniec - despite of validate that is the right person
        # it could be possible verify document_number and birthdate
        return None, 'Los datos que proporciono son incorrectos'
    
    @staticmethod
    def mock_person(document_number):
        data = {
            '62279648': {
                'document_type': '01',
                'document_number': '62279648',
                'first_last_name': 'Salvador',
                'second_last_name': 'Rivera',
                'name': 'Jharol',
                'birthdate': datetime(1995, 1, 18),
                'gender': 'male'
            }
        }
        return data[document_number]

class Scrapper:

    @staticmethod
    def get_fake_address():
        def extract_key(key):
            span = soup.find('li', {"class": 'col-sm-6'}).find('b', string=f'{key}').parent
            unwanted  = span.find('b')
            unwanted.extract()
            return span.text.strip()
        
        url = 'https://www.bestrandoms.com/random-address-in-pe'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Referer': 'https://www.fakeaddressgenerator.com/All_countries/address/country/Peru',
        }
        response = requests.get(url, headers=headers)
        data = {}
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            data['street'] = extract_key('Street:')
            data['city'] = extract_key('City:')
            data['state'] = extract_key('State/province/area: ')
            return data
        return data
    
    @staticmethod
    def get_face_base64():
        main_host_path = "http://vis-www.cs.umass.edu/lfw/"
        url = f'{main_host_path}alpha_all_{randint(1,25)}.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Referer': 'https://www.fakeaddressgenerator.com/All_countries/address/country/Peru',
        }
        response = requests.get(url, headers=headers)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            images_tags = soup.findAll('img', {'alt': 'person image'})
            face_img = images_tags[randint(0, len(images_tags)- 1)]
            img_downloaded = requests.get(f"{main_host_path}{face_img.get('src')}", headers=headers)
            image_base64 = base64.b64encode(img_downloaded.content)
            return image_base64.decode('utf-8')
