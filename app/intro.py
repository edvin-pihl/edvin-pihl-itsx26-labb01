import re

print("Hej ITSX26!")
print("Jag studerar IT- och Cybersäkerhet.")

while True:
    name = input("Vad heter du? ")

    if re.fullmatch(r"[A-Öa-ö ]+", name):
        break

    else:
         print("Fel! Använd endast bokstäver (A-Ö). Försök igen.")

print(f"Hej {name}! Välkommen till kursen IT- och Cybersäkerhet.")