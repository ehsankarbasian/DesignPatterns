from abstract import AbstractHomeApplianceFactory
from abstract import AbstractVacuumCleaner, AbstractLaundry, AbstractFridge


# Concrete Factory
class AzmayeshFactory(AbstractHomeApplianceFactory):
    
    def make_vacuum_cleaner(self, model_number):
        return _AzmayeshVacuumCleaner(model_number=model_number)
    
    def make_laundry(self, generation):
        return _AzmayeshLaundry(generation=generation)
    
    def make_fridge(self, type_):
        return _AzmayeshFridge(type_=type_)


# Concrete Products
class _AzmayeshVacuumCleaner(AbstractVacuumCleaner):
    
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


class _AzmayeshLaundry(AbstractLaundry):
    
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


class _AzmayeshFridge(AbstractFridge):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        return '__NOT_AS_SOON_AS_YOUR_DEATH__'
    
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
