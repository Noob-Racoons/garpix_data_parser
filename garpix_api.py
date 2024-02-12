import requests
import json


class GarpixAPI:
    def __init__(self):
        self._session = requests.session()
        self._host = 'https://back.glsystem.net'
        self._headers = {'Content-Type': 'application/json'}
        self._access_token = None
        self._refresh_token = None
        self._logged_in = False

    def login(self, username, password):
        endpoint = '/api/v2/auth/login/'
        payload = {'username': username, 'password': password}
        response = self._session.post(url=f'{self._host}{endpoint}', data=payload)
        if response.status_code == 200:
            response_body = response.json()
            self._access_token = response_body['access_token']
            self._refresh_token = response_body['refresh_token']
            self._headers['Authorization'] = f'Bearer {self._access_token}'
            self._logged_in = True

    def logout(self):
        endpoint = '/api/v2/auth/logout/'
        self._session.post(url=f'{self._host}{endpoint}')

    def create_project(self, project_name):
        project = None
        endpoint = '/api/v2/project/'
        payload = {'title': project_name}
        response = self._session.post(url=f'{self._host}{endpoint}', json=payload, headers=self._headers)
        if response.status_code == 201:
            project = response.json()
        else:
            print(f'Error {response.status_code}')
        return project

    def delete_project(self, project_id):
        endpoint = f'/api/v2/project/{project_id}/'
        self._session.delete(url=f'{self._host}{endpoint}', headers=self._headers)

    def get_projects_list(self,):
        endpoint = f'/api/v2/project/'
        response = self._session.get(url=f'{self._host}{endpoint}', headers=self._headers)
        return response.json()

    def get_project(self, project_id):
        endpoint = f'/api/v2/project/{project_id}/'
        response = self._session.get(url=f'{self._host}{endpoint}', headers=self._headers)
        return response

    def get_van(self, van_id):
        endpoint = f'/api/v2/van/{van_id}/'
        response = self._session.get(url=f'{self._host}{endpoint}', headers=self._headers)
        return response.json()

    def create_calculation(self, payload):
        endpoint = f'/api/v2/calculation/'
        response = self._session.post(url=f'{self._host}{endpoint}', json=payload, headers=self._headers)
        return response.json()
