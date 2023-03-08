from VkPhotos import VkPhotos
from YandexDisk import YandexDisk

def main(id,yandex_token:str,vk_token:str,vk_version:str):
    """Принимает id и токен Яндекс.Полигона от пользователя,
    а также считанные из файла config.txt токен VK API и версию VK API.
    Создает экземпляры классов VkPhotos и YandexDisk,
    Создает папку Photos from VK profile на Яндекс.Диске,
    либо сообщает что папка уже существует,либо сообщает об ошибке.
    Загружает 5 или меньше фотографий из профиля ВК,
    Показывает прогресс загрузки по одной фотографии,
    Сообщает о том что фотография загружена на Яндекс.Диск,
    Сообщает о том что сформирован выходной файл output.json.
    """
    id = id
    yandex_token = yandex_token
    vk_token = vk_token
    Photographer = VkPhotos(id,vk_token,vk_version)
    Backuper =  YandexDisk(yandex_token)
    folder_create = Backuper.create_yandex_disk_folder()
    if folder_create == 201:
        print('Папка c названием Photos from VK profile создана')
    elif folder_create == 409:
        print('Папка с названием Photos from VK profile уже существует')
    else:
        print('При создании папки произошла ошибка')
    Backuper.upload_photos_from_vk(Photographer.get_vk_photo_sorted())
    
    
    
if __name__ == '__main__':
    yandex_token = input('Введите OAuth токен для Яндекс.Полигонa  ')
    id = int(input('Введите id пользователя VK,c профиля которого необходимо скачать фотографии(цифры)  '))
    """Получение токена VK API и версии VK API"""   
    with open('config.txt','r',encoding='utf-8') as file:
        file.readline()
        vk_token = file.readline()
        file.readline()
        vk_version = file.readline()
        file.readline()
    main(id,yandex_token=yandex_token,vk_token=vk_token,vk_version=vk_version)
        