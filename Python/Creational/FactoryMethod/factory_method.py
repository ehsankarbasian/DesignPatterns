from abc import ABC, abstractmethod


class InterviewerInterface(ABC):
    
    @abstractmethod
    def ask_questions(self):
        pass


class Developer(InterviewerInterface):
    
    def ask_questions(self):
        print('Asking about programming.')


class HREmployee(InterviewerInterface):
    
    def ask_questions(self):
        print('Where do you see yourself in five years later !?')


class AbstractHiringManager(ABC):
    
    # Factory Method
    @abstractmethod
    def _make_interviewer(self):
        pass
    
    def take_interview(self):
        interviewer = self._make_interviewer()
        interviewer.ask_questions()


class DevelopmentManager(AbstractHiringManager):
    
    def _make_interviewer(self):
        return Developer()


class HumanResourcesManager(AbstractHiringManager):
    
    def _make_interviewer(self):
        return HREmployee()


dev_manager = DevelopmentManager()
dev_manager.take_interview()

hr_manager = HumanResourcesManager()
hr_manager.take_interview()
