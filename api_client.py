import requests


class APIClient:
    def __init__(self, token):
        self.base_url = 'https://dniruc.apisperu.com/api/v1/dni/'
        self.token = token

    def get_user_info(self, dni):
        url = self.base_url + dni + '?token=' + self.token
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('success'):
                return response_json
            else:
                print(f"Error en la respuesta de la API: {response_json}")
                return None
        else:
            print(f"Error en la solicitud HTTP: {response.status_code}")
            return None
