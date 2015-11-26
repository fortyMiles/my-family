'''
Read the data to db.

@author Minchiuan Gao <minchiuan.gao@gmail.com>
Build Date: 2015-Nov-25 Wed
'''
from relation.models import RelationValue


def build_model():
    data = open('/Users/develop/Workspace/my-family/maili-develop/relation/utility/data.data', 'r')

    def change_to_int(e):
        if e.isdigit():
            e = int(e)
        return e

    for line in data.readlines():
        row = line.split('\t')
        row = map(change_to_int, row)
        (title, weight, abbr, level, cft, cfa, cmt, cma) = tuple(row)

        relation = RelationValue(title=title, weight=weight,
                                  abbr=abbr, level=level, cft=cft,
                                  cfa=cfa, cmt=cmt, cma=cma)
        relation.save()


if __name__ == '__main__':
    build_model()
