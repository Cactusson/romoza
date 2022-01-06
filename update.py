import django
import os
import requests

from bs4 import BeautifulSoup
from datetime import date


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'romoza.settings')
django.setup()


from movies.models import Movie


DIARIES = {
    'I': 'https://letterboxd.com/cactusson/films/diary/',
    'O': 'https://letterboxd.com/krabby01/films/diary/'
}

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def collect_movies_from_diary(ids, url):
    movies = []

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

    return movies


if __name__ == '__main__':
    i_watchlist = Movie.objects.filter(i_watchlist=True).filter(i_watched_date=None)
    ids = [movie.num for movie in i_watchlist]
    watched = collect_movies_from_diary(ids, DIARIES['I'])

    for film in watched:
        movie = Movie.objects.get(num=film['id'])
        movie.i_watched_date = film['date']
        movie.save()

    o_watchlist = Movie.objects.filter(o_watchlist=True).filter(o_watched_date=None)
    ids = [movie.num for movie in o_watchlist]
    watched = collect_movies_from_diary(ids, DIARIES['O'])

    for film in watched:
        movie = Movie.objects.get(num=film['id'])
        movie.o_watched_date = film['date']
        movie.save()
