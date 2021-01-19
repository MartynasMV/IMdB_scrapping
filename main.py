import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"Accept-language": "en_US, en; q=0.5"}

url = 'https://www.imdb.com/search/title/?groups=top_1000'
requests = requests.get(url, headers=headers)
html = requests.text
soup = BeautifulSoup(html, 'html.parser')

#print(soup.prettify())
titles = []
years = []
runtime = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', {"class": "lister-item mode-advanced"} )

for container in movie_div:
    #titles
    name = container.h3.a.text
    titles.append(name)
    #year
    year = container.h3.find('span', class_="lister-item-year text-muted unbold").text
    years.append(year)
    #runtime
    time = container.p.find('span', class_="runtime").text if container.p.find('span', class_='runtime') else '-'
    runtime.append(time)
    #imdbrating
    imdb = float(container.find('strong').text)
    imdb_ratings.append(imdb)
    #metascore rating
    metascore_raw = int(container.find('span', class_='metascore').text.strip()) if container.find('span', class_='metascore') else '-'
    metascores.append(metascore_raw)
    #votes and gross
    votes_and_gross = container.find_all('span', attrs={'name': 'nv'})
    #votes
    votes_raw = votes_and_gross[0].text
    votes.append(votes_raw)
    #gross
    gross_raw = votes_and_gross[1].text if len(votes_and_gross) > 1 else "-"
    us_gross.append(gross_raw)

movies = pd.DataFrame({
    'Movie': titles,
    'Year': years,
    'Lenght': runtime,
    'IMdB rating': imdb_ratings,
    'Metascore': metascores,
    'Votes': votes,
    'Gross(US)': us_gross,
})

#cleaning:
movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['Lenght'] = movies['Lenght'].str.extract('(\d+)').astype(int)
movies['Votes'] = movies['Votes'].str.replace(',','').astype(int)
movies['Gross(US)'] = movies['Gross(US)'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['Gross(US)'] = pd.to_numeric(movies['Gross(US)'], errors='coerce')

print(movies)
#movies.to_csv('movies.csv')