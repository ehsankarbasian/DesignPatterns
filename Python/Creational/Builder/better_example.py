from abc import ABC, abstractmethod


class Car:
    
    def set_seat_count(self, count):
        print(f'{count} seats for the Car')
    
    def set_seat_type(self, type_):
        print(f'Seats type is: {type_}')
    
    def set_engine_power(self, power):
        print(f'Engine power: {power} HP')
    
    def set_engine_volume(self, volume):
        print(f'Engine volume: {volume}')
    
    def set_trip_computer_model_no(self, model_no):
        print(f'Trip computer model number: {model_no}')
    
    def set_gps(self):
        print('The car have GPS now.')


class Manual:
    
    def set_seats(self, **kwargs):
        print('Manual set_seats', kwargs)
    
    def set_engine(self, **kwargs):
        print('Manual set_engine', kwargs)
    
    def set_about_trip_computer(self, **kwargs):
        print('Manual set_about_trip_computer', kwargs)
    
    def set_about_gps(self):
        print('Manual set_about_gps')


class BuilderInterface(ABC):
    
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def set_seats(self, count, type_):
        pass
    
    @abstractmethod
    def set_engine(self, power, volume):
        pass
    
    @abstractmethod
    def set_trip_computer(self, model_no):
        pass
    
    @abstractmethod
    def set_gps(self):
        pass


class CarBuilder(BuilderInterface):
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._car = Car()
    
    def set_seats(self, count, type_):
        self._car.set_seat_count(count)
        self._car.set_seat_type(type_)
    
    def set_engine(self, power, volume):
        self._car.set_engine_power(power)
        self._car.set_engine_volume(volume)
    
    def set_trip_computer(self, model_no):
        self._car.set_trip_computer_model_no(model_no)
    
    def set_gps(self):
        self._car.set_gps()
    
    def get_product(self):
        product = self._car
        self.reset()
        return product


class CarManualBuilder(BuilderInterface):
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._car_manual = Manual()
    
    def set_seats(self, count, type_):
        self._car_manual.set_seats(count=count, type_=type_)
    
    def set_engine(self, power, volume):
        self._car_manual.set_engine(power=power, volume=volume)
    
    def set_trip_computer(self, model_no):
        self._car_manual.set_about_trip_computer(model_no=model_no)
    
    def set_gps(self):
        self._car_manual.set_about_gps()
    
    def get_product(self):
        product = self._car_manual
        self.reset()
        return product


class Director:
    
    def construct_sport_car(self, builder):
        print('\nconstruct_sport_car')
        builder.reset()
        builder.set_seats(2, 'Gaming')
        builder.set_engine(power=360, volume=2000)
        builder.set_trip_computer(model_no=2)
        builder.set_gps()
    
    def construct_suv_car(self, builder):
        print('\nconstruct_suv_car')
        builder.reset()
        builder.set_seats(6, 'RestSeat')
        builder.set_engine(power=80, volume=1500)
        builder.set_trip_computer(model_no=1)
        builder.set_gps()


if __name__ == "__main__":
    director = Director()
    
    car_builder = CarBuilder()
    director.construct_sport_car(car_builder)
    sport_car = car_builder.get_product()

    car_manual_builder = CarManualBuilder()
    director.construct_sport_car(car_manual_builder)
    sport_car_manual = car_manual_builder.get_product()
    
    car_builder.reset()
    director.construct_suv_car(car_builder)
    sport_car = car_builder.get_product()
    
    car_manual_builder.reset()
    director.construct_suv_car(car_manual_builder)
    sport_car_manual = car_manual_builder.get_product()
