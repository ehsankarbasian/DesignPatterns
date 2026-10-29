
# Products
class DarkButton:
    pass

class DarkMenu:
    pass

class LightButton:
    pass

class LightMenu:
    pass


# Abstract factory
class ThemeFactory:
    button = None
    menu = None

    def create_button(self):
        return self.button()

    def create_menu(self):
        return self.menu()


# Concrete factories
class DarkThemeFactory(ThemeFactory):
    button = DarkButton
    menu = DarkMenu

class LightThemeFactory(ThemeFactory):
    button = LightButton
    menu = LightMenu


# Client
factory = DarkThemeFactory()

button = factory.create_button()
menu = factory.create_menu()
