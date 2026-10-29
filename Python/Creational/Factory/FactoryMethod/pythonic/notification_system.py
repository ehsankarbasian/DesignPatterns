from typing import Callable, Dict


class Notification:
    def send(self, message: str):
        raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message: str):
        print(f"Email sent: {message}")

class SMSNotification(Notification):
    def send(self, message: str):
        print(f"SMS sent: {message}")

class PushNotification(Notification):
    def send(self, message: str):
        print(f"Push sent: {message}")


class NotificationFactory:

    _registry: Dict[str, Callable[[], Notification]] = {}

    @classmethod
    def register(cls, name: str, creator: Callable[[], Notification]):
        cls._registry[name] = creator

    @classmethod
    def create(cls, name: str) -> Notification:
        creator = cls._registry.get(name)
        if not creator:
            raise ValueError(f"Unknown notification type: {name}")
        return creator()


# Register the concrete classes
# 'registry pattern': registryـdictionary + callables
NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms", SMSNotification)
NotificationFactory.register("push", PushNotification)


# Client code
notifier = NotificationFactory.create("email")
notifier.send("Hello!")
