from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def home_page(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=6529385ba8f6c3c160458f9199feabc4"
    
    #This checks what the form is trying to do with the database
    #In this case, we are adding to the database
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    #This returns a cleared form for the user
    form = CityForm()
    
    #Holds the data of each city we added to the database
    weather_data = []

    #loops through our database and store weather details
    cities = City.objects.all()
    for city in cities:
        response =requests.get(url.format(city))
        data_from_api = response.json()
        weather_details ={
            #Returns cityName instead of its object
            'city': city.name,
            'description': data_from_api['weather'][0]['description'],
            'temperature': data_from_api['main']['temp'],
            'icon': data_from_api['weather'][0]['icon'],
        }
        weather_data.append(weather_details)


    #Data that will be displayed on our database
    context = {
        'weather_data': weather_data,
        'form': form,
    }

    return render(request, 'weather/index.html', context)