import base64
from random import randint

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from mpi_client.client import MPIClient

from .constants import DNI_DOCUMENT
from .models import Person

MPI_API_TOKEN = 'b87f096c846642159ee9e9d2b135f7d4'


class ReniecClient:
    mpi_client = MPIClient(settings.MPI_API_TOKEN)

    @classmethod
    def search(cls, document_number, birthdate):
        response = cls.mpi_client.get(
            f"{settings.MPI_API_HOST}/api/v1/ciudadano/ver/{DNI_DOCUMENT}/{document_number}/"
        )
        if response:
            citizen = response.json().get('data').get('attributes')
            temp = {
                'document_type': citizen.get('tipo_documento'),
                'document_number': citizen.get('numero_documento'),
                'last_name': f"{citizen.get('apellido_paterno')} {citizen.get('apellido_materno')}",
                'name': citizen.get('nombres'),
            }
            brithdate_reniec = citizen.get('fecha_nacimiento')
            if datetime.strptime(birthdate, '%Y-%m-%d') == datetime.strptime(brithdate_reniec, '%Y-%m-%d'):
                return Person(**temp), None
        return None, 'Los datos que proporciono son incorrectos'

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
