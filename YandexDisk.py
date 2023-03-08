import time
import json
import requests
from tqdm import tqdm


class YandexDisk: 
    
    base_path = '/Photos from VK profile/'
    """Инициализация класса"""
    def __init__(self,yandex_token):
        self.yandex_token = yandex_token
            
    def get_headers(self):
        """Метод для передачи заголовков"""
        return {
            'Content_Type': 'application/json',
            'Authorization': f'OAuth {self.yandex_token}'
        }
    
    def create_yandex_disk_folder(self):
        """Метод создания папок в Яндекс.Диске"""
        path_name = self.base_path
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path_name, 'overwrite': 'true'}
        response = requests.put(url=url,params=params,headers=headers)
        return response.status_code
    
    def upload_photos_from_vk(self,data):
        """Метод загрузки фото на Яндекс диск
        Получает данные от функции из класса VkPhotos,
        Проверяет кол-во фотографий в списке,и если фотографий 5 или больше,или меньше 5,загружает их на Яндекс.Диск,
        Возвращает json файл с выходными данными,а также показывает прогресс загрузки фото на Яндекс.Диск.
        """
        self.data = data
        headers = self.get_headers()
        if len(data) >= 5:
            number = 5 
        else:
            if len(data) < 5:
                number = (len(data))
        with open('output.json','w',encoding='utf-8') as output_file:
            output_list = []
            for i in tqdm(range(0,number)):
                time.sleep(0.02)
                params = {'url':data[i]['url'], 'path':self.base_path+str(data[i]['file_name']) }
                url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                response = requests.post(url=url,params=params,headers=headers)
                if response.raise_for_status() == None:
                    output_info = dict(file_name = data[i]['file_name'],size = data[i]['size'])
                    output_list.append(output_info)
                    print(' Файл загружен')
                else:
                    if response.raise_for_status() != None:
                        print('При загрузке файла произошла ошибка')
            result = json.dumps(output_list,indent=2)
            output_file.write(result)
            return print('Output.json cоздан')
    