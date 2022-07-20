from getCourses import *
from fuzzy_search import *
from selectClass import *
ipt = input('是否需要更新课程信息? (y/n)\n')
if ipt == 'y':
    getCourses()
ipt = input('是否需要更新选课列表? (y/n)\n')
if ipt == 'y':
    search()
ipt = input('是否开始选课? (y/n)\n')
if ipt == 'y':
    selectClass()
