from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=500)
    year = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(default=0)
    i_watchlist = models.BooleanField(default=False)
    i_watched_date = models.DateField(null=True)
    o_watchlist = models.BooleanField(default=False)
    o_watched_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.title} ({self.year})'
