from app.constants import ADMIN_USERS_FILE_DATA, CLI_PIN
from app.utils import read_file_data, rewrite_file_data


def get_admin_users():
    file_data = read_file_data(ADMIN_USERS_FILE_DATA)

    users = file_data.get("records") or []

    if len(users) == 0:
        print("\nNo admin users found")
        return None

    print("")
    for user in users:
        print(f"User ID: {user["user_id"]}")

    return None


def add_admin_users():
    file_data = read_file_data(ADMIN_USERS_FILE_DATA)

    id = input("\nEnter ID of the user to add as admin: ")

    increment = (file_data.get("increment") or 0) + 1

    rewrite_file_data(ADMIN_USERS_FILE_DATA, {
        **file_data,
        "increment": increment,
        "records": [
            *(file_data.get("records") or []),
            {"id": increment, "user_id": id}
        ],
    })

    return None


def remove_admin_users():
    file_data = read_file_data(ADMIN_USERS_FILE_DATA)

    id = input("\nEnter ID of the user to remove as admin: ")

    rewrite_file_data(ADMIN_USERS_FILE_DATA, {
        **file_data,
        "records": [
            user for user in (file_data.get("records") or [])
            if user["id"] != id
        ],
    })

    return None


def main():
    try:
        print("\niParkir CLI console")

        pin = input("\nEnter PIN to access the console menu: ")

        if pin != CLI_PIN:
            print("\nInvalid PIN")
            return

        print("\nWelcome to the console menu")

        while True:
            print("\nMenu:")
            print("1. Get Admin Users")
            print("2. Add Admin User")
            print("3. Remove Admin User")
            print("4. Exit")

            choice = input("\nEnter your choice (1/2/3/4): ")

            if choice == "1":
                get_admin_users()
            elif choice == "2":
                add_admin_users()
            elif choice == "3":
                remove_admin_users()
            elif choice == "4":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a valid option.")
    except:
        return None


if __name__ == "__main__":
    main()