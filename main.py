from vehicle_manger import VehicleManger, Vehicle

manager = VehicleManger(url="https://test.tspb.su/test-task")
print(manager.get_vehicles())

print(manager.filter_vehicles(params={"name": "Toyota"}))

print(manager.get_vehicle(vehicle_id=1))

new_veh = manager.add_vehicle(
        veh=Vehicle(
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
     )
 )
print(new_veh)

up_veh = manager.update_vehicle(
        veh=Vehicle(
            id=1,
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
     )
 )
print(up_veh)

print(manager.delete_vehicle(id=1))

print(manager.get_distance(id1=1, id2=2))

print(manager.get_nearest_vehicle(id=1))