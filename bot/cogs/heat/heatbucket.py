import time


class HeatBucket:
    def __init__(self, max_heat_age: int = 3600):
        self.age = max_heat_age
        self.heat = 0
        self.heats = []

    def collect_expired(self):
        for item in self.heats:
            if time.time() < item[0]:
                self.heat -= item[1]

        if self.heat < 0:
            self.heat = 0

    def add(self, amount: int):
        self.heat += amount
        self.heats.append((round(time.time()), amount))
        self.collect_expired()
        return self.heat
