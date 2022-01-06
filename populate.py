import requests

from bs4 import BeautifulSoup
from datetime import date

from movies.models import Movie


MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def collect_movies_from_lists(urls):
    movies = []

    for url in urls:
        while True:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            movies_on_page = soup.find(class_='poster-list')

            for movie in movies_on_page.findAll('li'):
                title = movie.find('a').text
                year = int(movie.find('small').text)
                id_num = int(movie.find('div')['data-film-id'])
                movies.append({'title': title, 'year': year, 'id': id_num})

            link = soup.find(class_='next')
            if link is None:
                break

            try:
                url = 'https://letterboxd.com' + link['href']
            except KeyError:
                break

    return movies


def collect_movies_from_diary(to_watch, url):
    movies = []
    ids = [movie['id'] for movie in to_watch]

    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        movies_on_page = soup.find(class_='film-table').find('tbody')
        current_year = None
        current_month = None

        for movie in movies_on_page.findAll('tr'):
            calendar, day, title = movie.findAll('td')[:3]

            calendar = calendar.find('div')
            if calendar:
                current_month, current_year = [
                    link.text for link in calendar.findAll('a')]
                current_month = MONTHS.index(current_month) + 1
                current_year = int(current_year)
            day = int(day.find('a').text)
            d = date(current_year, current_month, day)

            id_num = int(title.find('div')['data-film-id'])

            if id_num in ids:
                movies.append({'date': d, 'id': id_num})

        link = soup.find(class_='next')
        if link is None:
            break

        try:
            url = 'https://letterboxd.com' + link['href']
        except KeyError:
            break

    return movies


LISTS = {
    'I': [
        'https://letterboxd.com/cactusson/list/whatever/detail/',
        'https://letterboxd.com/cactusson/list/whatever-2/detail/',
        'https://letterboxd.com/cactusson/list/whatever-3/detail/',
        'https://letterboxd.com/cactusson/list/whatever-4/detail/',
        'https://letterboxd.com/cactusson/list/whatever-5/detail/',
        'https://letterboxd.com/cactusson/list/criterion-challenge-2021/detail/',
        'https://letterboxd.com/cactusson/list/criterion-challenge-2022/detail/',
        'https://letterboxd.com/cactusson/list/snowflake-challenge/detail/',
    ],

    'O': [
        'https://letterboxd.com/krabby01/list/the-150/detail/',
        'https://letterboxd.com/krabby01/list/2021/detail/',
        'https://letterboxd.com/krabby01/list/the-criterion-challunenge-2022/detail/',
    ]
}

DIARIES = {
    'I': 'https://letterboxd.com/cactusson/films/diary/page/2/',
    'O': 'https://letterboxd.com/krabby01/films/diary/page/2/'
}


to_watch = collect_movies_from_lists(LISTS['I'])
watched = collect_movies_from_diary(to_watch, DIARIES['I'])


for film in to_watch:
    print(film)
    movie = Movie.objects.get_or_create(title=film['title'], num=film['id'])[0]
    movie.year = film['year']
    movie.i_watchlist = True
    movie.save()

for film in watched:
    print(film)
    movie = Movie.objects.get(num=film['id'])
    movie.i_watched_date = film['date']
    movie.save()


to_watch = collect_movies_from_lists(LISTS['O'])
watched = collect_movies_from_diary(to_watch, DIARIES['O'])

for film in to_watch:
    print(film)
    movie = Movie.objects.get_or_create(title=film['title'], num=film['id'])[0]
    movie.year = film['year']
    movie.o_watchlist = True
    movie.save()

for film in watched:
    print(film)
    movie = Movie.objects.get(num=film['id'])
    movie.o_watched_date = film['date']
    movie.save()
