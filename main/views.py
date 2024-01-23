from django.shortcuts import render
import json
import urllib.request
# Create your views here.

def index(request):
    if request.method == 'POST':
        try:
            city = request.POST['city']
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + 'YOUR_API_KEY').read()
            list_of_data = json.loads(source)
            data = {
                "city": str(list_of_data['name']),
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                "temp": str(round(list_of_data['main']['temp']-273.15)) + '°C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "main": str(list_of_data['weather'][0]['main']),
                "description": str(list_of_data['weather'][0]['description']),
                "icon": list_of_data['weather'][0]['icon'],
            }
            print(data)
        except Exception as e:
            print(e)
            return render(request, "error.html")
    else:
        print("error")
        data={}
        # return render(request, "error.html")
    return render(request, "index.html", data)
