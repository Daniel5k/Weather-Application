from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def home_page(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=6529385ba8f6c3c160458f9199feabc4"
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    
    weather_data = []
    cities = City.objects.all()
    for city in cities:
        response =requests.get(url.format(city))
        data_from_api = response.json()
        weather_details ={
            'city': city.name,
            'description': data_from_api['weather'][0]['description'],
            'temperature': data_from_api['main']['temp'],
            'icon': data_from_api['weather'][0]['icon'],
        }
        weather_data.append(weather_details)

    context = {
        'weather_data': weather_data,
        'form': form,
    }
    return render(request, 'weather/index.html', context)