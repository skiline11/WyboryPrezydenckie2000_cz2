from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View
from django.template import context
from .models import Wynik, Kandydat
from .forms import WynikZPostForm



def edycja(request, wojewodztwo, okreg, powiat, gmina):
    form = WynikZPostForm()
    powiat = str(powiat).replace("_", " ")
    gmina = str(gmina).replace("_", " ")
    print("Jestem tutaj :-D HELLO")
    print("Wojewodztwo = " + wojewodztwo)
    print("Okreg = " + okreg)
    print("Powiat = " + powiat)
    print("Gmina = " + gmina)
    kandydaci = Kandydat.objects.all()
    wyniki = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat, gmina=gmina)
    w = wyniki[0]
    liczba_glosow = [w.w1, w.w2, w.w3, w.w4, w.w5, w.w6, w.w7, w.w8, w.w9, w.w10, w.w11, w.w12]
    parzyste = [{'kandydat': kandydaci[i * 2], 'glosy': int(liczba_glosow[i * 2])} for i in range(6)]
    nieparzyste = [{'kandydat': kandydaci[i * 2 + 1], 'glosy': int(liczba_glosow[i * 2 + 1])} for i in range(6)]
    dane = [{'parzyste': parzyste[i], 'nieparzyste': nieparzyste[i]} for i in range(6)]
    powiat = str(powiat).replace(" ", "_")
    gmina = str(gmina).replace(" ", "_")
    return render(request, 'wyniki/edytujWyniki.html', {
        'dane': dane,
        'form': form,
        'wojewodztwo': wojewodztwo,
        'okreg': okreg,
        'powiat': powiat,
        'gmina': gmina
    })
    # return HttpResponse('<p>dziala</p>')


def aktualizuj_baze(post, diff, diff_all):
    msc_tab = Wynik.objects.filter(wojewodztwo=post.wojewodztwo, okreg=post.okreg, powiat=post.powiat, gmina=post.gmina)
    msc = msc_tab[0]

    msc.waznych_glosow += diff_all
    msc.niewaznych_glosow = msc.wyjetych_kart - msc.waznych_glosow

    msc.w1 += diff[1]
    msc.w2 += diff[2]
    msc.w3 += diff[3]
    msc.w4 += diff[4]
    msc.w5 += diff[5]
    msc.w6 += diff[6]
    msc.w7 += diff[7]
    msc.w8 += diff[8]
    msc.w9 += diff[9]
    msc.w10 += diff[10]
    msc.w11 += diff[11]
    msc.w12 += diff[12]

    msc.save()


def logowanie(request):
    return render(request, 'wyniki/logowanie.html')


# Stworzyć konto na gitlabie / bitbuckecie i wysłać : założyć projekt i wysłać link na maila
# Dopisać wyszukiwarkę

