from abc import ABC, abstractmethod


# Subject interface
class PublisherInterface(ABC):
    
    @abstractmethod
    def register(self, subscriber):
        pass
    
    @abstractmethod
    def deregister(self, subscriber):
        pass
    
    @abstractmethod
    def notify_subscribers(self):
        pass
    
    @property
    @abstractmethod
    def latest_not_notified(self):
        pass


# Concrete subject 1
class PublisherBook(PublisherInterface):

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
    def latest_not_notified(self):
        return self.__latest_books
    
    @property
    def subscribers(self):
        return [type(s).__name__ for s in self.__subscribers]


# Concrete subject 2
class PublisherArticle(PublisherInterface):
    
    def __init__(self):
        self.__subscribers = []
        self.__latest_articles = []
        self.__all_articles = []

    def register(self, subscriber):
        self.__subscribers.append(subscriber)

    def deregister(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify_subscribers(self):
        for subscriber in self.__subscribers:
            subscriber.update(self)
        self._clear_latest_articles()
    
    def _clear_latest_articles(self):
        self.__latest_articles = []

    def add_article(self, article):
        self.__all_articles.append(article)
        self.__latest_articles.append(article)

    @property
    def all_articles(self):
        return self.__all_articles
    
    @property
    def latest_not_notified(self):
        return self.__latest_articles
    
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
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, '\n')

# Concrete Observer 2
class EmailSubscriber(SubscriberInterface):

    def update(self, subject):
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, '\n')


# Concrete Observer 3
class AnyOtherSubscriber(SubscriberInterface):

    def update(self, subject):
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, '\n')

if __name__ == '__main__':
    sms_subscriber = SMSSubscriber()
    email_subscriber = EmailSubscriber()
    other_subscriber = AnyOtherSubscriber()
    
    # Use book publisher
    publisher_book = PublisherBook()
    publisher_book.register(sms_subscriber)
    publisher_book.register(email_subscriber)
    publisher_book.register(other_subscriber)
    print("\nPublisherBook Subscribers: ", publisher_book.subscribers)
    
    publisher_book.add_book("Advanced Python")
    publisher_book.notify_subscribers()
    
    publisher_book.deregister(email_subscriber)
    print("\nnPublisherBook unregistered: EmailSubscriber")
    print("\nPublisherBook Subscribers: ", publisher_book.subscribers)
    
    publisher_book.add_book("Clean Code")
    publisher_book.notify_subscribers()
    
    # Use article publisher
    publisher_article = PublisherArticle()
    publisher_article.register(sms_subscriber)
    publisher_article.register(email_subscriber)
    print("\nPublisherArticle Subscribers: ", publisher_article.subscribers)
    
    publisher_article.add_article("Real Python")
    publisher_article.add_article("Thricks")
    publisher_article.notify_subscribers()
    
    publisher_article.deregister(sms_subscriber)
    print("\nPublisherArticle unregistered: SmsSubscriber")
    publisher_article.register(other_subscriber)
    print("\nPublisherArticle Subscribers: ", publisher_article.subscribers)
    publisher_article.add_article("Design patterns")
    publisher_article.notify_subscribers()
