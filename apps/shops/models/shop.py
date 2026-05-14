from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self):
        ratings = self.ratings.all()

        if ratings.exists():
            avg = sum(r.rating for r in ratings) / ratings.count()
            self.average_rating = round(avg, 2)
        else:
            self.average_rating = 0

        self.save()
