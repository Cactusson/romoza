from django.shortcuts import render


from .models import Movie


def index(request):
    i_watchlist = Movie.objects.filter(i_watchlist=True)
    i_watched = i_watchlist.exclude(i_watched_date=None).order_by('-i_watched_date')

    o_watchlist = Movie.objects.filter(o_watchlist=True)
    o_watched = o_watchlist.exclude(o_watched_date=None).order_by('-o_watched_date')

    context = {
        'i_watchlist': i_watchlist.count(),
        'i_watched': i_watched,

        'o_watchlist': o_watchlist.count(),
        'o_watched': o_watched,
    }

    return render(request, 'movies/index.html', context)
