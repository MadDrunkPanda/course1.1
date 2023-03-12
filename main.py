import requests
from pprint import pprint

TOKEN_YA = ''
TOKEN_VK = ''
user = ''


class VkUser():
    def __init__(self,token_ya):
        self.token_ya = token_ya

    def get_photos_dict(self,user_id):
        self.user_id = user_id
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': TOKEN_VK,
            'v': '5.131',
            'owner_id': user,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1,
            'rev': 0,
            'count': 500
        }
        req = requests.get(url, params=params).json()
        postlist = req['response']['items']
        photo_dict = {}
        for dict in postlist:
            for i in dict['sizes']:
                if i['type'] == 'z':
                    if dict['likes']['count'] in photo_dict.values():
                        photo_dict[i['url']] = str(dict['likes']['count']) + '/' + str(dict['date'])
                    else:
                        photo_dict[i['url']] = dict['likes']['count']
        return  photo_dict

    def upload_files(self,user_id,count=5):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_ya)
        }
        photo_dict = self.get_photos_dict(user_id=user_id)
        while count > 0:
            for image in photo_dict.items():
                params = {
                    'path' : f'Folder/{image[1]}.jpg',
                    'overwrite' : 'true'
                }
                count -= 1
                res = requests.get(files_url, headers=headers, params=params)
                url = res.json()['href']
                response = requests.put(url, data = open(image[0], 'rb'))
                response.raise_for_status()







user_vk = VkUser(TOKEN_YA)
pprint(user_vk.upload_files(user,3))

