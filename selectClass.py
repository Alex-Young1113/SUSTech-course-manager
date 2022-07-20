import json
import random
from evaluation import *

def timeStringToTuple(timeString):
    a = timeString.index("星") + 2
    b = timeString.index("节") - 1
    if timeString[a] == '一':
        dayOfWeek = 1
    elif timeString[a] == '二':
        dayOfWeek = 2
    elif timeString[a] == '三':
        dayOfWeek = 3
    elif timeString[a] == '四':
        dayOfWeek = 4
    elif timeString[a] == '五':
        dayOfWeek = 5
    elif timeString[a] == '六':
        dayOfWeek = 6
    elif timeString[a] == '日':
        dayOfWeek = 7
    else:
        print("时间格式错误！")
    
    return (dayOfWeek, int(timeString[b]) // 2)

def selectClass() :
    f = open('wishlist.json')

    courseList = []
    data = json.load(f)

    for i in data:
        courseList.append(i.get('courseID'))

    f.close()

    print("您要选的课程ID为：")
    print(courseList)
    print('\n')

    dict = {} # stores the mapping from courseID to all its classes

    f2 = open('courses.json')
    Courses = json.load(f2)

    for i in courseList:
        dict[i] = []

    for course in Courses:
        if course['courseID'] in courseList:
            dict[course['courseID']].append((course['className'],{timeStringToTuple(x) for x in course['time']}))

    print('各个课程ID及其对应的班级为：')
    print(dict)
    print('\n')

    # now began the process of choosing the class for each course

    constraint = [0, ] * len(courseList) # i-th course has constraint[i] classes
    for i in range(len(courseList)):
        constraint[i] = len(dict[courseList[i]])

    bestChoice = []
    maxNum = 0
    # choose class randomly for each course, repeat 100000 times to get the best choice
    # I do not know how to fully iterate through all the possibilities, if you know, please tell me
    for j in range(100000): 
        choice = [0, ] * len(constraint)
        n = 0
        for i in range(len(constraint)):
            choice[i] = random.randint(0, constraint[i])
            if choice[i] != 0:
                n += 1
        time = []
        valid = True
        for i in range(len(choice)):
            if choice[i] != 0: # choice = 0 -> does not select this course
                for t in dict[courseList[i]][choice[i] - 1][1]:
                    if t in time:
                        valid = False
                        break
                    else:
                        time.append(t)
        if valid and n > maxNum:
            bestChoice = choice
            maxNum = n

    selectedClass = [] # className for all selected classes
    for i in range(len(bestChoice)):
        selectedClass.append(dict[courseList[i]][bestChoice[i] - 1][0])

    print("您选的班级为：")
    print(selectedClass)
    print('\n')

    f3 = open('selectedClass.json', 'w')

    finalList = []
    meo = []
    for course in Courses:
        if course['className'] in selectedClass:
            cur_course = {}
            meo.append(course['className'])
            cur_course['courseName'] = course['courseName']
            cur_course['courseID'] = course['courseID']
            cur_course['className'] = course['className']
            cur_course['time'] = course['time']
            cur_course['teacherName'] = course['teacherName']
            cur_course['credit'] = course['credit']
            cur_course['rating'] = getRating(cur_course.get('courseID'), cur_course.get('teacherName')[0])
            finalList.append(cur_course)
    json.dump(finalList, f3, indent = 4, ensure_ascii=False)

    ipt = input('是否需要生成喵课脚本所需的Class.txt文件？(y/n)\n')
    if ipt == 'y':
        f4 = open('Class.txt', 'w')
        f4.write('\n')
        for i in meo:
            f4.write(i + '\n')
        f4.close()
    f3.close()
    f2.close()
    f.close()



