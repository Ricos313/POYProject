import math
from functions_physics import *


astronomical_unit = 149597870
G = 6.67 * 10 ** -11
m = 3.986 * 10 ** 14


class Sputnik:
    def __init__(self, coords, speeds, h, larger_axel, e, memory=100):
        self.coords = coords
        self.speeds = speeds
        self.u = m * G
        self.memory = memory
        self.h = h
        self.smaller_axel = larger_axel * math.sqrt(1 - e*e)
        self.e = e
        self.large_axel = larger_axel
        self.lon, self.lat = xyz_to_lonlat(self.coords[0], self.coords[1], self.coords[2])

    # def rotating(self, i, o, w, M0, t):
    #     n = calculation_n(m, self.large_axel)
    #
    #     M = calculation_M(M0, n, t)
    #
    #     E = calculation_E(M, self.e)
    #
    #     E2 = math.radians(E)
    #
    #     O = calculation_O_angle(self.e, E, E2)\
    #
    #     u = w + O
    #
    #     r = calculation_r(self.large_axel, self.e, O)
    #
    #     self.coords = calculation_coords(r, o, u, i)
    #
    #     p = self.large_axel * (1 - self.e ** 2)
    #
    #     self.speeds = calculation_speeds(m, p, self.e, i, o, u, O)
    #
    #     self.lon, self.lat = xyz_to_lonlat(self.coords[0], self.coords[1], self.coords[2])

    def rotating(self, i, o, w, T, t):
        p = self.large_axel * (1 - self.e ** 2)

        M = sqrt(m / self.large_axel ** 3) * (t - T)

        E = calculation_E(M, self.e)

        v = 2 * atan(sqrt((1 + self.e)/(1 - self.e)) * tan(radians(E) / 2))

        u = w + v

        r = p / (1 + self.e * cos(radians(v)))

        coordinates = calculation_coords(r, o, u, i)
        self.coords.x, self.coords.y, self.coords.z = coordinates[0], coordinates[1], coordinates[2]

        self.speeds = calculation_speeds(m, p, self.e, i, o, u, v)
    # def is_object_in_cone(self, object_lat, object_lon, cone_angle):
    #     self.lat = radians(self.lat)
    #     self.lon = radians(self.lon)
    #     object_lat = radians(object_lat)
    #     object_lon = radians(object_lon)
    #
    #     earth_radius = 6371.0
    #
    #     # Расчет длин дуги и направления между спутником и объектом
    #     g = Geod(ellps='WGS84')
    #     _, _, distance = g.inv(self.lon, self.lat, object_lon, object_lat)
    #
    #     # Расчет высоты конуса видимости
    #     cone_height = earth_radius * sin(radians(cone_angle))
    #
    #     # Расчет радиуса основания конуса видимости
    #     cone_radius = earth_radius * cos(radians(cone_angle))
    #
    #     # Проверка, попадает ли объект внутрь конуса видимости
    #     print(object_lat, self.lat)
    #     return distance <= cone_radius and abs(object_lat - self.lat) <= cone_height

    def is_object_in_cone(self, object_lat, object_lon, cone_angle):
        object_lat_rad = math.radians(object_lat)
        object_lon_rad = math.radians(object_lon)

        object_x = math.cos(object_lat_rad) * math.cos(object_lon_rad)
        object_y = math.cos(object_lat_rad) * math.sin(object_lon_rad)
        object_z = math.sin(object_lat_rad)

        cone_base_x = self.coords.x
        cone_base_y = self.coords.y
        cone_base_z = self.coords.z

        dot_product = (object_x * cone_base_x) + (object_y * cone_base_y) + (object_z * cone_base_z)

        object_magnitude = math.sqrt(object_x ** 2 + object_y ** 2 + object_z ** 2)
        cone_base_magnitude = math.sqrt(cone_base_x ** 2 + cone_base_y ** 2 + cone_base_z ** 2)

        angle = math.degrees(math.acos(dot_product / (object_magnitude * cone_base_magnitude)))
        if angle <= cone_angle:
            return True
        else:
            return False
