"""
Sends binary data to file server.

Author: Minchiuan Gao <minchiuan.gao@gmail.com>
Date: 2015-Oct-29
"""

import requests
from account.configuration import websites


class FileSender(object):
    file_server = websites.file_server

    @staticmethod
    def send_file(file_binary_data):
        '''
        returns:
            the file saved name in file server, the client could get this file
            by this name.
        '''
        r = requests.post(FileSender.file_server, files=file_binary_data)
        print(r.json())


if __name__ == '__main__':
    file_data = open('')
