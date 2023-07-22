from math import cos, sin, radians, fmod, sqrt, floor, atan, asin, acos, pi, tan
from pyproj import Geod, Transformer, CRS
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import ephem

m = 3.986 * 10 ** 14


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def calculation_n(m, a):
    return sqrt(m) / (a * sqrt(a))


def calculation_M(M0, n, t):
    return ((M0 * 3.14 / 180) + n * t * 3.14) * 180 / 3.14


def calculation_E(M, e):
    E0 = M + e * sin(radians(M))
    Ek = M + e * sin(radians(E0))
    n = 1
    while Ek - E0 > 10 ** -8:
        E0 = Ek
        Ek = E0 + e * sin(radians(E0))
    return Ek


def calculation_O_angle(e, E, E2):
    return E + 2 * (atan((e * sin(E2)) / (1 + sqrt(1 - e ** 2) - e * cos(E2))))


def calculation_r(a, e, O):
    return (a * (1 - e ** 2)) / 1 + e * cos(radians(O))


def calculation_coords(r, o, u, i):
    x = r * (cos(radians(o)) * cos(radians(u)) - sin(radians(o)) * sin(
        radians(u)) * cos(radians(i)))
    y = r * (sin(radians(o)) * cos(radians(u)) + cos(radians(o)) * sin(
        radians(u)) * cos(radians(i)))
    z = r * sin(radians(u)) * sin(radians(i))
    return [int(x), int(y), int(z)]


def calculation_speeds(m, p, e, i, o, u, O):
    first_coeff = sqrt(m / p) * e * sin(radians(O))
    second_coeff = sqrt(m / p) * (1 + e * cos(radians(O)))
    x_first_coeff = (cos(radians(o)) * cos(radians(u)) - sin(radians(o)) * sin(radians(u)) * cos(radians(i)))
    x_second_coeff = (-1 * cos(radians(o)) * sin(radians(u)) - sin(radians(o)) * cos(radians(u)) * cos(radians(i)))
    x = first_coeff * x_first_coeff + second_coeff * x_second_coeff
    y_first_coeff = (sin(radians(o)) * cos(radians(u)) + cos(radians(o)) * sin(
        radians(u)) * cos(radians(i)))
    y_second_coeff = (-1 * sin(radians(o)) * sin(radians(u)) + cos(radians(o)) * cos(
        radians(u)) * cos(radians(i)))
    y = first_coeff * y_first_coeff + second_coeff * y_second_coeff
    z_first_coeff = sin(radians(u)) * sin(radians(i))
    z_second_coeff = cos(radians(u)) * sin(radians(i))
    z = first_coeff * z_first_coeff + second_coeff * z_second_coeff
    return [x, y, z]


# def xyz_to_lonlat(x, y, z):
#     x, y, z = x, y, z
#     # Создаем объект Transformer для преобразования координат
#     transformer = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(4978), always_xy=True)
#
#     # Преобразовываем координаты из x, y, z в долготу и широту
#     lon, lat, _ = transformer.transform(x, y, z)
#     rxy = sqrt(x * x + y * y)
#     len = sqrt(x * x + y * y + z * z)
#     lat = asin(z / len)
#     lon = acos(x / rxy)
#     if y < 0:
#         lon = 2 * pi - lon
#
#     return lon, lat


def ICS_to_GCS(pos, starTime):
    cw = cos(radians(starTime))
    sw = sin(radians(starTime))

    x = cw * pos.x + sw * pos.y
    y = -1 * sw * pos.x + cw * pos.y
    pos.x = x
    pos.y = y
    return


# def starTime(lat, lon):
#     obs = ephem.Observer()
#     obs.lat = lat
#     obs.lon = lon
#     sun = ephem.Sun()
#     current_time = datetime.now()
#     obs.date = current_time
#     sun.compute(obs)
#     sidereal_time_deg = ephem.degrees(sun.ra)
#     return sidereal_time_deg


def get_star_time(t):
    twopi = 2 * pi
    deg2rad = pi / 180

    dtDate = t.date()
    dtTime = t.time()
    year = dtDate.year
    mon = dtDate.month
    day = dtDate.day
    hr = dtTime.hour
    minute = dtTime.minute
    sec = dtTime.second

    jd = 367 * year - floor((7 * (year + floor((mon + 9) / 12))) * 0.25) + floor(275 * mon / 9) + day + 1721013.5 + (
            (sec / 60 + minute) / 60 + hr) / 24
    jdut1 = jd
    tut1 = (jdut1 - 2451545) / 36525
    temp = -6.2e-6 * tut1 * tut1 * tut1 + 0.093104 * tut1 * tut1 + (876600 * 3600 + 8640184.812866) * tut1 + 67310.54841
    temp = fmod(temp * deg2rad/240, twopi)
    if temp < 0:
        temp += twopi
    return temp

print(get_star_time(datetime.now()))
