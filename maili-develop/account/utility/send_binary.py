"""
Sends binary data to file server.

Author: Minchiuan Gao <minchiuan.gao@gmail.com>
Date: 2015-Oct-29
"""

import requests
from account.configuration import websites


class FileSender(object):
    file_server = websites.file_server
    # file_server = 'http://127.0.0.1:8777/file/upload'

    @staticmethod
    def send_file(file_binary_data):
        '''
        returns:
            the file saved name in file server, the client could get this file
            by this name.
        '''
        files = {'file': file_binary_data}
        r = requests.post(FileSender.file_server, files=files)
        json_data = r.json()
        return json_data.values()[0]


if __name__ == '__main__':
    file_data = open('test.jpg', 'rb')
    print FileSender.send_file(file_data)
