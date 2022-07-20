# 与tis交互的代码来自于https://github.com/GhostFrankWu/SUSTech_Tools

import _thread
import json

import requests
from os import path
from re import findall
from json import loads
from colorama import init
from getpass import getpass

from html_parser import getTeacherAndTime

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}


def cas_login(user_name, pwd):
    """ 用于和南科大CAS认证交互，拿到tis的有效cookie
    输入用于CAS登录的用户名密码，输出tis需要的全部cookie内容(返回头Set-Cookie段的route和jsessionid)
    我的requests的session不吃CAS重定向给到的cookie，不知道是代码哪里的问题，所以就手动拿了 """
    print("[\x1b[0;36m!\x1b[0m] " + "测试CAS链接...")
    try:  # Login 服务的CAS链接有时候会变
        login_url = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas"
        req = requests.get(login_url, headers=head)
        assert (req.status_code == 200)
        print("[\x1b[0;32m+\x1b[0m] " + "成功连接到CAS...")
    except:
        print("[\x1b[0;31mx\x1b[0m] " + "不能访问CAS, 请检查您的网络连接状态")
        return "", ""
    print("[\x1b[0;36m!\x1b[0m] " + "登录中...")
    data = {  # execution大概是CAS中前端session id之类的东西
        'username': user_name,
        'password': pwd,
        'execution': str(req.text).split('''name="execution" value="''')[1].split('"')[0],
        '_eventId': 'submit',
    }
    req = requests.post(login_url, data=data, allow_redirects=False, headers=head)
    if "Location" in req.headers.keys():
        print("[\x1b[0;32m+\x1b[0m] " + "登录成功")
    else:
        print("[\x1b[0;31mx\x1b[0m] " + "用户名或密码错误，请检查")
        return "", ""
    req = requests.get(req.headers["Location"], allow_redirects=False, headers=head)
    route_ = findall('route=(.+?);', req.headers["Set-Cookie"])[0]
    jsessionid = findall('JSESSIONID=(.+?);', req.headers["Set-Cookie"])[0]
    return route_, jsessionid


def getinfo(semester_data):
    """ 用于向tis请求当前学期的课程ID，得到的ID将用于选课的请求
    输入当前学期的日期信息，返回的json包括了课程名和内部的ID """
    course_list = []
    alreadySelectedCoursesList = []
    coursesList = []
    course_types = {'bxxk': "通识必修选课", 'xxxk': "通识选修选课", "kzyxk": '培养方案内课程', "zynknjxk": '非培养方案内课程'}
    for course_type in course_types.keys():
        data = {
            "p_xn": semester_data['p_xn'],  # 当前学年
            "p_xq": semester_data['p_xq'],  # 当前学期
            "p_xnxq": semester_data['p_xnxq'],  # 当前学年学期
            "p_pylx": 1,
            "mxpylx": 1,
            "p_xkfsdm": course_type,
            "pageNum": 1,
            "pageSize": 1000  # 每学期总共开课在1000左右，所以单组件可以包括学期的全部课程
        }
        req = requests.post('https://tis.sustech.edu.cn/Xsxk/queryKxrw', data=data, headers=head)
        raw_class_data = loads(req.text)
        classData = {}
        with open("raw_data.json", "w") as outfile:
            json.dump(raw_class_data, outfile, indent=4)
        if len(alreadySelectedCoursesList)== 0:
            for i in raw_class_data['yxkcList']:
                cur_course = {}
                cur_course['courseID'] = i['kcdm']
                cur_course['courseName'] = i['kcmc']
                cur_course['credit'] = i['xf']
                teacherName, time = getTeacherAndTime(i['kcxx'])
                cur_course['teacherName'] = teacherName
                cur_course['time'] = time
                cur_course['className'] = i['rwmc']
                alreadySelectedCoursesList.append(cur_course)
        if 'kxrwList' in raw_class_data.keys():
            for i in raw_class_data['kxrwList']['list']:
                classData[i['rwmc']] = i['id']
                cur_course = {}
                cur_course['courseID'] = i['kcdm']
                cur_course['courseName'] = i['kcmc']
                cur_course['credit'] = i['xf']
                teacherName, time = getTeacherAndTime(i['kcxx'])
                cur_course['teacherName'] = teacherName
                cur_course['time'] = time
                cur_course['className'] = i['rwmc']
                coursesList.append(cur_course)
    with open("alreadySelectedCourses.json", "w") as outfile1:
        json.dump(alreadySelectedCoursesList, outfile1, indent=4, ensure_ascii=False)
    with open("courses.json", "w") as outfile2:
        json.dump(coursesList, outfile2, indent=4,  ensure_ascii=False)

def getCourses():
    init(autoreset=True)
    # 下面是CAS登录
    route, JSESSIONID = "", ""
    while route == "" or JSESSIONID == "":
        userName = input("请输入学号：")
        passWord = getpass("请输入CAS密码: ")
        route, JSESSIONID = cas_login(userName, passWord)
        if route == "" or JSESSIONID == "":
            print("[\x1b[0;33m-\x1b[0m] " + "请重试...")
    head['cookie'] = f'route={route}; JSESSIONID={JSESSIONID};'
    semester_info = loads(   # 这里要加mxpylx才能获取到选课所在最新学期
        requests.post('https://tis.sustech.edu.cn/Xsxk/queryXkdqXnxq', data={"mxpylx": 1}, headers=head).text)
    print("[\x1b[0;32m+\x1b[0m] " + f"当前学期是{semester_info['p_xn']}学年第{semester_info['p_xq']}学期，为"
                                    f"{['', '秋季', '春季', '小'][int(semester_info['p_xq'])]}学期")
    # 下面获取课程信息
    print("[\x1b[0;36m!\x1b[0m] " + "从服务器下载课程信息，请稍等...")
    postList = getinfo(semester_info)
    print("[\x1b[0;32m+\x1b[0m] " + "课程信息下载完成")
    return