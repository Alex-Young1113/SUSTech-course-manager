from fuzzywuzzy import fuzz
from operator import itemgetter
import json

from numpy import mat
def search():
    wishlist = []
    with open('courses.json') as f:
        Courses = json.load(f)
        print("（输入空字符串以退出）")
        while True:
            cur_course = input("请输入课程名称：")
            if len(cur_course) == 0:
                break
            matched = False
            for course in Courses:
                if course['courseName'] == cur_course:
                    wishlist.append((course['courseID'], course['courseName']))
                    print("成功添加课程：{} {}".format(course['courseID'], course['courseName']))
                    matched = True
                    break
            if not matched: # didn't find the course, try fuzzy search
                candidates = []
                for course in Courses:
                    score = fuzz.WRatio(course['courseName'], cur_course, force_ascii=False) 
                    if score >= 80 and (course['courseID'], course['courseName'], score) not in candidates:
                        candidates.append((course['courseID'], course['courseName'], score)) 
                # no result   
                if len(candidates) == 0:
                    print("未找到课程，请重新输入")
                    continue
                candidates.sort(key=itemgetter(2), reverse=True)
                i = 1
                for course in candidates:
                    print("{:2d} | {:2d} | {:>10s} | {:>20s}".format(i, course[2], course[0], course[1]))
                    i += 1
                choice = input("请输入选课序号（输入0放弃）：")
                if choice == '0' or not choice.isnumeric:
                    continue
                choice = int(choice)
                if choice < 1 or choice > len(candidates):
                    print("输入有误，请重新输入")
                    continue
                wishlist.append((candidates[choice-1][0], candidates[choice-1][1]))
                print("成功添加课程：{} {}".format(candidates[choice-1][0], candidates[choice-1][1]))
        print("您的选课列表为：")
        i = 1
        for course in wishlist:
                print("{:2d} | {:>10s} | {:>20s}".format(i, course[0], course[1]))
                i += 1
        print("请确认您的选课列表，输入y确认，输入其他字符放弃")
        choice = input("请输入：")
        if choice != 'y':
            print("放弃选课")
            exit(0)
        print("开始选课")
        with open('wishlist.json', 'w') as f:
            fs = ['courseID', 'courseName']
            us = []
            for course in wishlist:
                us.append(dict(zip(fs,course)))
            json.dump(us, f)
            print("选课成功")


