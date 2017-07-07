import csv, sys, os
import numpy as np

os.environ['DJANGO_SETTINGS_MODULE'] = 'wybory.settings'

import django

django.setup()

from wyniki.models import Wynik, Kandydat, WynikZPost
from django.contrib.auth.models import User

# Otwieram plik z danymi
file = open('static/data/pkw2000.csv')
my_reader = csv.reader(file)
plikDoPrzerobienia = list(my_reader)
plik = np.array(plikDoPrzerobienia)


# print("model 1:")
# print("Wojewodztwo : " + plik[1][0])
# print("Nr okregu   : " + plik[1][1])
# print("Powiat      : " + plik[1][4])
# print("Gmina       : " + plik[1][3])
#
# print("model ostatni:")
# print("Wojewodztwo : " + plik[2494][0])
# print("Nr okregu   : " + plik[2494][1])
# print("Powiat      : " + plik[2494][4])
# print("Gmina       : " + plik[2494][3])
nowy = WynikZPost()
nowy.w1 = nowy.w2 = nowy.w3 = nowy.w4 = nowy.w5 = nowy.w6 = nowy.w7 = nowy.w8 = nowy.w9 = nowy.w10 = nowy.w11 = nowy.w12 = 0
nowy.save()

def dodaj_kandydatow_do_bazy_danych():
    for x in range(12):
        print("Wstawiam pod indeksem " + str(x + 1) + " osobę : " + plik[0][11 + x])
        nowy = Kandydat()
        nowy.numerKandydata = "w" + str(x + 1)
        nowy.imieINazwisko = plik[0][11 + x]
        nowy.save()


def dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart, wyjetych_kart, niewaznych_glosow, waznych_glosow):
    dana = Wynik()
    dana.wojewodztwo = wojewodztwo
    dana.okreg = okreg
    dana.powiat = powiat
    dana.gmina = gmina
    dana.w1 = float(wyniki_kandydatow[0])
    dana.w2 = float(wyniki_kandydatow[1])
    dana.w3 = float(wyniki_kandydatow[2])
    dana.w4 = float(wyniki_kandydatow[3])
    dana.w5 = float(wyniki_kandydatow[4])
    dana.w6 = float(wyniki_kandydatow[5])
    dana.w7 = float(wyniki_kandydatow[6])
    dana.w8 = float(wyniki_kandydatow[7])
    dana.w9 = float(wyniki_kandydatow[8])
    dana.w10 = float(wyniki_kandydatow[9])
    dana.w11 = float(wyniki_kandydatow[10])
    dana.w12 = float(wyniki_kandydatow[11])
    dana.uprawnionych = uprawnionych
    dana.wydanych_kart = wydanych_kart
    dana.wyjetych_kart = wyjetych_kart
    dana.niewaznych_glosow = niewaznych_glosow
    dana.waznych_glosow = waznych_glosow
    dana.save()


def dodaj_statystyki_Polski():
    uprawnionych = 0
    wydanych_kart = 0
    wyjetych_kart = 0
    niewaznych_glosow = 0
    waznych_glosow = 0

    wojewodztwo = ""
    okreg = ""
    powiat = ""
    gmina = ""

    wyniki_kandydatow = [0 for i in range(12)]
    for y in range(1, 2495):
        for x in range(12):
            wyniki_kandydatow[x] += int(plik[y][11 + x])
        uprawnionych += int(plik[y][6])
        wydanych_kart += int(plik[y][7])
        wyjetych_kart += int(plik[y][8])
        niewaznych_glosow += int(plik[y][9])
        waznych_glosow += int(plik[y][10])

    dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart, wyjetych_kart,
                  niewaznych_glosow, waznych_glosow)



def dodaj_statystyki_wojewodztw():
    uprawnionych = 0
    wydanych_kart = 0
    wyjetych_kart = 0
    niewaznych_glosow = 0
    waznych_glosow = 0

    wojewodztwo = plik[1][0]
    okreg = ""
    powiat = ""
    gmina = ""

    wyniki_kandydatow = [0 for i in range(12)]
    for y in range(1, 2495):
        if plik[y][0] != wojewodztwo:
            dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart,
                          wyjetych_kart, niewaznych_glosow, waznych_glosow)
            wojewodztwo = plik[y][0]
            for x in range(12):
                wyniki_kandydatow[x] = 0
            uprawnionych = 0
            wydanych_kart = 0
            wyjetych_kart = 0
            niewaznych_glosow = 0
            waznych_glosow = 0

        for x in range(12):
            wyniki_kandydatow[x] += int(plik[y][11 + x])
        uprawnionych += int(plik[y][6])
        wydanych_kart += int(plik[y][7])
        wyjetych_kart += int(plik[y][8])
        niewaznych_glosow += int(plik[y][9])
        waznych_glosow += int(plik[y][10])

    dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart, wyjetych_kart,
                  niewaznych_glosow, waznych_glosow)


