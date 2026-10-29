from concrete import SamaungFactory, SonyFactory, LgFactory, NokiaFactory, ArjFactory, AzmayeshFactory

'''
Implement products [
    TV,
    Radio,
    Phone,
    Camera,
    VacuumCleaner,
    Laundry,
    Fridge
]
for the brands [
    LG,
    Samsung,
    Sony,
    Arj,
    Azmayesh,
    Nokia
]

Raise Exception if the brand doesn't produce the product

The productions of each brand matrix:
                |    LG      |  Samsung   |    Sony    |    Arj     |  Azmayesh  |    Nokia   |
    Radio       |     1      |     1      |     1      |     0      |     0      |     0      |
    TV          |     1      |     1      |     1      |     0      |     0      |     0      |
    Phone       |     1      |     1      |     1      |     0      |     0      |     1      |
    Camera      |     1      |     1      |     1      |     0      |     0      |     0      |
  VacuumCleaner |     1      |     1      |     0      |     1      |     1      |     0      |
    Laundry     |     1      |     1      |     0      |     1      |     1      |     0      |
    Fridge      |     1      |     1      |     0      |     1      |     1      |     0      |
'''


# Client code:
if __name__ == "__main__":
    samsung_factory = SamaungFactory()
    sony_factory = SonyFactory()
    lg_factory = LgFactory()
    nokia_factory = NokiaFactory()
    arj_factory = ArjFactory()
    azmayesh_factory = AzmayeshFactory()
    
    print('\nCreate and use TVs:')
    small_samsung_tv = samsung_factory.make_tv(diameter=12)
    big_sony_tv = sony_factory.make_tv(diameter=52)
    mid_lg_tv = lg_factory.make_tv(diameter=27)
    big_sony_tv.channel_down()
    mid_lg_tv.weight
    small_samsung_tv.turn_on()
    small_samsung_tv.diameter
    
    print('\nCreate and use Radios:')
    old_sony_radio = sony_factory.make_radio(version=2)
    new_samsung_radio = samsung_factory.make_radio(version=14)
    old_sony_radio.set_mode(mode='FM')
    old_sony_radio.volume_up()
    new_samsung_radio.turn_off()
    
    print('\nCreate and use Phones:')
    good_sony_phone = sony_factory.make_phone(model='Xperia')
    lg_wing_phone = lg_factory.make_phone(model='wing')
    nokia_1 = nokia_factory.make_phone(model='1200')
    nokia_2 = nokia_factory.make_phone(model='6600')
    good_sony_phone.call(number='0999***1111')
    lg_wing_phone.reject_call()
    good_sony_phone.turn_off()
    nokia_1.call(number='0999***2222')
    print(nokia_1.average_life_span)
    nokia_1.turn_off()
    nokia_2.turn_on()
    nokia_2.reject_call()
    
    print('\nCreate and use Cameras:')
    sony_camera = sony_factory.make_camera(mega_pixels=128)
    samsung_camera = samsung_factory.make_camera(mega_pixels=64)
    sony_camera.take_picture()
    samsung_camera.take_film
    sony_camera.weight
    
    print('\nCreate and use Vacuum Cleaners:')
    lg_vacuum_cleaner = lg_factory.make_vacuum_cleaner(model_number=15)
    arj_vacuum_cleaner = arj_factory.make_vacuum_cleaner(model_number=2)
    lg_vacuum_cleaner.turn_off()
    arj_vacuum_cleaner.turn_on()
    print(arj_vacuum_cleaner.warranty_expiration_date)
    print(arj_vacuum_cleaner.average_life_span)
    
    print('\nCreate and use Laundries:')
    samsung_laundary = samsung_factory.make_laundry(generation=12)
    arj_laundary = arj_factory.make_laundry(generation=4224)
    azmayesh_laundary = azmayesh_factory.make_laundry(generation=2)
    samsung_laundary.turn_off()
    print(arj_laundary.warranty_expiration_date)
    azmayesh_laundary.turn_off()
    
    print('\nCreate and use Fridges:')
    lg_fridge = lg_factory.make_fridge(type_='freezer')
    arj_fridge = arj_factory.make_fridge(type_='fridge')
    azmayesh_fridge = azmayesh_factory.make_fridge(type_='freezer-fridge')
    lg_fridge.turn_off()
    arj_fridge.turn_on()
    print(arj_fridge.average_life_span)
    print(arj_fridge.warranty_expiration_date)
    print(azmayesh_fridge.average_life_span)
