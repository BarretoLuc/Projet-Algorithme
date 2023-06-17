from OSMPythonTools.nominatim import Nominatim
from typing import List
import requests

from models.cityModel import CityModel

class CityService:
    def __init__(self) -> None:
        pass
    
    def get_coordinates(self, city: str) -> List[float]:
        nominatim = Nominatim()
        area = nominatim.query(city)
        return area.toJSON()[0]['lat'], area.toJSON()[0]['lon']
    
    def load_cities(self, path: str):
        cities = []
        with open(path, encoding='utf8') as file:
            
            for line in file:
                city = line.rstrip('\n').split(',')
                x, y = self.get_coordinates(city[0])
                cities.append(CityModel(city[0], float(x), float(y)))
        return cities
    
