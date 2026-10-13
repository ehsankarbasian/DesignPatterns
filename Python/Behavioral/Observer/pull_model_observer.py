from abc import ABC, abstractmethod


# Declares contract for registering subscribers and querying subject state.
# Subject Interface
class PublisherInterface(ABC):
    """
    Contract for publishers supporting subscriber management and state polling.
    """

    @abstractmethod
    def register(self, subscriber: "SubscriberInterface") -> None:
        pass

    @abstractmethod
    def deregister(self, subscriber: "SubscriberInterface") -> None:
        pass

    @abstractmethod
    def notify_subscribers(self) -> None:
        pass

    @property
    @abstractmethod
    def latest_not_notified(self):
        pass


# Implements reusable subscriber registration and notification infrastructure.
# Simple Observable Base Component
class SimpleObservable(ABC):
    """
    Encapsulates subscriber management logic to prevent duplicate registration code.

    Trade-offs
        Subclasses inherit subscriber bookkeeping but must coordinate notification lifecycle.
    """

    def __init__(self) -> None:
        self._subscribers = []

    def register(self, subscriber: "SubscriberInterface") -> None:
        self._subscribers.append(subscriber)

    def deregister(self, subscriber: "SubscriberInterface") -> None:
        self._subscribers.remove(subscriber)

    def notify_subscribers(self) -> None:
        for subscriber in self._subscribers:
            subscriber.update(self)

    @property
    def subscribers(self):
        return [type(s).__name__ for s in self._subscribers]


# Manages published books and provides state query for pulling observers.
# Concrete Subject Component
class PublisherBook(SimpleObservable, PublisherInterface):
    """
    Book publisher notifying registered subscribers with subject reference.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__latest_books = []
        self.__all_books = []

    def notify_subscribers(self) -> None:
        super().notify_subscribers()
        self._clear_latest_books()

    def _clear_latest_books(self) -> None:
        self.__latest_books = []

    def add_book(self, book: str) -> None:
        self.__all_books.append(book)
        self.__latest_books.append(book)

    @property
    def all_books(self):
        return self.__all_books

    @property
    def latest_not_notified(self):
        return self.__latest_books


# Manages published articles and provides state query for pulling observers.
# Concrete Subject Component
class PublisherArticle(SimpleObservable, PublisherInterface):
    """
    Article publisher notifying registered subscribers with subject reference.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__latest_articles = []
        self.__all_articles = []

    def notify_subscribers(self) -> None:
        super().notify_subscribers()
        self._clear_latest_articles()

    def _clear_latest_articles(self) -> None:
        self.__latest_articles = []

    def add_article(self, article: str) -> None:
        self.__all_articles.append(article)
        self.__latest_articles.append(article)

    @property
    def all_articles(self):
        return self.__all_articles

    @property
    def latest_not_notified(self):
        return self.__latest_articles


# Declares observer contract receiving subject reference to pull state.
# Observer Interface
class SubscriberInterface(ABC):
    """
    Subscriber interface receiving the publisher reference to query updates.
    """

    @abstractmethod
    def update(self, subject: PublisherInterface) -> None:
        pass


# Receives publisher reference and pulls latest books or articles for SMS delivery.
# Concrete Observer Component
class SMSSubscriber(SubscriberInterface):
    """
    SMS delivery subscriber pulling latest unnotified entries from subject.
    """

    def update(self, subject: PublisherInterface) -> None:
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, '\n')


# Receives publisher reference and pulls latest books or articles for Email delivery.
# Concrete Observer Component
class EmailSubscriber(SubscriberInterface):
    """
    Email delivery subscriber pulling latest unnotified entries from subject.
    """

    def update(self, subject: PublisherInterface) -> None:
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, '\n')


# Receives publisher reference and pulls latest books or articles for generic handling.
# Concrete Observer Component
class AnyOtherSubscriber(SubscriberInterface):
    """
    Generic subscriber pulling latest unnotified entries from subject.
    """

    def update(self, subject: PublisherInterface) -> None:
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
