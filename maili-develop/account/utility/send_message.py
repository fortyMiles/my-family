"""
Send message by a phone number.
"""
import datetime
import requests
import hashlib

VER_ACCOUNT_SID = "8a70971adf5ba2d4598193cc03fcbaa2"
VER_AUTH_TOKEN = "7c7c4e5d324b7efbf75db740fdf6a253"
VER_TEM_ID = "12750"
VER_APP_ID = "71ca63be653c45129a819964265eccec"
VER_URL = "https://www.ucpaas.com/maap/sms/code"
VER_VERSION = "2014-06-30"


def random_code(number):
    def add_one(item):
        value = int(item) * 7 / 3
        return str(value)

    number = map(add_one, number[-6:])
    return number


def send_message(phone, code):
    '''
    Sends message by phone number
    ---
    args:
        phone: phone number
    '''

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    print current_time

    m = hashlib.md5()
    m.update(VER_ACCOUNT_SID + current_time + VER_AUTH_TOKEN)
    md5_code = m.hexdigest()

    verify_code = {
        'sid': VER_ACCOUNT_SID,
        'appId': VER_APP_ID,
        'sign': md5_code,
        'time': current_time,
        'templateId': VER_TEM_ID,
        'to': phone,
        'param': code
    }

    print("sending message..")
    response = requests.post(VER_URL, data=verify_code, verify=False)
    status = response.json()['resp']['respCode']

    success = False
    if status == '000000':
        success = True

    print response.text
    return success


if __name__ == '__main__':
    phone = '18857453090'
    print send_message(phone, '123456')
