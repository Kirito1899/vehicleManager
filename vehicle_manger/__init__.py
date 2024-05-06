from dataclasses import fields, asdict
import geopy.distance
from .vehicle import Vehicle

import requests


class VehicleManger:

    vehicles = '/vehicles'

    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self):
        response = requests.get(self.url + self.vehicles)
        raw_vehicles = response.json()
        return [Vehicle(**element) for element in raw_vehicles]

    def get_vehicle(self, vehicle_id: int):
        response = requests.get(f'{self.url}{self.vehicles}/{vehicle_id}')
        raw_vehicle = response.json()
        return Vehicle(**raw_vehicle)

    def filter_vehicles(self, params: dict):
        self._validate_params(params)
        vehicles = self.get_vehicles()
        filtered_result = list(filter(
            lambda x: all(getattr(x, key) == value for key, value in params.items()), vehicles
        ))
        return filtered_result

    def add_vehicle(self, veh: Vehicle):
        del veh.id
        response = requests.post(f'{self.url}{self.vehicles}', data=asdict(veh))
        if response.status_code == 201:
            return response.content
        return f"Ошибка: {response.status_code}"

    def _validate_params(self, params: dict):
        valid_keys = set(field.name for field in fields(Vehicle))
        for key in params.keys():
            if key not in valid_keys:
                raise ValueError(f"Ключ {key} не является допустимым для класса Vehicle")
        return params

    def update_vehicle(self, veh: Vehicle):
        if veh.id is None:
            return False
        response = requests.put(f'{self.url}{self.vehicles}/{veh.id}', json=asdict(veh))
        if response.status_code == 200:
            return True
        return False

    def delete_vehicle(self, id: int):
        response = requests.delete(f'{self.url}{self.vehicles}/{id}')
        if response.status_code == 204:
            return True
        else:
            print(f"Ошибка: {response.status_code}")
            print(response.text)
            return False

    @staticmethod
    def _get_distace_km(vehicle1: Vehicle, vehicle2: Vehicle):
        return geopy.distance.geodesic((vehicle1.latitude, vehicle1.longitude),
                                       (vehicle2.latitude, vehicle2.longitude)).km

    def get_distance(self, id1: int, id2: int):
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        return self._get_distace_km(vehicle1, vehicle2)

    def get_nearest_vehicle(self, id: int):
        min_distance = float("inf")
        nearest_vehicle = None
        my_vehicle = self.get_vehicle(id)
        vehicles = self.get_vehicles()
        for veh in vehicles:
            if veh.id == my_vehicle.id:
                continue
            distance = self._get_distace_km(my_vehicle, veh)
            if distance < min_distance:
                min_distance = distance
            nearest_vehicle = asdict(veh)
        return nearest_vehicle
