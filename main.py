from pprint import pprint

import requests


class YaUploader:
    def __init__(self, tooken: str):
        self.token = tooken

    files_url = "https://cloud-api.yandex.net/v1/disk/resources/files"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_upload_link(self, file_path: str) -> dict:
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.headers)
        jsonify = response.json()
        pprint(jsonify)
        return jsonify


    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, 'rb') as file:
            response = requests.put(href, data=file)
            if response.status_code == 201:
                print("файл загружен")
                return True
            print("файл не загружен потому что", response.status_code)
            return False


class VkRequester:
    def __init__(self, token: str, id):
        self.token = token
        self.id = id

    def get_request(self, amount=5): #функция делает запрос, находит числовой id в ВК и выдает информациию о аватарках пользователя
        resp = requests.get("https://api.vk.com/method/users.get", params=dict(access_token=self.token, user_ids=self.id, v='5.131')).json()
        for i in  resp['response']:
            ids = i['id']
        response = requests.get("https://api.vk.com/method/photos.get", params=dict(access_token=self.token, owner_id=ids, v='5.131',album_id='profile', extended='1', count=amount)).json()
        return response

    def get_file_name(self, number, amount=None): #находит количество лайков для имя файла с фото
        file = self.get_request(amount)
        for info in file.items():
            body = list(info[1].values())[1]
            for likes in body[number]['likes'].values():
                r_1 = likes
                return (r_1+body[number]['date'])


    def photo_get(self, number, amount=None): #выдает размер фото и ссылку на него
        file = self.get_request(amount)
        for info in file.items():
            val = list(info[1].values())[1]
            for k, v in val[number].items():
                if k == 'sizes':
                    fotos = v
            lengh = len(fotos)
            foto = fotos[lengh - 1]
            final = list(foto.values())
            return (final[1], final[3])



    def file_create(self,number, amount=None): #создает файл с фотографией
        p = self.photo_get(number, amount=None)[1]
        apiphoto = requests.get(p)
        out = open(f'{self.get_file_name(number, amount=None)}.jpeg', "wb")
        out.write(apiphoto.content)
        out.close()
        return f'{self.get_file_name(number)}.jpeg'

    def counter(self): #считает сколько у пользователя аватарок, чтобы знать, сколько раз нужно запустить код
        file = self.get_request()
        for info in file.items():
            for count in info[1].values():
                return count





if __name__ == '__main__':
    # # Получить токен от пользователя
    tooken = input('Введите ваш токен от Яндекс диска: ')
    uploader = YaUploader(tooken)
    ids = input('Введите ваш id во вконтакте: ')
    tokenVK = 'b5d9a5e6b5d9a5e6b5d9a5e6d9b6cbe76fbb5d9b5d9a5e6d61f686cf8af3715f7137d7f'
    test = VkRequester(tokenVK, ids)


    for proccess in range(0, test.counter()):
        uploader.upload(test.file_create(proccess))
