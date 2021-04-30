from pprint import pprint
import requests
from requests import get
from json import loads
import os
import time

TOKEN = input('Введите Yandex token:')
class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)

        for links in response.json()['items']:
            if name_of_folder in links['path']:
                print('file_name : '+str((links)['name']), '\nsize : '+str((links)['size']))
            else:
                pass

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        # pprint(response.json())
        return response.json()

    def upload_folder(self, name_of_folder):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": name_of_folder, "overwrite": "true"}
        response = requests.put(upload_url, headers=headers, params = params)
        if response.status_code == 201:
            print('Success')

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')

class api:
    def __init__(self, token):
        self.__token__ = token
        self.__api__ = 'https://api.vk.com/method/'
        self.params = {
            'user_id' : '139620093',
            'access_token' : token,
            'v' : '5.130',
        }

    def get_photos_from_album(self, owner_id, album_id, count):
        method = f'{self.__api__}photos.get'
        result = get(method, params={
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_sizes': 1,
            'count': count,
            'access_token': self.__token__,
            'version': '5.130'
        })
        return result.json()


    def get_photos_from_album_list(self, owner_id, album_id, count):
        method = self.__api__ + 'photos.get'
        groups_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_sizes': 1,
            'count': count,
            'access_token': self.__token__,
            'version': '5.130'
        }
        res = requests.get(method, params={**self.params, **groups_params})
        # return loads(res.text)
        links = res.json()['response']['items']
        link_list = []
        for x in range(100):
            for link in links:
                urls = link['sizes']
                try:
                    url1 = urls[x]
                except Exception:
                    pass
                if 'r' in url1.values():
                    link_list.append(url1['url'])

                else:
                    pass
        return link_list

    def get_likes(self, owner_id, album_id, count):
        method = self.__api__ + 'photos.get'
        groups_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_sizes': 1,
            'count': count,
            'access_token': self.__token__,
            'version': '5.130',
            'extended' : 1
        }
        res = requests.get(method, params={**self.params, **groups_params})

        links = res.json()['response']['items']
        link_list1 = []
        for link in links:
            urls = link['likes']['count']
            link_list1.append(urls)
        return link_list1

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
vk_cl = api(token)

vk_id = input('Введите vkontakte ID:')
photos = vk_cl.get_photos_from_album_list(vk_id, 'profile', 100)
likes = vk_cl.get_likes(vk_id, 'profile', 100)
diction = {}
the_list = []
for like in likes:
    time_num = like + time.time()
    clear_num = time_num - int(time.time())
    the_list.append(time_num)
# pprint(photos)

import urllib.request
xx = 'C:\\Users\\Laterman\\PycharmProjects\\pythonProject\\2.4.files\\sorted\\Photos\\'

def dl_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)

for n in range(len(photos)):
    diction[photos[n]] = likes[n]
# pprint(diction)
set = set()
second_l = []
for key, value in diction.items():
    if value not in set:
        set.add(value)
        second_l.append(value)
        dl_jpg(key, xx, str(value))
    if value in set:
        new_val = value + time.time()
        clear_num = new_val - int(time.time())
        second_l.append(clear_num)
        dl_jpg(key, xx, str(clear_num))
ya = YandexDisk(token=TOKEN)
name_of_folder = 'Vk_photos'
ya.upload_folder('/'+name_of_folder)
from tqdm import tqdm
for title in tqdm(second_l):
    ya.upload_file_to_disk(('/'+name_of_folder+'/'+str(title)+'.jpg'), ('C:\\Users\\Laterman\\PycharmProjects\\pythonProject\\2.4.files\\sorted\\Photos\\'+str(title)+'.jpg'))

pprint(ya.get_files_list())

