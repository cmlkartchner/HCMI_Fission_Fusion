class Memory:

    def __init__(self, hexagons):
        self.memory = {key:-1 for key in hexagons.keys()}

    