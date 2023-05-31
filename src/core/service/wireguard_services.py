import os
import requests
from src.core.config import WIREGUARD_URL, WIREGUARD_PASSWORD


class WireGuardAPI:
    def __init__(self):
        self.base_url = WIREGUARD_URL
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json"
        }

    def login(self, password):
        url = f"{self.base_url}/api/session"
        data = {
            "password": password
        }
        response = self.session.post(url, json=data)

        if not response.ok:
            error_message = response.json().get('error') or response.reason
            raise Exception(f"Login failed: {error_message}")

    def logout(self):
        url = f"{self.base_url}/api/session"
        response = self.session.delete(url, headers=self.headers)

        if not response.ok:
            error_message = response.json().get('error') or response.reason
            raise Exception(f"Logout failed: {error_message}")


    def get_clients(self):
        self.login(WIREGUARD_PASSWORD)
        url = f"{self.base_url}/api/wireguard/client"
        response = self.session.get(url, headers=self.headers)

        if not response.ok:
            error_message = response.json().get('error') or response.reason
            raise Exception(f"Error getting clients: {error_message}")

        self.logout()
        return response.json()


    def get_or_create_clients(self, name):

        """Получаем всех, чтобы проверить сущетсвование конфигурации"""
        client = [client for client in self.get_clients() if client['name'] == name]

        if client:
            return client[0]

        else:
            self.login(WIREGUARD_PASSWORD)
            url = f"{self.base_url}/api/wireguard/client"
            response = self.session.post(url=url, json={'name': name})

            if not response.ok:
                error_message = response.json().get('error') or response.reason
                raise Exception(f"Error creating: {error_message}")

            client_id = [client['id'] for client in self.get_clients() if client['name'] == name]
            new_client = response.json()
            new_client.update({'id': client_id})
            self.logout()

        return new_client

    def get_qrcode(self, client_id):
        self.login(WIREGUARD_PASSWORD)
        url = f"{self.base_url}/api/wireguard/client/{client_id}/qrcode.svg"
        response = self.session.get(url, headers=self.headers)

        # Сохраните файл временно
        file_path = 'temp/qrcode.svg'
        with open(file_path, 'wb') as file:
            file.write(response.content)


        if not response.ok:
            error_message = response.json().get('error') or response.reason
            raise Exception(f"Error getting clients: {error_message}")
        self.logout()
        return file

    def get_configuration(self, client_id):
        self.login(WIREGUARD_PASSWORD)
        url = f"{self.base_url}/api/wireguard/client/{client_id}/configuration"
        response = self.session.get(url, headers=self.headers)

        #todo Надо бы записывать этот файл куда-то, а то возможна конкуретность за файл между пользователями
        config_text = response.text
        file_path = 'temp/wg.conf'

        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file:
            file.write(config_text)

        if not response.ok:
            error_message = response.json().get('error') or response.reason
            raise Exception(f"Error getting clients: {error_message}")
        self.logout()
        return file


    def disable_client(self):
        pass
