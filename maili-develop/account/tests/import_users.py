'''
Import users from csv file
'''

import requests


def parse_itme(item):

    item = item.strip()

    if item == 'False':
        item = False

    if item == 'True':
        item = True

    return item


def send_post(phone, password, nickname, first_name, gender, marital_status):
    post = {
        'phone': phone,
        'password': password,
        'nickname': nickname,
        'first_name': first_name,
        'gender': gender,
        'marital_status': marital_status
    }

    r = requests.post('http://192.168.0.153:8000/account/user/', data=post)
    print(r.text)


def read_user_infor_from_file():
    filename = './user_login.csv'

    data = open(filename, 'r')

    for line in data.readlines():
        datas = line.split(',')
        datas = map(parse_itme, datas)
        (phone, password, nickname, first_name, gender, marital_status) = tuple(datas)

        send_post(phone, password, nickname, first_name, gender, marital_status)

if __name__ == '__main__':
    read_user_infor_from_file()
