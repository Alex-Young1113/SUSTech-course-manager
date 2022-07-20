def getTeacherAndTime(text):
    import requests
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    teacherName = []
    for i in soup.findAll('a', {'href': 'javascript:void(0);'}):
        if i.text != ' ' and ',' not in i.text and ':' not in i.text:
            teacherName.append(i.text.strip())
    time = []
    for i in soup.findAll('p'):
        if ',' in i.text and ':' not in i.text:
            time.append(i.text.strip())
    return teacherName, time