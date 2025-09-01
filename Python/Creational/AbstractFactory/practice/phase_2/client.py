from concrete import SamaungFactory, SonyFactory, LgFactory

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
    TV          |     1      |     1      |     1      |     0      |     0      |     1      |
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
    
    print('\nCreate and use TVs:')
    small_samsung_tv = samsung_factory.make_tv(diameter=12)
    big_sony_tv = sony_factory.make_tv(diameter=52)
    mid_lg_tv = lg_factory.make_tv(diameter=27)
    big_sony_tv.channel_down()
    mid_lg_tv.weight
    small_samsung_tv.turn_on()
    small_samsung_tv.diameter
    
    print('\nCreate and use radios:')
    old_sony_radio = sony_factory.make_radio(version=2)
    new_samsung_radio = samsung_factory.make_radio(version=14)
    old_sony_radio.set_mode(mode='FM')
    old_sony_radio.volume_up()
    new_samsung_radio.turn_off()
    
    print('\nCreate and use Phones:')
    good_sony_phone = sony_factory.make_phone(model='Xperia')
    lg_wing_phone = lg_factory.make_phone(model='wing')
    good_sony_phone.call(number='0999***1111')
    lg_wing_phone.reject_call()
    good_sony_phone.turn_off()
    
    print('\nCreate and use Cameras:')
    sony_camera = sony_factory.make_camera(mega_pixels=128)
    samsung_camera = samsung_factory.make_camera(mega_pixels=64)
    sony_camera.take_picture()
    samsung_camera.take_film
    sony_camera.weight
