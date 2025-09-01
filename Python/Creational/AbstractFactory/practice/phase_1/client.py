from concrete import SamaungFactory, SonyFactory, LgFactory

'''
Implement products [
    TV,
    Radio,
    Phone,
    Camera
]
for the brands [
    Samsung,
    Sony
    LG,
]
'''


# Client code:
if __name__ == "__main__":
    samsung_factory = SamaungFactory()
    sony_factory = SonyFactory()
    lg_factory = LgFactory()
    
    small_samsung_tv = samsung_factory.make_tv(diameter=12)
    mid_samsung_tv = samsung_factory.make_tv(diameter=27)
    big_samsung_tv = samsung_factory.make_tv(diameter=52)
    
    small_sony_tv = sony_factory.make_tv(diameter=12)
    mid_sony_tv = sony_factory.make_tv(diameter=27)
    big_sony_tv = sony_factory.make_tv(diameter=52)
    
    small_lg_tv = lg_factory.make_tv(diameter=12)
    mid_lg_tv = lg_factory.make_tv(diameter=27)
    big_lg_tv = lg_factory.make_tv(diameter=52)
