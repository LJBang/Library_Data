import requests
import xmltodict
import re

url='http://data4library.kr/api/loanItemSrch?authKey=35c3bfc58502e41b21e1c4ac301a8056cbf1902fccd78698b85a20c2bbbb3fdb&'
#결과 저장할 폴더
startDt=['2020','-','02','-','01'] #시작날짜
endDt=['2020','-','02','-','07'] #종료날짜
total_cnt=0 #대출수
idx=1 #주 확인용 인덱스
result=[] #결과 값 저장
x=['03','05','07','08']
y=['04','06']

while True:
    str_startDt="".join(startDt)
    str_endDt="".join(endDt)
    new_url=url+'startDt='+str_startDt+'&endDt='+str_endDt

    print(str_startDt,str_endDt) #시작날,종료날 확인
    req=requests.get(new_url).content
    xmlObject=xmltodict.parse(req)
    data=xmlObject['response']['docs']['doc']
    
    for i in range(len(data)):
        loan_cnt=data[i]['loan_count'].replace(',','') #int로 바꾸기 위해 , 제거
        total_cnt+=int(loan_cnt)
    #print(total_cnt) 1주일 동안 대출된 도서 수

    if (startDt[2]=='02') and (idx == 5): #2월 29일
        temp=result[3][1] #2월 넷째주 대출수
        total_cnt+=temp
        result[3]=[startDt[2]+'-'+str(idx-1),total_cnt] #2월 넷째주에 합치기
        #print(result)
        
    else:
        result.append([startDt[2]+'-'+str(idx),total_cnt])
        #print(result)
    
    total_cnt=0 #대출수 초기화

    if str_endDt == '2020-08-31': #전체 프로그램 종료조건
        break

    if idx == 4: #2월과 2월이 아닌 달 구분
        if startDt[2] == '02': #2월
            year=int(startDt[0])
            if ((year%4==0)and(year%100!=0))or(year%400==0): #윤년이면 29일까지 있음
                idx+=1
                startDt[4]='29'
                endDt[4]='29'
            else: #윤년이 아닌 연도는 28일까지 있으므로 3월로 넘김 
                idx=1
                startDt[2]='03'
                startDt[4]='01'
                endDt[2]='03'
                endDt[4]='07'
        else: #2월이 아닌 달 중 마지막 날이 30일인 날과 31일인 날 구분
            idx+=1
            startDt[4]='29'
            if startDt[2] in x:
                endDt[4]='31'
            if startDt[2] in y:
                endDt[4]='30'
    
    elif idx == 5: #다음달로 월 변경
        idx=1
        startDt[2]='0'+str(int(startDt[2])+1)
        startDt[4]='01'
        endDt[2]=startDt[2]
        endDt[4]='07'

    else: # 일 변경
        startDt[4]=str(int(startDt[4])+7)
        endDt[4]=str(int(endDt[4])+7)
        if idx == 1: #계산을 위해 int로 변환하면서 앞에 0이 없어졌기 때문에 다시 붙여준다
            startDt[4]='0'+startDt[4] #시작 일이 8일일 때 
        idx+=1

print(result)