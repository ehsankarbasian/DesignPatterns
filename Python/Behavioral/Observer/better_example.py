from abc import ABC, abstractmethod


# Subject interface
class PublisherInterface(ABC):
    
    def register(self, subscriber):
        pass
    
    def deregister(self, subscriber):
        pass
    
    def notify_subscribers(self):
        pass


# Concrete subject
class Publisher(PublisherInterface):

    def __init__(self):
        self.__subscribers = []
        self.__latest_books = []
        self.__all_books = []

    def register(self, subscriber):
        self.__subscribers.append(subscriber)

    def deregister(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self.__subscribers:
            subscriber.update(self)
        self._clear_latest_books()

    def _clear_latest_books(self):
        self.__latest_books = []
        
    def add_book(self, book):
        self.__all_books.append(book)
        self.__latest_books.append(book)

    @property
    def all_books(self):
        return self.__all_books
    
    @property
    def latest_books(self):
        return self.__latest_books
    
    @property
    def subscribers(self):
        return [type(s).__name__ for s in self.__subscribers]


# Observer interface
class SubscriberInterface(ABC):

    @abstractmethod
    def update(self, subject):
        pass


# Concrete Observer 1
class SMSSubscriber(SubscriberInterface):

    def update(self, subject):
        print("Update from:", type(subject).__name__, subject.latest_books)


# Concrete Observer 2
class EmailSubscriber(SubscriberInterface):

    def update(self, subject):
        print("Update from:", type(subject).__name__, subject.latest_books)


# Concrete Observer 3
class AnyOtherSubscriber(SubscriberInterface):

    def update(self, subject):
        print("Update from:", type(subject).__name__, subject.latest_books)


if __name__ == '__main__':
    sms_subscriber = SMSSubscriber()
    email_subscriber = EmailSubscriber()
    other_subscriber = AnyOtherSubscriber()
    
    publisher = Publisher()
    publisher.register(sms_subscriber)
    publisher.register(email_subscriber)
    publisher.register(other_subscriber)
    
    print("\nSubscribers: ", publisher.subscribers)
    publisher.add_book("Advanced Python")
    publisher.notify_subscribers()
    
    publisher.deregister(email_subscriber)
    print("\nUnregistered: EmailSubscriber")
    print("\nSubscribers: ", publisher.subscribers)
    
    publisher.add_book("Clean Code")
    publisher.add_book("The Clean Coder")
    publisher.notify_subscribers()
