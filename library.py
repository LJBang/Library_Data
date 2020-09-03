import csv
import requests
import xmltodict
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

for j in range(2009,2021):
    f=open('./dataset/Best'+str(j)+'.csv','r',encoding='cp949') #파일 주소
    data=csv.reader(f)
    header=next(data)
    cnt=0
    authk = ''
    url='http://data4library.kr/api/keywordList?authKey='+authk+'&isbn13='
    result='result/' #결과 저장할 폴더
    k=0
    keyword_list=""

    for row in data:
        if k>99:
            break
        new_url=url+row[6]
    #    new_file_name=re.sub('[:-?%*|"<>./]','',row[1]) #엑셀 제목에 못 쓰는 특수문자 제거
    #    new_file_name=result+new_file_name.strip()+'.csv' #공백 제거
    #    print(new_file_name)
        req=requests.get(new_url).content
        xmlObject=xmltodict.parse(req)
        keyword=xmlObject['response']['items']
        if keyword: #키워드가 있는 경우
            keyword=xmlObject['response']['items']['item']
            for i in range(len(keyword)):
                if keyword[i]['weight']!='1':
                    keyword_list=keyword_list+' '+keyword[i]['word']
        else: #키워드가 없는 경우
            print(row[1]+'has no keyword')
        k = k + 1

    wc = WordCloud(font_path='fonts/GmarketSansTTFBold.ttf', background_color='white').generate(keyword_list)
    plt.figure(figsize=(22,22)) #이미지 사이즈 지정
    plt.imshow(wc, interpolation='lanczos') #이미지의 부드럽기 정도
    plt.axis('off') #x y 축 숫자 제거
    plt.savefig('./images/'+str(j)+'.png')
#    plt.show()

    f.close