import requests
from bs4 import BeautifulSoup


def cut(str):
    new = str[str.index("：") + 1:len(str)]
    return new


def getRating(courseID, teacherName):
    url = 'https://nces.cra.moe/search/?q=' + courseID
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    for div in soup.find_all('div', {'class': 'dashed'}):
        if (div.find_next('span', {'class': 'text-muted px12'}).text != '暂无评价') & (
                teacherName in div.find_next('a').text):
            web = 'https://nces.cra.moe' + div.find('a')['href']
            difficulty = div.find_next('li', {'class': 'right-mg-md'}).text
            workload = div.find_next('li', {'class': 'right-mg-md'}).find_next().text
            grading = div.find_next('li', {'class': 'right-mg-md'}).find_next().find_next().text
            gains = div.find_next('li', {'class': 'right-mg-md'}).find_next().find_next().find_next().text
            score = div.find('span', {'class': 'rl-pd-sm h4'}).text
            return {
                'url': web,
                'difficulty': cut(difficulty),
                'workload': cut(workload),
                'grading': cut(grading),
                'gains': cut(gains),
                'score': score
            }