def strona(request, wojewodztwo, okreg, powiat, gmina):

    powiat = str(powiat).replace("_", " ")
    gmina = str(gmina).replace("_", " ")
    print("******************************************************")
    print("Nazwa obszaru jest " + wojewodztwo + "/" + okreg + "/" + powiat + "/" + gmina)
    print("******************************************************")

    if request.method == "POST" and wojewodztwo == "": #logujemy sie
        print("Logujemy sie")
        zalogowany_uzytkownik = authenticate(username=request.POST['username'], password=request.POST['password'])
        if zalogowany_uzytkownik is None:
            print("Nie przeszlismy logowania")
            return render(request, 'wyniki/logowanie.html')
        else:
            print("Przeszlismy logowanie")

    print("przeszlismy logowanie")
    if request.method == "POST" and wojewodztwo != "": #updatujemy dane
        print("Metoda post")
        danePost = WynikZPostForm(request.POST)

        dane = Wynik()
        dane.wojewodztwo = wojewodztwo
        dane.okreg = okreg
        dane.powiat = powiat
        dane.gmina = gmina
        if danePost.is_valid():
            gm = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat, gmina=gmina)
            ta_gmina = gm[0]

            roznica_poszczegolnych_glosow = [
                0, danePost.cleaned_data['w1'] - ta_gmina.w1, danePost.cleaned_data['w2'] - ta_gmina.w2,
                danePost.cleaned_data['w3'] - ta_gmina.w3, danePost.cleaned_data['w4'] - ta_gmina.w4,
                danePost.cleaned_data['w5'] - ta_gmina.w5, danePost.cleaned_data['w6'] - ta_gmina.w6,
                danePost.cleaned_data['w7'] - ta_gmina.w7, danePost.cleaned_data['w8'] - ta_gmina.w8,
                danePost.cleaned_data['w9'] - ta_gmina.w9, danePost.cleaned_data['w10'] - ta_gmina.w10,
                danePost.cleaned_data['w11'] - ta_gmina.w11, danePost.cleaned_data['w12'] - ta_gmina.w12]

            roznica_glosow = 0
            for i in range(13):
                roznica_glosow += roznica_poszczegolnych_glosow[i]

            # print("Roznica glosow : " + roznica_glosow)

            aktualizuj_baze(dane, roznica_poszczegolnych_glosow, roznica_glosow)
            dane.gmina = ""
            aktualizuj_baze(dane, roznica_poszczegolnych_glosow, roznica_glosow)
            dane.powiat = ""
            aktualizuj_baze(dane, roznica_poszczegolnych_glosow, roznica_glosow)
            dane.okreg = ""
            aktualizuj_baze(dane, roznica_poszczegolnych_glosow, roznica_glosow)
            dane.wojewodztwo = ""
            aktualizuj_baze(dane, roznica_poszczegolnych_glosow, roznica_glosow)

        else:
            print("Formularz nie jest valid")

    kandydaci = Kandydat.objects.all()
    typ_statystyk = ""
    wyniki_ogolne = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat, gmina=gmina)

    if wojewodztwo == "":
        typ_statystyk = "wojewodztwo"
        staty_szczegolowe = Wynik.objects.filter(okreg="").exclude(wojewodztwo="")
    elif okreg == "":
        typ_statystyk = "okreg"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, powiat="").exclude(okreg="")
    elif powiat == "":
        typ_statystyk = "powiat"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, gmina="").exclude(powiat="")
    elif gmina == "":
        typ_statystyk = "gmina"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat).exclude(gmina="")

    w = wyniki_ogolne[0]
    liczba_glosow = [w.w1, w.w2, w.w3, w.w4, w.w5, w.w6, w.w7, w.w8, w.w9, w.w10, w.w11, w.w12]
    suma_glosow = 0
    for i in range(12):
        suma_glosow += liczba_glosow[i]
    procentowa_liczba_glosow = [liczba_glosow[i] * 100 / suma_glosow for i in range(12)]
    parzyste = [{'kandydat': kandydaci[i * 2].imieINazwisko, 'glosy': int(liczba_glosow[i * 2]),
                 'procent': format(procentowa_liczba_glosow[i * 2], '.2f')} for i in range(6)]
    nieparzyste = [{'kandydat': kandydaci[i * 2 + 1].imieINazwisko, 'glosy': int(liczba_glosow[i * 2 + 1]),
                    'procent': format(procentowa_liczba_glosow[i * 2 + 1], '.2f')} for i in range(6)]
    dane = [{'parzyste': parzyste[i], 'nieparzyste': nieparzyste[i]} for i in range(6)]
    nazwa_wykresu = "Polska"
    frekwencja = w.wydanych_kart * 100 / w.uprawnionych
    if typ_statystyk == "wojewodztwo" or typ_statystyk == "okreg":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
        } for i in range(staty_szczegolowe.__len__())]
        # wyniki_szczegolowe = [[staty_szczegolowe[i], format(frekwencja_szczegolowa[i], '.2f'), ''] for i in
        #                       range(staty_szczegolowe.__len__())]
    elif typ_statystyk == "powiat":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
            'powiat_z_podkreslnikiem': staty_szczegolowe[i].powiat.replace(' ', '_'),
        } for i in range(staty_szczegolowe.__len__())]
        # wyniki_szczegolowe = [[staty_szczegolowe[i], format(frekwencja_szczegolowa[i], '.2f'), staty_szczegolowe[i].gmina.replace(' ', '_')] for i in
        #                       range(staty_szczegolowe.__len__())]
    elif typ_statystyk == "gmina":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
            'powiat_z_podkreslnikiem': staty_szczegolowe[i].powiat.replace(' ', '_'),
            'gmina_z_podkreslnikiem': staty_szczegolowe[i].gmina.replace(' ', '_'),
        } for i in range(staty_szczegolowe.__len__())]
    else:
        wyniki_szczegolowe = [
            wojewodztwo,
            okreg,
            powiat.replace(' ', '_'),
            gmina.replace(' ', '_')
        ]
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print(wojewodztwo)
        print(okreg)
        print(powiat)
        print(gmina)
        print("~~~~~~~~~~~~~~~~~~~~~~~~")

    dane_do_wykresu = [{
        'kandydat': kandydaci[i].imieINazwisko,
        'glosy': liczba_glosow[i],
        'procent': format(procentowa_liczba_glosow[i], '.2f')
    } for i in range(12)]

    return render(request, 'wyniki/templateStrony.html', {
        'dane': dane,
        'nazwa_wykresu': nazwa_wykresu,
        # 'adres_js': adres_js,
        'statystyki_obszaru': w,
        'frekwencja': format(frekwencja, '.2f'),
        'typ_statystyk': typ_statystyk,
        'wyniki_szczegolowe': wyniki_szczegolowe,

        'dane_do_wykresu': dane_do_wykresu,
        'suma_glosow': suma_glosow,
    })