def dodaj_statystyki_okregow():
    uprawnionych = 0
    wydanych_kart = 0
    wyjetych_kart = 0
    niewaznych_glosow = 0
    waznych_glosow = 0

    wojewodztwo = plik[1][0]
    okreg = plik[1][1]
    powiat = ""
    gmina = ""

    wyniki_kandydatow = [0 for i in range(12)]
    for y in range(1, 2495):
        if plik[y][1] != okreg:
            dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart,
                          wyjetych_kart, niewaznych_glosow, waznych_glosow)
            wojewodztwo = plik[y][0]
            okreg = plik[y][1]
            for x in range(12):
                wyniki_kandydatow[x] = 0
            uprawnionych = 0
            wydanych_kart = 0
            wyjetych_kart = 0
            niewaznych_glosow = 0
            waznych_glosow = 0

        for x in range(12):
            wyniki_kandydatow[x] += int(plik[y][11 + x])
        uprawnionych += int(plik[y][6])
        wydanych_kart += int(plik[y][7])
        wyjetych_kart += int(plik[y][8])
        niewaznych_glosow += int(plik[y][9])
        waznych_glosow += int(plik[y][10])

    dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart, wyjetych_kart,
                  niewaznych_glosow, waznych_glosow)


def dodaj_statystyki_powiatow():
    powiaty = {}
    ost = ''
    ile_powiatow = 0
    gmina = ""
    for y in range(1, 2495):
        if plik[y][4] != ost:
            ost = plik[y][4]
            ile_powiatow += 1
            powiaty[ost] = 1
    for key in powiaty:
        uprawnionych = 0
        wydanych_kart = 0
        wyjetych_kart = 0
        niewaznych_glosow = 0
        waznych_glosow = 0
        wyniki_kandydatow = [0 for i in range(12)]
        for y in range(1, 2495):
            if plik[y][4] == key:
                wojewodztwo = plik[y][0]
                okreg = plik[y][1]
                powiat = plik[y][4]
                for x in range(12):
                    wyniki_kandydatow[x] += int(plik[y][11 + x])
                uprawnionych += int(plik[y][6])
                wydanych_kart += int(plik[y][7])
                wyjetych_kart += int(plik[y][8])
                niewaznych_glosow += int(plik[y][9])
                waznych_glosow += int(plik[y][10])
        dodaj_do_bazy(wojewodztwo, okreg, powiat, gmina, wyniki_kandydatow, uprawnionych, wydanych_kart, wyjetych_kart,
                      niewaznych_glosow, waznych_glosow)


def dodaj_statystyki_gmin():
    for y in range(1, 2495):
        wyniki_kandydatow = [int(plik[y][11 + x]) for x in range(12)]
        dodaj_do_bazy(plik[y][0], plik[y][1], plik[y][4], plik[y][3], wyniki_kandydatow, int(plik[y][6]), int(plik[y][7]),
                      int(plik[y][8]), int(plik[y][9]), int(plik[y][10]))


print("Dodaje kandydatów do bazy ...")
dodaj_kandydatow_do_bazy_danych()
print("-------------------------")
print("... Dodałem kandydatów do bazy")
print("-------------------------")
print("Dodaje statysytki Polski ...")
dodaj_statystyki_Polski()
print("... Dodałem statystyki Polski")
print("-------------------------")
print("Dodaje statysytki wojewodztw ...")
dodaj_statystyki_wojewodztw()
print("... Dodałem statystyki wojewodztw")
print("-------------------------")
print("Dodaje statystyki okregow ...")
dodaj_statystyki_okregow()
print("... Dodałem statystyki okregow")
print("-------------------------")
print("Dodaje statystyki powiatow ...")
dodaj_statystyki_powiatow()
print("... Dodałem statystyki powiatow")
print("-------------------------")
print("Dodaje statystyki gmin ...")
dodaj_statystyki_gmin()
print("...Dodalem statystyki gmin")
print("--------KONIEC------------")

User.objects.create_user(username="u1", password="p1")
User.objects.create_user(username="u2", password="p2")
print("Dodalem uzytkownikow (username:'u1', password:'p1'), (username:'u2', password:'p2')")
# x = Wynik()
# x.wojewodztwo = "abecadłowo"
# x.okreg = 12
# x.save(x)
