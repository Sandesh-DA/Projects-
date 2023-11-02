import requests
from bs4 import BeautifulSoup
import csv

csv_file = open('IMDb_TopMovies.csv', 'w',encoding="utf-8")

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Rank','Movie Name','Rating','Released','Duration'])

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

try:
   source = requests.get('https://www.imdb.com/chart/top/',headers=headers)
   source.raise_for_status()
   soup = BeautifulSoup(source.text)
   movies_rating =  soup.find('ul',class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 ckQYbL compact-list-view ipc-metadata-list--base')
   for movies in movies_rating.find_all('li'):
       
       title = movies.find('div',class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-c7e5f54-9 irGIRq cli-title")
       movie_name = title.a.h3.text.split('.')
       rank = title.a.h3.text.split('.')[0]
       
       ratingg =  movies.find('span',class_="sc-c7e5f54-1 lhsppJ")
       rating = ratingg.find('span',class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text[:3]


       i = movies.find('div',class_="sc-c7e5f54-7 brlapf cli-title-metadata").find_all('span')
       year = i[0].text
       duration = i[1].text
       
       print(rank,movie_name,rating,year,duration)

       csv_writer.writerow([rank,movie_name,rating,year,duration])
       
       
except Exception as e:
   print(e)

csv_file.close()