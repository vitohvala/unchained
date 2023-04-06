class flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name):
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)

fly = flight(3)
poeple = ["Ja", "Mile", "Milorad", "Biske"]

for person in poeple:
    succes = fly.add_passenger(person)
    if succes:
        print(f"Added {person} to flight")
    else:
        print(f"No available seats for {person}")
