
from pprint import pprint
from decimal import *
import time
import json
import csv
import datetime

getcontext().prec = 50
REMAINING_TIME = '1234567890.0987654321'
FIELD_NAMES = ['current_location_name', 'current_experience', 'current_date']
VICTORY = 280
NICE = '*' * 15
LINES = '-' * 60
remaining_time = Decimal(REMAINING_TIME)
start = time.monotonic()
new_loc = True
journal = []

class Hero:
    def __init__(self):
        self.remaining_time = remaining_time
        self.current_location_name = list(LOCATIONS.keys())[0]
        self.current_location = LOCATIONS[self.current_location_name]
        self.current_experience = Decimal(0)
        self.current_date = datetime.datetime.now()

    def moving_to_new_loc(self, loc):
        self.current_location_name = self.dict_of_objects['Locs'][loc]
        for list_obj in self.current_location:
            if self.current_location_name in list_obj:
                self.current_location = list_obj[self.current_location_name]
        self.remaining_time -= Decimal((self.current_location_name.split('tm')[1]))

    def attack(self, mob):
        self.current_experience += Decimal(mob.split('_')[1].lstrip('exp'))
        self.remaining_time -= Decimal((mob.split('tm')[1]))


    def find_objects(self):
        self.dict_of_objects = {'Mobs':[],'Locs':[]}
        for _object in self.current_location:
            if 'Mob' in _object or 'Boss' in _object:
                self.dict_of_objects['Mobs'].append(_object)

            new_locations = (*_object,)

            for loc in new_locations:
                if 'Loc' in loc:
                    self.dict_of_objects['Locs'].append(loc)

        return self.dict_of_objects



with open("rpg.json", "r") as read_file:
    LOCATIONS = json.load(read_file)



# запуск игры
print(f'{NICE} Добро пожаловать в игру {NICE}')
hero = Hero()

while hero.remaining_time > 0:
    # описание статусов
    print(
        f'{LINES}\n'
        f'Вы находитесь в {hero.current_location_name}\n'
        f'У вас {hero.current_experience} опыта и осталось {hero.remaining_time} секунд игрового времени\n'
        f'Прошло уже {datetime.datetime.now() - hero.current_date} реального времени\n'
        'Внутри вы видите:'
    )

    if new_loc:
        mobs_and_locs = hero.find_objects()
        new_loc = False
    pprint(mobs_and_locs)

    print(
        'Доступные действия:\n'
        '1. Атаковать монстра\n'
        '2. Перейти в другую локацию\n'
        '3. Выход\n'
        f'{LINES}\n'
    )

    # выбор дальнейших действий по номеру ответа
    number = int(input('Введите номер действия: '))

    if number == 1:
        if len(mobs_and_locs['Mobs']) > 0:
            mob = mobs_and_locs['Mobs'].pop()
            hero.attack(mob)
            print(f'Атакую монстра {mob}!')
        else:
            print('Монстров нет!')

    elif number == 2:
        new_loc = True
        digit_of_locs = len(mobs_and_locs['Locs'])

        if digit_of_locs == 0:
            print('Доступных локаций нет!')
        else:
            if digit_of_locs == 1:
                number_of_loc = 0
            else:
                number_of_loc = int(input('Выберите конкретную локацию по её номеру: '))
            print(f'Перехожу в локацию {mobs_and_locs["Locs"][number_of_loc]}')
            hero.moving_to_new_loc(number_of_loc)

    elif number == 3:
        print(f'{NICE} Вы выключили игру {NICE}')
        break

    else:
        print('Такого номера нет')

    if hero.current_experience >= VICTORY:
        print(f'{NICE} ПОБЕДА! Вы всех спасли и вообще молодец! {NICE}')

    journal.append([hero.current_location_name, hero.current_experience, hero.remaining_time])

with open('dungeon.csv', 'w', newline='') as out_csv:
    writer = csv.writer(out_csv)
    writer.writerow(FIELD_NAMES)
    writer.writerows(journal)





