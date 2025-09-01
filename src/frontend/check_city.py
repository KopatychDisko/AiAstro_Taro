from geopy.geocoders import Nominatim
import pycountry

geolocator = Nominatim(user_agent="geo_checker", timeout=10)

def get_info_from_city(city_name):
    location = geolocator.geocode(city_name, language='en', exactly_one=True)
    if not location:
        return None
    
    address_types = ['town', 'city', 'hamlet', 'state', 'county']
    
    if location.raw['addresstype'] not in address_types:
        return None
    
    country = location.raw['display_name'].split(', ')[-1]
    alpha_2 = pycountry.countries.search_fuzzy(country)[0].alpha_2
    
    city = location.raw['display_name'].split(', ')[0]
    
    return city, alpha_2