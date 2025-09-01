from abstract import AbstractProductFactory
from abstract import AbstractVacuumCleaner, AbstractLaundry, AbstractFridge


# Concrete Factory
class ArjFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        raise Exception
    
    def make_radio(self, version):
        raise Exception
    
    def make_phone(self, model):
        raise Exception
    
    def make_camera(self, mega_pixels):
        raise Exception
    
    def make_vacuum_cleaner(self, model_number):
        return _ArjVacuumCleaner(model_number=model_number)
    
    def make_laundry(self, generation):
        return _ArjLaundry(generation=generation)
    
    def make_fridge(self, type_):
        return _ArjFridge(type_=type_)


# Concrete Products
class _ArjVacuumCleaner(AbstractVacuumCleaner):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        pass
    
    @property
    def warranty_expiration_date(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    def set_level(self):
        pass
    
    def restract_cord(self):
        pass


class _ArjLaundry(AbstractLaundry):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        pass
    
    @property
    def warranty_expiration_date(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    @property
    def capacity(self):
        pass
    
    def set_program(self):
        pass


class _ArjFridge(AbstractFridge):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        pass
    
    @property
    def warranty_expiration_date(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    @property
    def feet_tall(self):
        pass
    
    @property
    def temperature(self):
        pass
    
    def boost(self):
        pass
