from abc import ABC, abstractmethod


class SectionInterface(ABC):

    @abstractmethod
    def describe(self):
        pass


class PersonalSection(SectionInterface):

    def describe(self):
        print("PersonalSection")


class AlbumSection(SectionInterface):

    def describe(self):
        print("AlbumSection")


class PatentSection(SectionInterface):

    def describe(self):
        print("PatentSection")


class PublicationSection(SectionInterface):

    def describe(self):
        print("PublicationSection")


class BullShitSection(SectionInterface):
    
    def describe(self):
        print("bullshit bullshit bullshit ...")


#Creator
class AbstractProfile(ABC):

    def __init__(self):
        self._sections = []
        self._create_profile()
        print('\nCreated instance: ', type(self).__name__)

    # Factory Method
    @abstractmethod
    def _create_profile(self):
        pass

    def add_sections(self, section):
        self._sections.append(section)
    
    def _pretty_print_sections(self):
        print(f'{type(self).__name__} sections: [')
        for section in self._sections:
            print(f'    {section.__class__.__name__},')
        print(']')


class LinkedIn(AbstractProfile):

    def _create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(PatentSection())
        self.add_sections(PublicationSection())


class FaceBook(AbstractProfile):

    def _create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(AlbumSection())


class Instagram(AbstractProfile):
    
    def _create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(AlbumSection())
        self.add_sections(BullShitSection())


profile = LinkedIn()
profile._pretty_print_sections()

profile = FaceBook()
profile._pretty_print_sections()

profile = Instagram()
profile._pretty_print_sections()
