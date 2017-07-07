// Czy mogę to "var chart = " usunąć, bo z tego co widzę to bez tego też działa
// Szczególnie że nie używam tej zmiennej nigdzie ??? chociaż używam "wykresKolumnowy"
// Dlaczego to też działa bez tego ???
var chart = AmCharts.makeChart("wykresKolumnowy", {
            "type": "serial",
            "theme": "light",
            "marginRight": 70,
            "dataProvider": [
                {% for dana in dane_do_wykresu %}
                {
                    "name": "{{ dana.kandydat }}",
                    "percent": "{{ dana.procent }}",
                    "color": "#"+((1<<24)*Math.random()|0).toString(16)
                },
                {% endfor %}
            ],
            "valueAxes": [{
                "axisAlpha": 0,
                "position": "left",
                "title": "Procentowa liczba głosow"
            }],
            "startDuration": 1,
            "graphs": [{
                "balloonText": "<b>[[category]]: [[value]]</b>",
                "fillColorsField": "color",
                "fillAlphas": 0.9,
                "lineAlpha": 0.2,
                "type": "column",
                "valueField": "percent"
            }],
            "chartCursor": {
                "categoryBalloonEnabled": false,
                "cursorAlpha": 0,
                "zoomable": false
            },
            "categoryField": "name",
            "categoryAxis": {
                "gridPosition": "start",
                "labelRotation": 45
            },
            "export": {
                "enabled": true
            }

        });