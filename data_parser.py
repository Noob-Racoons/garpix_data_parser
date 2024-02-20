import os
import json
import random
from zipfile import ZipFile
from time import sleep

from garpix_api import GarpixAPI


class GLSDataParser:
    def __init__(self, boxes_data_dir='./boxes_data/'):
        self._api = GarpixAPI()
        self._boxes = []
        zFiles = [f for f in os.listdir(boxes_data_dir)]
        for zFile in zFiles:
            with ZipFile(f'{boxes_data_dir}{zFile}') as zip_f:
                files = zip_f.namelist()
                for file in files:
                    with zip_f.open(file) as json_file:
                        json_data = json.load(json_file)
                        box = {}
                        for item in json_data['data_result']['boxes']:
                            box['title'] = 'Коробка'
                            box['width'] = item['size']['width']
                            box['height'] = item['size']['height']
                            box['length'] = item['size']['length']
                            box['mass'] = item['mass']
                            box['stacking'] = item['stacking']
                            box['stacking_limit'] = item['stacking_limit']
                            box['turnover'] = item['turnover']
                            try:
                                box['is_rotate_y'] = item['is_rotate_y']
                            except KeyError:
                                pass
                            box['count'] = random.randint(1, 5)
                            self._boxes.append(box)

    def login(self, username, password):
        self._api.login(username, password)

    def logout(self):
        self._api.logout()

    def calc_result(self):
        project = self._api.create_project('Data parser project')
        boxes = self._create_boxes_set()
        # van = self._api.get_van(435)
        calculation_request_body = {
            "project": project['id'],
            "input_data": {
                "cargo_spaces": [
                    435
                ],
                "groups": [
                    {
                        "title": "my cool cargo",
                        "pallet": 0,
                        "cargoes": boxes,
                        "sort": 1
                    }
                ],
                "userSort": True
            },
        }

        done = False
        result = None
        status = {}
        retries = 5
        self._api.create_calculation(calculation_request_body)
        while not done:
            if retries == 0:
                done = True
                status['status'] = 'error'
                status['message'] = 'Max retries exceeded!'
                status['code'] = 0
            else:
                sleep(5)
                response = self._api.get_project(project['id'])
                if response.status_code == 200:
                    result = response.json()
                    print(f'Current project: {project["id"]} Status: {result["last_calc"]["status"]}')
                    if result['last_calc']['status'] == 'success':
                        done = True
                        status['status'] = 'success'
                    elif result['last_calc']['status'] in ['calculating', 'in_queue']:
                        pass
                    else:
                        retries -= 1
                else:
                    done = True
                    status['status'] = 'error'
                    status['message'] = 'HTTP Error'
                    status['code'] = response.status_code

        self._api.delete_project(project['id'])

        return result, status

    def _create_boxes_set(self):
        boxes_set = []
        boxes_count = random.randint(5, 50)
        for i in range(boxes_count):
            box = random.choice(self._boxes)
            boxes_set.append(box)

        return boxes_set
