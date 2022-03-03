import requests
import datetime
import sys
def main(dnum):
    ystday=(datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')#yesterday
    date=(datetime.date.today()-datetime.timedelta(days=int(dnum))).strftime('%Y-%m-%d')#number of days
    url_api='api'
    headers={'Key':'xxxxxxxxxxxxxxxxxxxxxxxxx'}


    def condata(account):
        body={'account':account,'from':date,'to':ystday}
        response=requests.post(url_api,data=body,headers=headers)#POST，Content-Type：application/x-www-form-urlencoded;charset=utf-8
        all_con=account+'\n'
        for i in range(len(response.json()['data'])-1,-1,-1):
            con=str(response.json()['data'][i]['articleLikesCount'])+'\t'+\
                str(response.json()['data'][i]['rankPosition'])+'\t'+\
                str(response.json()['data'][i]['articleClicksCountTopLine'])+'\t'+\
                response.json()['data'][i]['rankDate'][0:10]+'\n'
            all_con=all_con+con
        return all_con

    f=open(r'D:\tempfiles\test.txt','w')
    f.write(condata('')+condata(''))
    f.close()



if __name__=='__main__':
    try:
        main(sys.argv[1])
    except:
        main(1)#Just 1 day
