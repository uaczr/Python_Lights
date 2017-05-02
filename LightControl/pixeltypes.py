
#http://fastled.io/docs/3.1/pixeltypes_8h_source.html

class CRGB:
        def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def __init__(self, _r, _g, _b):
        self.r = _r
        self.g = _g
        self.b = _b


class CHSV:
    def __init__(self):
        self.h = 0
        self.s = 0
        self.v = 0

    def __init__(self, _h, _s, _v):
        self.h = _h
        self.s = _s
        self.v = _v