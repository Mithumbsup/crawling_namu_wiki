from bs4 import BeautifulSoup
import requests
import urllib.request as req
import urllib.parse as rep
import os,errno
import csv 
import pandas as pd 


def makeUrl(base_url,target):
    quote = rep.quote_plus(target) # url encode -> 16진수로 인코딩
    # url은 ASCII 코드값만 사용됨, 따라서 한글이 포함될경우 인코딩을 통해 ASCII 코드로 변환함     >> urllib.request.urlopen를 위한 인코딩 
    url = base_url + quote
    print(url)
    resp = requests.get(url)  # GET/POST 여부에 상관없이 매개변수를 인코딩 할 필요가 없으며, json으로 디코딩하기에 편리함.
    return resp


def makeDirs(savePath, nameList):
    makeDirs = []
    # savePath 의 참주소를 검정하는 코드가 필요할듯 ㅜ
    for name in nameList:
        path = savePath  + '\\' + str(name) + '\\'
        try:
            if not(os.path.isdir(path)):
                os.makedirs(os.path.join(path))
                makeDirs.append(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!!!!")
                raise
    return makeDirs


def csvToDf(filePath):
    df = pd.read_csv(filePath)
    columns = df.columns # columns는 list 타입 - 추출해낼 데이터 컬럼 조회 
    # print(columns) 
    # print(type(df['질병 '])) #
    diseaseList = df['CROPNAME'] # series type 
    
    mainthemeList = []
    for maintheme in diseaseList:  # 원할한 검색을 위해 series안에 공백 제거를 함
        maintheme = maintheme.strip()
        mainthemeList.append(maintheme)
    print(mainthemeList)    # type = List  
    return mainthemeList


def extract_searchList(mainthemeList):
    base = "https://namu.wiki/w/"

    for maintheme in mainthemeList :
        res1 = makeUrl(base,maintheme)
        soup = BeautifulSoup(res1.text,"html.parser")

        searchList = soup.find_all('div',{'class':'wiki-paragraph'})
        print(searchList)
        result_title =[]

        for title in searchList:
            # print(title)
            title = title.get_text()
            result_title.append(title)
            # print(len(title))
            # print(result_title)

    return result_title


def extract(result_title):
    base = "https://namu.wiki/w/"
    
    maintheme = '두통'

    for theme in result_title:
        print(theme)
        res = makeUrl(base,theme)
        soup = BeautifulSoup(res.text,"html.parser")
        print(soup)
        txt_savePath = 'C:\\Pythonsource\\Workspace\\Crawling\\Project\\'+ str(maintheme) + '\\' + str(theme) + '\\txt'
        f = open(txt_savePath + '\\' + str(theme) + '.csv', 'a', encoding='utf-8')

        num_stage = len(soup.find_all('div', {"class": "section steps sticky"})) + 1    # 단계의 갯수.
        ol_li_list = []       # 텍스트 크롤링을 위한 Selector의 첫번째 부분을 저장한 리스트.


        for a in range(1, num_stage + 1):
            t = "div#단계_" + str(a) + " > ol > li"
            ol_li = soup.select(t)            # 각 ol 안에 들어있는 list 태그의 갯수.
            print(len(ol_li))
            ol_li_list.append(len(ol_li))   # 리스트에 저장.

        first_list = []    # 텍스트 크롤링을 위한 Selector의 첫번째 부분을 저장한 리스트.

        for a in range(1, num_stage + 1):
            first = "div#단계_" + str(a) + " > ol > li#step-id-" + str(a-1)   # 텍스트 크롤링을 위한 Selector의 첫번째 부분.
            first_list.append(first)                                         # 리스트에 저장.

        num_contents = 0    # 텍스트를 크롤링할 게시물의 갯수.

        url_list = []       # 텍스트 크롤링을 위한 최종 Selector를 저장한 리스트.

        for n in range(0,num_stage):
            num_li = ol_li_list[n]              # 리스트에 저장되어 있는 각 ol 안의 list 태그 갯수를 하나씩 불러오기.
            first_selector = first_list[n]      # 리스트에 저장되어 있는 Selector의 첫번째 부분을 하나씩 불러오기.

            for e in range(0,num_li):
                final_url = first_selector + str(num_contents)      # 텍스트 크롤링을 위한 최종 Selector.
                num_contents += 1
                url_list.append(final_url)                          # 리스트에 저장.

        index = 0                               # 크롤링한 텍스트의 순서를 표시할 인덱스.

        for f_url in url_list:
            text = soup.select(f_url + " > div.step > b.whb")[0].getText()      # 최종 크롤링 과정.
            f.write(str(index+1))
            f.write('.' + ' ')
            f.write(text)
            f.write('\n')
            index += 1
        f.close()
        print('텍스트 크롤링 완료')       

        break

    return text 




filePath = "C:\\Users\\mis\\Desktop\\crawling\\csv\\cropName.csv"
diseaseList = csvToDf(filePath)
extract_searchList(diseaseList)

# # result_title = extract_searchList()
# # text = extract(result_title)

# target = "몬스테라"
# base_url = "https://namu.wiki/w/"

# print(base_url)
# makeUrl(base_url,target)


# def makeUrl(base_url,target):
#     quote = rep.quote_plus(target) # url encode -> 16진수로 인코딩
#     # url은 ASCII 코드값만 사용됨, 따라서 한글이 포함될경우 인코딩을 통해 ASCII 코드로 변환함
#     url = base_url + quote
#     print(url)
#     res = req.urlopen(url)
#     return res