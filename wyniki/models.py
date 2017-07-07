from django.db import models

class WynikZPost(models.Model):
    w1 = models.FloatField(default=0)
    w2 = models.FloatField(default=0)
    w3 = models.FloatField(default=0)
    w4 = models.FloatField(default=0)
    w5 = models.FloatField(default=0)
    w6 = models.FloatField(default=0)
    w7 = models.FloatField(default=0)
    w8 = models.FloatField(default=0)
    w9 = models.FloatField(default=0)
    w10 = models.FloatField(default=0)
    w11 = models.FloatField(default=0)
    w12 = models.FloatField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return "WynikZPost"


class Wynik(models.Model):
    wojewodztwo = models.CharField(max_length=100)
    okreg = models.CharField(max_length=100)
    powiat = models.CharField(max_length=100)
    gmina = models.CharField(max_length=100)
    w1 = models.FloatField(default=0)
    w2 = models.FloatField(default=0)
    w3 = models.FloatField(default=0)
    w4 = models.FloatField(default=0)
    w5 = models.FloatField(default=0)
    w6 = models.FloatField(default=0)
    w7 = models.FloatField(default=0)
    w8 = models.FloatField(default=0)
    w9 = models.FloatField(default=0)
    w10 = models.FloatField(default=0)
    w11 = models.FloatField(default=0)
    w12 = models.FloatField(default=0)
    uprawnionych = models.IntegerField(default=0)
    wydanych_kart = models.IntegerField(default=0)
    wyjetych_kart = models.IntegerField(default=0)
    niewaznych_glosow = models.IntegerField(default=0)
    waznych_glosow = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.wojewodztwo + "/" + self.okreg + "/" + self.powiat + "/" + self.gmina


class Kandydat(models.Model):
    numerKandydata = models.CharField(max_length=100) # w1, w2, itd.
    imieINazwisko = models.CharField(max_length=100)

    def publish(self):
        self.save()

    def __str__(self):
        return self.imieINazwisko

# Create your models here.

# from wyniki.models import Kandydat
# Kandydat.objects.all()