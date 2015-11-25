'''
Self defined errors

@author Minchiuan Gao <minchiuan.gao@gmail.com>
Build Date: 2015-Nov-25 Wed
'''

class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

