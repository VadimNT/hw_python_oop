from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MSG = ('Тип тренировки: {training_type}; '
           'Длительность: {duration:.3f} ч.; '
           'Дистанция: {distance:.3f} км; '
           'Ср. скорость: {speed:.3f} км/ч; '
           'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить сообщение о тренировке"""
        return self.MSG.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Расчет каллорий недоступен!')

    def show_training_info(self) -> InfoMessage:
        """"Получить информацию о тренировке"""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER = 18
    SHIFTER = 20

    def get_spent_calories(self) -> float:
        result = (((self.MULTIPLIER * self.get_mean_speed()
                    - self.SHIFTER) * self.weight)
                  / self.M_IN_KM * self.duration * self.MIN_IN_H)
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER1 = 0.035
    MULTIPLIER2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (self.MULTIPLIER1
                          * self.weight
                          + (self.get_mean_speed() ** 2 // self.height)
                          * self.MULTIPLIER2
                          * self.weight) * self.duration * self.MIN_IN_H
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CORR_MEAN_SPEAD = 1.1
    MULTIPLIER = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.CORR_MEAN_SPEAD)
                          * self.MULTIPLIER
                          * self.weight)
        return spent_calories


"""Словарь CLASS_TRAINING содержит допустимые тренировки:
RUN - бег,
WLK - спортивная ходьба (бег),
SWM - плавание."""

CLASS_TRAINING: Dict[str, Training] = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming}


def read_package(t_type: str, params_training: list) -> Training:
    """Считать входные данные с датчиков."""
    if t_type in CLASS_TRAINING:
        return CLASS_TRAINING[t_type](*params_training)
    raise TypeError('Тренировка не задана!')


def main(t: Training) -> None:
    """Головная функция"""
    info = t.show_training_info()
    info_training = info.get_message()
    print(info_training)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    if len(packages) > 0:
        for i in range(len(packages)):
            try:
                workout_type = packages[i][0]
                data = packages[i][1]
                training = read_package(workout_type, data)
                main(training)
            except TypeError:
                print('Параметры переданы неправильно!')
            except ZeroDivisionError:
                print('Датчики не исправны!')
    else:
        print('Параметры фитнесс-трекера не переданы!')
