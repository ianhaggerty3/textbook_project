import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.math.purdue.edu/academic/courses")
text = page.text
text = BeautifulSoup(text, 'html.parser')
columns = text.find_all('td')
course_nums = []

for x in range(0, len(columns) - 1, 2):
    temp = str(columns[x]).split()
    course_nums.append(temp[5])

fid = open('MA_info.txt', 'w')

courseinfo = {'subject': 'MA'}
book_names = {}
book_urls = {}

for x in course_nums:
    textfields = []
    textbooks = []
    urls = []
    start = 0
    stop = 50
    courseinfo['course'] = x
    page = requests.get("https://www.math.purdue.edu/academic/courses/coursepage", params=courseinfo)
    text = page.text
    text = BeautifulSoup(text, 'html.parser')
    columns = text.find_all('td')
    for y in range(len(columns)):
        if columns[y].get_text().find(' Textbook ') != -1:
            textfields.append(y + 1)
        #if columns[y].get_text().find(' Other ') != -1:
        #    textfields.append(y + 1)
    for y in textfields:
        textbooks.append(columns[y].get_text()[1:])
        try:
            urls.append(columns[y].contents[1].attrs['href'])
        except KeyError:
            print('error with url for course MA ', x)
    if len(textbooks) > 0:
        book_names[x] = textbooks
        book_urls[x] = urls
        fid.write('\nCourse Number: {:s}\n'.format(x))
        for i in range(len(textbooks)):
            fid.write('{:s}\n{:s}\n'.format(textbooks[i], urls[i]))
    else:
        fid.write('\nMA {:s} does not need a textbook\n'.format(x))

fid.close()
