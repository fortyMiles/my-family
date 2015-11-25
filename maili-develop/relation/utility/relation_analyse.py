"""
Analyser of the relation.

@author: Minchiuan Gao <minchiuan.gao@gmail.com>
Build Date: 2015-Nov-25 Wed
"""


class RelationValue(object):
    def __init__(self, title, weight, abbr, level):
        self.title = title
        self.weight = weight
        self.abbr = abbr
        self.level = level


class Analyse(object):
    def __init__(self):
        self.weigth = {}

    def caculate_value(self, r1, r2, r3):
        pass

    def caculate_weigth(self, person1, peron2):
        '''
        Caculates the weight between person1 and person2
        '''
        pass

    def read_data(self):
        data = open('./data.data', 'r')
        for line in data.readlines():
            row = line.split('\t')
            relationValue = RelationValue(row[0], row[1], row[2], row[3])
            self.weight


if __name__ == '__main__':
    analyse = Analyse()
    analyse.read_data()
