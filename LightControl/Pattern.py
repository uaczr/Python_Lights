from pixeltypes import CRGB

class Pattern:

    def __init__(self, _variable1):
        self.fastLED = FastLED()

    def baseChoser():
        temp = int(nbasePattern / 255 * 6)

        # switch/case
        temp = {
            1: baseRectDimm(),
            2: baseLinDimm(),
            3: baseQuadDimm(),
            4: baseQuadDimmRand50(),
            5: baseCompartements(),
            6: baseStatic(),
        }.get(x, fillBlack())

    def baseRectDimm():
        if (millisSinceBeat < nbaseSpeed / 255 * beatPeriodMillis):
            fill_solid(this->backleds, side_length, dimByVal(baseColor, nbaseDim))
            else:
            fill_solid(leds, length, CRGB::Black)

    def baseLinDimm():
        if (millisSinceBeat < nbaseSpeed / 255 * beatPeriodMillis):
            CRGB
            col(baseColor)
            col.r = (unsigned
            int)(linearApp(col.r, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.g = (unsigned
            int)(linearApp(col.g, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.b = (unsigned
            int)(linearApp(col.b, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            fill_solid(backleds, side_length, dimByVal(col, nbaseDim))
        else:
            fill_solid(leds, length, CRGB::Black)

    def baseQuadDimm():
        if (millisSinceBeat < nbaseSpeed / 255 * beatPeriodMillis):
            CRGB
            col(baseColor)
            col.r = (unsigned
            int)(quadApp(col.r, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.g = (unsigned
            int)(quadApp(col.g, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.b = (unsigned
            int)(quadApp(col.b, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            fill_solid(backleds, side_length, dimByVal(col, nbaseDim))
        else:
            fill_solid(leds, length, CRGB::Black)

    def baseQuadDimmRand50():
        if (millisSinceBeat == 0 & & first):
            if (rand() > RAND_MAX / 2):
                onRand = true
            else:
                onRand = false
            first = false
        if (millisSinceBeat > 0):
            first = true
        if (millisSinceBeat < nbaseSpeed / 255 * beatPeriodMillis & & onRand):
            CRGB
            col(baseColor)
            col.r = (unsigned
            int)(quadApp(col.r, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.g = (unsigned
            int)(quadApp(col.g, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.b = (unsigned
            int)(quadApp(col.b, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            fill_solid(backleds, side_length, dimByVal(col, nbaseDim))
        else:
            fill_solid(leds, length, CRGB::Black):

    def baseCompartements():
        if (millisSinceBeat == 0 & & first):
            first = false
            comp = rand() % 4
        if (millisSinceBeat > 0):
            first = true
        if (millisSinceBeat < nbaseSpeed / 255 * beatPeriodMillis):
            CRGB
            col(baseColor)
            col.r = (unsigned
            int)(
            quadApp(col.r, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.g = (unsigned
            int)(
            quadApp(col.g, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            col.b = (unsigned
            int)(
            quadApp(col.b, 0, nbaseSpeed / 255 * beatPeriodMillis, millisSinceBeat))
            fillCompartmentBack(dimByVal(col, nbaseDim), comp)
        else:
            fill_solid(leds, length, CRGB::Black)

    def baseStatic():
        fill_solid(leds, length, dimByVal(baseColor, nbaseDim))

    def fillBlack():
        fill_solid(leds, length, CRGB::Black)


    def quadApp(amp1, amp2, deltax, x)
        if (amp1 > amp2):
            return (amp1 - amp2) / (deltax * deltax) * x * x - 2 * (
            amp1 - amp2) / (deltax) * x + amp1
        else:
            return (amp2 - amp1) / (deltax * deltax) * x * x + amp1