from abstract import AbstractHomeApplianceFactory
from abstract import AbstractVacuumCleaner, AbstractLaundry, AbstractFridge


# Concrete Factory
class ArjFactory(AbstractHomeApplianceFactory):
    
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
        return '__AFTER_YOUR_LAST_CHILD_DEATH__'
    
    @property
    def warranty_expiration_date(self):
        return '__YOUR_DEAD_THAT_DAY__'
    
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
        return '__FOR_LIFE__'
    
    @property
    def warranty_expiration_date(self):
        return 'The name you know an trust it !'
    
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
        return '__YOU_WILL_DIE_EARLIER__'
    
    @property
    def warranty_expiration_date(self):
        return '__NEWER_NEED_FIX__'
    
    def turn_on(self):
        print('Here we go again !')
    
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
