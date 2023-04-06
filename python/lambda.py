ppl = [
    {"name": "Mile", "House": "Gruffindor"},
    {"name": "Cho", "House": "Ravenclaw"},
    {"name": "Draco", "House": "Slytherin"}
]

def f(person):
    return person["name"]

ppl.sort(key=lambda person: person["name"])

print(ppl)
