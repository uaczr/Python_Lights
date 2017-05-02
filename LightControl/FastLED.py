class FastLED

    # https://github.com/FastLED/FastLED/blob/master/colorutils.cpp
    def fill_solid(leds, numToFill, CRGBcolor)
        for i in Range(numToFill)
            leds[i] = CRGBcolor

