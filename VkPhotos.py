import time
import requests
from datetime import datetime
    
class VkPhotos:
    url = 'https://api.vk.com/method/photos.get'
    def __init__(self,id,token,vk_version):
        self.id = id
        self.token = token
        self.vk_version = vk_version
    def get_vk_photo_response_json(self):
        """
        Получает параметры фотографий  от API VK,
        и выдает ошибку если профиль отсутствует,или если фотографий в профиле нет,
        также если фотографий в профиле меньше 5 сообщит об этом.'
        """
        params = {
            'owner_id':self.id,
            'access_token': self.token, 
            'v':self.vk_version,
            'album_id':'profile',
            'photo_sizes':'0',
            'extended':'1',
            'rev':'1'}
        response = requests.get(url=self.url,params=params).json()
        count = response['response']['count']
        if count == 0:
            print('Фотографии в профиле отсутствуют')
        elif response['response'] == 0:
            print('Профиль не существует,введите корректный id')
        else:
            if count >= 5:
                return response['response']['items']
            else:
                if count < 5:
                    print(f'В профиле {count} фотографий')
                    return response['response']['items']
    
    def get_vk_photo_sorted(self):
        """
        Получает json c информацией о фотографиях от предыдущей функции,
        и сортирует их по типу фотографий представленных в API VK в новый словарь,
        присваивая имени файла значение лайков и даты загрузки фотографии.
        Возвращает список со словарями.
        
        """
        res = self.get_vk_photo_response_json()
        vk_sizes = dict(s=1,m=2,o=3,p=4,q=5,r=6,x=7,y=8,z=9,w=10)
        list_photos = []
        for items in res:
            time.sleep(0.02)
            name ={}
            ph_date = items['date']
            ph_date = datetime.utcfromtimestamp(ph_date).strftime('%Y-%m-%d_%H-%M-%S')
            name['file_name'] = items['likes']['count'],ph_date
            size_max = max(items['sizes'],key = lambda x:vk_sizes[x['type']])
            name['size'] = size_max['type']
            name['url'] = size_max['url']
            list_photos.append(name)
        return list_photos

