import csv
import requests
import xmltodict
import re

f=open('C:/Users/user/Desktop/데이터 분석/library/Best2019.csv','r',encoding='cp949') #파일 주소
data=csv.reader(f)
header=next(data)
cnt=0
url='http://data4library.kr/api/keywordList?authKey=35c3bfc58502e41b21e1c4ac301a8056cbf1902fccd78698b85a20c2bbbb3fdb&isbn13='
result='result/' #결과 저장할 폴더
for row in data:
    new_url=url+row[6]
    new_file_name=re.sub('[:-?%*|"<>./]','',row[1]) #엑셀 제목에 못 쓰는 특수문자 제거
    new_file_name=result+new_file_name.strip()+'.csv' #공백 제거
    #print(new_file_name)
    req=requests.get(new_url).content
    xmlObject=xmltodict.parse(req)
    keyword=xmlObject['response']['items']
    if keyword: #키워드가 있는 경우
        nf=open(new_file_name,'w',newline='')
        write=csv.DictWriter(nf,fieldnames=['키워드','빈도수'])
        write.writeheader()
        keyword=xmlObject['response']['items']['item']
        for i in range(len(keyword)):
            write.writerow({'키워드':keyword[i]['word'],'빈도수':keyword[i]['weight']})
    else: #키워드가 없는 경우
        print(row[1]+'has no keyword')
    nf.close
f.close
