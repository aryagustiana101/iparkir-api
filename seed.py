import os
from faker import Faker

from app.services import spots
from app.libs.constants import SPOTS_FILE_DATA

fake = Faker(locale="id_ID")


def main():
    try:
        reset = input("Do you want to reset the parking spots data? (y/n) ")
        length = input("How many fake parking spots do you want to create? ")

        if not length.isdigit():
            print("\nInvalid input")
            return

        if reset.lower() == "y" or reset.lower() == "yes":
            if os.path.exists(SPOTS_FILE_DATA):
                os.remove(SPOTS_FILE_DATA)

            print("\nSuccessfully reset parking spots data")

        for _ in range(int(length)):
            spots.create_spot(
                status="available",
                name=str(fake.company()),
                location=str(fake.address()),
                description=str(fake.text()),
                price_rate=fake.random_int(10000, 100000),
            )

        print(f"\nSuccessfully created {length} fake parking spots")
    except:
        return None


if __name__ == "__main__":
    main()
