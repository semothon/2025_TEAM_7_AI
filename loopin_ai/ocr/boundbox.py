class BoundBox:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def __str__(self):
        return f"BoundBox({self.x_min}, {self.y_min}, {self.x_max}, {self.y_max})"

    def __repr__(self):
        return self.__str__()

    def area(self):
        return (self.x_max - self.x_min) * (self.y_max - self.y_min)
    
    def is_point_inside(self, point):
        x, y = point
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max
    
    def is_point_inside(self, x, y):
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max
    
    def does_box_include(self, other):
        return (self.x_min <= other.x_min and self.x_max >= other.x_max and
                self.y_min <= other.y_min and self.y_max >= other.y_max)