def wyszukiwarka(request):
    print("Jestem w wyszukiwarce")

    wojewodztwo = request.POST['wojewodztwo']
    okreg = request.POST['okreg']
    powiat = request.POST['powiat']
    gmina = request.POST['gmina']

    print("Wojewodztwo " + wojewodztwo + "Gmina " + gmina + "Powiat " + powiat + "Okreg " + okreg)
    kandydaci = Kandydat.objects.all()
    typ_statystyk = ""
    wyniki_ogolne = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat, gmina=gmina)
    if wyniki_ogolne.count() == 0:
        return HttpResponse("<p>Nie istnieje takie miejsce</p>")
    if wojewodztwo == "":
        typ_statystyk = "wojewodztwo"
        staty_szczegolowe = Wynik.objects.filter(okreg="").exclude(wojewodztwo="")
    elif okreg == "":
        typ_statystyk = "okreg"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, powiat="").exclude(okreg="")
    elif powiat == "":
        typ_statystyk = "powiat"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, gmina="").exclude(powiat="")
    elif gmina == "":
        typ_statystyk = "gmina"
        staty_szczegolowe = Wynik.objects.filter(wojewodztwo=wojewodztwo, okreg=okreg, powiat=powiat).exclude(gmina="")

    w = wyniki_ogolne[0]
    liczba_glosow = [w.w1, w.w2, w.w3, w.w4, w.w5, w.w6, w.w7, w.w8, w.w9, w.w10, w.w11, w.w12]
    suma_glosow = 0
    for i in range(12):
        suma_glosow += liczba_glosow[i]
    procentowa_liczba_glosow = [liczba_glosow[i] * 100 / suma_glosow for i in range(12)]
    parzyste = [{'kandydat': kandydaci[i * 2].imieINazwisko, 'glosy': int(liczba_glosow[i * 2]),
                 'procent': format(procentowa_liczba_glosow[i * 2], '.2f')} for i in range(6)]
    nieparzyste = [{'kandydat': kandydaci[i * 2 + 1].imieINazwisko, 'glosy': int(liczba_glosow[i * 2 + 1]),
                    'procent': format(procentowa_liczba_glosow[i * 2 + 1], '.2f')} for i in range(6)]
    dane = [{'parzyste': parzyste[i], 'nieparzyste': nieparzyste[i]} for i in range(6)]
    nazwa_wykresu = "Polska"
    frekwencja = w.wydanych_kart * 100 / w.uprawnionych
    if typ_statystyk == "wojewodztwo" or typ_statystyk == "okreg":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
        } for i in range(staty_szczegolowe.__len__())]
        # wyniki_szczegolowe = [[staty_szczegolowe[i], format(frekwencja_szczegolowa[i], '.2f'), ''] for i in
        #                       range(staty_szczegolowe.__len__())]
    elif typ_statystyk == "powiat":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
            'powiat_z_podkreslnikiem': staty_szczegolowe[i].powiat.replace(' ', '_'),
        } for i in range(staty_szczegolowe.__len__())]
        # wyniki_szczegolowe = [[staty_szczegolowe[i], format(frekwencja_szczegolowa[i], '.2f'), staty_szczegolowe[i].gmina.replace(' ', '_')] for i in
        #                       range(staty_szczegolowe.__len__())]
    elif typ_statystyk == "gmina":
        frekwencja_szczegolowa = [wynik.wydanych_kart * 100 / wynik.uprawnionych for wynik in staty_szczegolowe]
        wyniki_szczegolowe = [{
            'szczegoly': staty_szczegolowe[i],
            'frekwencja': format(frekwencja_szczegolowa[i], '.2f'),
            'powiat_z_podkreslnikiem': staty_szczegolowe[i].powiat.replace(' ', '_'),
            'gmina_z_podkreslnikiem': staty_szczegolowe[i].gmina.replace(' ', '_'),
        } for i in range(staty_szczegolowe.__len__())]
    else:
        wyniki_szczegolowe = [
            wojewodztwo,
            okreg,
            powiat.replace(' ', '_'),
            gmina.replace(' ', '_')
        ]
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print(wojewodztwo)
        print(okreg)
        print(powiat)
        print(gmina)
        print("~~~~~~~~~~~~~~~~~~~~~~~~")

    dane_do_wykresu = [{
        'kandydat': kandydaci[i].imieINazwisko,
        'glosy': liczba_glosow[i],
        'procent': format(procentowa_liczba_glosow[i], '.2f')
    } for i in range(12)]

    return render(request, 'wyniki/templateStrony.html', {
        'dane': dane,
        'nazwa_wykresu': nazwa_wykresu,
        # 'adres_js': adres_js,
        'statystyki_obszaru': w,
        'frekwencja': format(frekwencja, '.2f'),
        'typ_statystyk': typ_statystyk,
        'wyniki_szczegolowe': wyniki_szczegolowe,

        'dane_do_wykresu': dane_do_wykresu,
        'suma_glosow': suma_glosow,
    })
