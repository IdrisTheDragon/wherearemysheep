import abc


class Finder(abc.ABC):
    """
    Abstract class for a Finder to find things in images
    """
    @abc.abstractmethod
    def findInImage(self,image):
        pass