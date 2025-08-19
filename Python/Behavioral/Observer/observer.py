from abc import ABC, abstractmethod


class JopPost:
    
    def __init__(self, title):
        self._title = title
    
    @property
    def title(self):
        return self._title


class Observer(ABC):
    
    @abstractmethod
    def on_job_posted(self, post):
        pass


class JobSeeker(Observer):
    
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    def on_job_posted(self, job_post):
        print (f'Hi {self.name}! New job posted: {job_post.title}')


class Observable(ABC):
    
    @property
    @abstractmethod
    def observers(self):
        pass
    
    @abstractmethod
    def _notify(self, post):
        pass
    
    @abstractmethod
    def attach(self, observer):
        pass
    
    @abstractmethod
    def detach(self, observer):
        pass


class EmploymentAgency(Observable):
    
    def __init__(self):
        self._observers = list()
    
    @property
    def observers(self):
        return self._observers
    
    def _notify(self, job_posting):
        for observer in self.observers:
            observer.on_job_posted(job_posting)
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def add_job(self, job_posting):
        self._notify(job_posting)


john = JobSeeker('john')
sara = JobSeeker('sara')

job_posting = EmploymentAgency()
job_posting.attach(john)
job_posting.attach(sara)

job_posting.add_job(JopPost('Sofware Engineer'))

job_posting.detach(sara)
job_posting.add_job(JopPost('DevOps Engineer'))
