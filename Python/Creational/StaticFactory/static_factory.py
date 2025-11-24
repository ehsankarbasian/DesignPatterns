from abc import ABC, abstractmethod


class DataReaderInterface(ABC):
    
    @abstractmethod
    def read_data(self, filename: str):
        pass


class CsvReader(DataReaderInterface):
    
    def read_data(self, filename):
        print(f'Reading the CSV file: "{filename}"')


class JsonReader(DataReaderInterface):
    
    def read_data(self, filename):
        print(f'Reading the JSON file: "{filename}"')


class XmlReader(DataReaderInterface):
    
    def read_data(self, filename):
        print(f'Reading the XML file: "{filename}"')


# Static factory
class DataProcessor:
    
    @staticmethod
    def create_data_reader(type_: str) -> DataReaderInterface:
        if type_ == 'csv':
            return CsvReader()
        elif type_ == 'json':
            return JsonReader()
        elif type_ == 'xml':
            return XmlReader()
        else:
            raise Exception


class Client:
    
    @staticmethod
    def run(type_: str):
        data_reader = DataProcessor.create_data_reader(type_=type_)
        data_reader.read_data('my_file_name')


Client.run(type_='json')
