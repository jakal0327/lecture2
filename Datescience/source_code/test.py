from bs4 import BeautifulSoup # 크롤링하는 패키지
import pandas as pd # 데이터 분석 패키지
# 웹 url로 요청/응답 처리 패키지
import urllib
from urllib.request import urlopen
# tqdm
from tqdm import tqdm

date = pd.date_range('2019-12-01', periods=3, freq='w-tue') # w-tue : week + tuesday
time = [i for i in range(7, 24, 5)]

chart_date = []
chart_time = []
chart_ranking = []
chart_title = []
chart_artist = []
chart_album = []

for today in tqdm(date):
    for t in tqdm(time):
        url1 = "https://music.bugs.co.kr/chart/track/realtime/total?"
        url2 = "chartdate={date}&charthour={time}"
        url = url1+url2
        
        parsed_date = urllib.parse.quote(today.strftime('%Y%m%d'))
        html = url.format(date=parsed_date, time= "%02d" % t )
        response = urlopen(html)
        soup = BeautifulSoup(response, 'html.parser')
        
        for i in range(3): # 3위까지
            chart_date.append(today)
            chart_time.append(t)
            chart_ranking.append( soup.find_all('div', 'ranking')[i].strong.string )
            chart_title.append( soup.find_all('p', 'title')[i].a.string )
            chart_artist.append( soup.find_all('p', 'artist')[i].a.string )
            chart_album.append( soup.find_all('a', 'album')[i+1].string )

chart = pd.DataFrame({ 'date': chart_date,
                     'time': chart_time,
                     'ranking': chart_ranking,
                     'title': chart_title,
                     'artist': chart_artist,
                     'album': chart_album})

chart_grouped = chart.groupby(['title', 
                               'artist']).size().reset_index(name='count')
chart_grouped = chart_grouped.set_index(['title', 'artist'])
chart_grouped.sort_values(by='count', ascending=False)

print(chart_grouped)