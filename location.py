


class Location:
    def __init__(self,coords,count:int=None,size=None):
        self.coords = coords
        self.count = count
        self.size = size
        self.detected = 1

    def __str__(self):
        return "(" + str(self.coords) + ',' + str(self.count) + "," + str(self.size) + "," + str(self.detected) + ")"

    def __repr__(self):
        return self.__str__()