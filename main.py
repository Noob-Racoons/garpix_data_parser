import os
import json

from dotenv import load_dotenv
from time import time

from data_parser import GLSDataParser

if __name__ == '__main__':
    load_dotenv()
    parser = GLSDataParser()
    parser.login(os.getenv('GLS_USERNAME'), os.getenv('GLS_PASSWORD'))
    count = 5000
    done = False
    while not done:
        if count == 0:
            done = True
        else:
            filename = str(5001 - count).rjust(4, '0') + '.json'
            start_time = time()
            calcs_list, status = parser.calc_result()
            if status['status'] == 'success':
                with open(f'./data/{filename}', 'w') as f:
                    json.dump(calcs_list, f)
                count -= 1
                print(f'{filename} is saved successfully!')
                print("--- %s seconds ---" % (time() - start_time))
