from abc import ABC, abstractmethod


# Subject
class Image(ABC):
    
    @abstractmethod
    def display(self):
        pass


# RealSubject
class RealImage(Image):
    
    def __init__(self, filename: str):
        self.filename = filename
        self._load_image_from_disk()

    def _load_image_from_disk(self):
        print(f"Loading image: {self.filename} from disk")

    def display(self):
        print(f"Displaying image: {self.filename}")


# Proxy
class ProxyImage(Image):
    
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            # Lazy load image: Instantiate only if necessary really
            self._real_image = RealImage(self.filename)
        
        self._real_image.display()


# Client code
image = ProxyImage("example.jpg")
# Image will be loaded from disk only when display() is called (lazy loading)
image.display()
# Image will not be loaded again, as it has been cached in the Proxy
image.display()
image.display()
