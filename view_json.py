import json

i = input("按0显示已经选择的课程，按1选择可以选择的课程, 2显示wish list, 3显示selectedClass: \n")
if i == '0':
    with open('alreadySelectedCourses.json') as f:
        courses = json.load(f)
        print(json.dumps(courses, indent=4, ensure_ascii=False))
elif i == '1':
    with open('courses.json') as f:
        courses = json.load(f)
        print(json.dumps(courses, indent=4, ensure_ascii=False))
elif i == '2':
    with open('wishList.json') as f:
        courses = json.load(f)
        print(json.dumps(courses, indent=4, ensure_ascii=False))
elif i == '3':
    with open('selectedClass.json') as f:
        courses = json.load(f)
        print(json.dumps(courses, indent=4, ensure_ascii=False))