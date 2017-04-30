class LLSignal:
    name = ""
    value = 0;

    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def register(self):
