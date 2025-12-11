class Route:
    def __init__(self, route_id, route_code, name, transport_type, distance_km):
        self.route_id = route_id
        self.route_code = route_code
        self.name = name
        self.transport_type = transport_type
        self.distance_km = distance_km

    def get_route_info(self):
        return f"{self.transport_type} '{self.route_code}' – {self.name} ({self.distance_km} км)"

class Driver:
    def __init__(self, driver_id, first_name, last_name, experience_years):
        self.driver_id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.experience_years = experience_years

    def get_info(self):
        return f"Водій {self.first_name} {self.last_name}, досвід {self.experience_years} років"

class VehicleType:
    def __init__(self, type_id, name, capacity):
        self.type_id = type_id
        self.name = name
        self.capacity = capacity

class Vehicle:
    def __init__(self, vehicle_id, vehicle_number, active, description, vehicle_type: VehicleType):
        self.vehicle_id = vehicle_id
        self.vehicle_number = vehicle_number
        self.active = active
        self.description = description

        # Зв’язок
        self.vehicle_type = vehicle_type

    def get_vehicle_info(self):
        return f"{self.vehicle_type.name} №{self.vehicle_number} (місць: {self.vehicle_type.capacity})"

class Stop:
    def __init__(self, stop_id, code, name, address):
        self.stop_id = stop_id
        self.code = code
        self.name = name
        self.address = address

    def get_info(self):
        return f"Зупинка {self.code}: {self.name}, {self.address}"

class StopTime:
    def __init__(self, stop_sequence, arrival_time, departure_time, stop: Stop, trip):
        self.stop_sequence = stop_sequence
        self.arrival_time = arrival_time
        self.departure_time = departure_time

        # Звʼязки
        self.stop = stop
        self.trip = trip

class Trip:
    def __init__(self, trip_id, trip_code, route: Route, start_time, end_time, vehicle: Vehicle, driver: Driver):
        self.trip_id = trip_id
        self.trip_code = trip_code
        self.route = route
        self.start_time = start_time
        self.end_time = end_time

        # Звʼязки
        self.vehicle = vehicle
        self.driver = driver

        # Список зупинок (StopTime)
        self.stop_times = []

    def add_stop_time(self, stop_time: StopTime):
        self.stop_times.append(stop_time)

    def get_full_info(self):
        return (
            f"Рейс {self.trip_code} — {self.route.get_route_info()}\n"
            f"Транспорт: {self.vehicle.get_vehicle_info()}\n"
            f"Виконує: {self.driver.get_info()}\n"
        )

class TripExtended(Trip):
    def __init__(self, *args, direction=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction  # 1 = прямий, 0 = зворотний

    def get_direction_text(self):
        return "Прямий" if self.direction == 1 else "Зворотний"

class DriverMixin:
    def get_driver_short(self):
        return f"{self.driver.first_name} {self.driver.last_name}"

class TripWithDriver(Trip, DriverMixin):
    def get_combined_info(self):
        base = self.get_full_info()
        return base + f"Коротко про водія: {self.get_driver_short()}"





bus_type = VehicleType(1, "Автобус", 80)
tram_type = VehicleType(2, "Трамвай", 160)


print(f"{bus_type.name}, місткість: {bus_type.capacity}")
print(f"{tram_type.name}, місткість: {tram_type.capacity}")


vehicle1 = Vehicle(101, "AB1234", True, "Solaris Urbino 12", bus_type)
vehicle2 = Vehicle(102, "TR320", True, "Tatra KT4", tram_type)

print(vehicle1.get_vehicle_info())
print(vehicle2.get_vehicle_info())


routeA = Route(10, "A5", "Центр — Аеропорт", "Автобус", 12.5)
routeT = Route(11, "T3", "Площа Ринок — Вокзал", "Трамвай", 7.8)

print(routeA.get_route_info())
print(routeT.get_route_info())

driver1 = Driver(1, "Олег", "Петровський", 12)
driver2 = Driver(2, "Ірина", "Самойлович", 8)

print(driver1.get_info())
print(driver2.get_info())


trip_basic = Trip(
    trip_id=200,
    trip_code="A5-09",
    route=routeA,
    start_time="09:00",
    end_time="09:40",
    vehicle=vehicle1,
    driver=driver1
)

print(trip_basic.get_full_info())

trip_ext = TripExtended(
    trip_id=201,
    trip_code="T3-14",
    route=routeT,
    start_time="14:10",
    end_time="14:40",
    vehicle=vehicle2,
    driver=driver2,
    direction=0
)

print(trip_ext.get_full_info())
print("Напрямок:", trip_ext.get_direction_text())

trip_mixed = TripWithDriver(
    trip_id=202,
    trip_code="A5-12",
    route=routeA,
    start_time="12:00",
    end_time="12:40",
    vehicle=vehicle1,
    driver=driver1
)

print(trip_mixed.get_combined_info())


stop1 = Stop(1, "S01", "Центр", "Головна площа")
stop2 = Stop(2, "S02", "Ринок", "Вул. Базарна")
stop3 = Stop(3, "S03", "Аеропорт", "Термінал A")
trip_basic.add_stop_time(StopTime(1, "09:00", "09:01", stop1, trip_basic))
trip_basic.add_stop_time(StopTime(2, "09:10", "09:11", stop2, trip_basic))
trip_basic.add_stop_time(StopTime(3, "09:35", "09:40", stop3, trip_basic))

print("Зупинки додано для базового рейсу!")


trips = [trip_basic, trip_ext, trip_mixed]
for t in trips:
    print("\nОб'єкт:", type(t).__name__)
    print(t.get_full_info() if hasattr(t, "get_full_info") else t.get_combined_info())
