# Platforms: web, mobile
# UI Components: button, checkbox


# Products
class WebButton:
    def render(self):
        print("Rendering 'web button' ...")

class WebCheckbox:
    def render(self):
        print("Rendering 'web checkbox' ...")

class MobileButton:
    def render(self):
        print("Rendering 'mobile button' ...")

class MobileCheckbox:
    def render(self):
        print("Rendering 'mobile checkbox' ...")


# Pythonic AbstractFactory: dataclass + dependency injection
from dataclasses import dataclass
from typing import Type


@dataclass
class UIFactory:
    button: Type
    checkbox: Type

    def create_button(self):
        return self.button()

    def create_checkbox(self):
        return self.checkbox()


# Concrete factories
web_factory = UIFactory(
    button=WebButton,
    checkbox=WebCheckbox)

mobile_factory = UIFactory(
    button=MobileButton,
    checkbox=MobileCheckbox)


# Client
def build_ui(factory: UIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.render()
    checkbox.render()


print('Build web ui:')
build_ui(web_factory)

print('\nBuild mobile ui:')
build_ui(mobile_factory)
