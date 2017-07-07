from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.logowanie,
        {},
        name='logowanie'
    ),
    url(
        r'^polska$',
        views.strona,
        {'wojewodztwo': '', 'okreg': '', 'powiat': '', 'gmina': ''},
        name='polska'
    ),
    url(
        r'^wyszukiwarka$',
        views.wyszukiwarka,
        {},
        name='wyszukiwarka'
    ),
    url(
        r'^polska/wojewodztwo/(?P<wojewodztwo>[\w-]+)$',
        views.strona,
        {'okreg': '', 'powiat': '', 'gmina': ''},
        name='woj'
    ),
    url(
        r'^polska/wojewodztwo/(?P<wojewodztwo>[\w-]+)/okreg/(?P<okreg>[\w-]+)$',
        views.strona,
        {'powiat': '', 'gmina': ''},
        name='okr'),
    url(
        r'^polska/wojewodztwo/(?P<wojewodztwo>[\w-]+)/okreg/(?P<okreg>[\w-]+)/powiat/(?P<powiat>[>_\w-]+)$',
        views.strona,
        {'gmina': ''},
        name='pow'
    ),
    url(
        r'^polska/wojewodztwo/(?P<wojewodztwo>[\w-]+)/okreg/(?P<okreg>[\w-]+)/powiat/(?P<powiat>[._\w-]+)/gmina/(?P<gmina>[._\w-]+)$',
        views.strona,
        name='gmi'
    ),
    url(
        r'^polska/wojewodztwo/(?P<wojewodztwo>[\w-]+)/okreg/(?P<okreg>[\w-]+)/powiat/(?P<powiat>[._\w-]+)/gmina/(?P<gmina>[._\w-]+)/edycja$',
        views.edycja,
        name='edit'
    ),


]