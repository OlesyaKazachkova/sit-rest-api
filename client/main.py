from urllib.parse import urljoin
import requests
import json


class Client:
    def __init__(self, username, password) -> None:
        self.url = "http://127.0.0.1:5000/"
        self.username = username
        self.password = password
        # Регистрируем на всякий случай, если он там уже есть, то вернётся 400
        requests.post(urljoin(self.url, 'user'),
                      auth=(self.username, self.password))

    def get_all(self):
        response = requests.get(urljoin(self.url, 'todo'),
                                auth=(self.username, self.password))
        response.raise_for_status()
        content = json.loads(response.content)
        if not content[0]:
            return "Что-то пошло не так, попробуйте позже"
        return content[1]

    def add_task(self, task_name):
        response = requests.post(urljoin(self.url, 'todo'),
                                 auth=(self.username, self.password),
                                 data={'task_name': task_name})
        response.raise_for_status()
        content = json.loads(response.content)
        if not content['success']:
            return 'Что-то пошло не так, попробуйте позже'
        return content['success']

    def update_task(self, task_id, value: bool):
        response = requests.put(urljoin(urljoin(self.url, '/todo/'), str(task_id)),
                                auth=(self.username, self.password),
                                data={'task_status': str(value)})
        response.raise_for_status()
        content = json.loads(response.content)
        if not content['success']:
            return 'Что-то пошло не так, попробуйте позже'
        return content['success']

    def delete_task(self, task_id):
        response = requests.delete(urljoin(urljoin(self.url, '/todo/'), str(task_id)),
                                   auth=(self.username, self.password))
        response.raise_for_status()
        content = json.loads(response.content)
        if not content['success']:
            return 'Что-то пошло не так, попробуйте позже'
        return content['success']


c = Client('Olesya', '12345')
print(c.get_all())
print(c.delete_task(2))
print(c.get_all())
print(c.update_task(1, True))
print(c.get_all())
print(c.add_task('DO IT'))
print(c.get_all())
