'''
Import users from csv file
'''

import requests
import hashlib

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def parse_itme(item):

    item = item.strip()

    if item == 'False':
        item = False

    if item == 'True':
        item = True

    return item


def send_post(phone, password, nickname, first_name, gender, marital_status, client):
    post = {
        'phone': phone,
        'password': computeMD5hash(password),
        'nickname': nickname,
        'first_name': first_name,
        'gender': gender,
        'marital_status': marital_status
    }

    r = requests.post('http://192.168.0.153:8000/account/user/', data=post)
    print r.text
    # resp = client.post('/account/user/', post)
    # print resp.data


def read_user_infor_from_file(client=None):
    filename = '/Users/develop/Workspace/my-family/maili-develop/account/tests/user_login.csv'

    data = open(filename, 'r')

    for line in data.readlines():
        datas = line.split(',')
        datas = map(parse_itme, datas)
        (phone, password, nickname, first_name, gender, marital_status) = tuple(datas)

        send_post(phone, password, nickname, first_name,
                  gender, marital_status, client)

if __name__ == '__main__':
    read_user_infor_from_file()
