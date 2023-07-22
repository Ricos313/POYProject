import datetime as dt
from sputnik import Sputnik, G, astronomical_unit


def func1(mass):
    with open('data.txt', 'w') as file:
        for i in mass:
            file.write(str(i) + '\n')


def sum_mass(mass):
    return [mass[0] + 1, mass[1] + 2, mass[2] - 2]


t = dt.datetime.now()
delta_t = dt.timedelta(minutes=1)
# with open('satellite_params') as satellite_params:
#     params_list = satellite_params.readlines()
#     for i in range(len(params_list)):
#         params_list[i] = params_list[i].split(', ')
#     print(params_list)
sputnik1 = Sputnik([1, 0, 5], [1, 1, 1], 200, 25500000, 0.00068)
timer = 0

with open('data.txt', 'w') as f:
    for i in range(2000):
        # if (t.hour, t.minute) == (dt.datetime.now().hour, dt.datetime.now().minute):
        t += delta_t
        sputnik1.rotating(64.9, 120, 135, 500, timer)
        timer += 3500
        for j in sputnik1.coords:
            print(j, end=' ', file=f)
        if sputnik1.is_object_in_cone(50.402395, 30.532690, 65):
            print(1, file=f)
        else:
            print(0, file=f)
