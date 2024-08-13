from collections import UserDict
import re
from datetime import datetime
from upcoming_birthdays import get_upcoming_birthdays
import pickle


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits long.")
        super().__init__(value)

    def validate(self, value):
        return re.fullmatch(r'\d{10}', value) is not None


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = self.validate(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def validate(self, value):
        try:
            # Attempt to parse the date
            return datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Address:
    def __init__(self, street: str, city: str, state: str, zip_code: str):
        self.street = street  
        self.city = city  
        self.state = state  
        self.zip_code = zip_code
        
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None 




    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = Phone(phone)  # Validate phone before removal
        self.phones = [p for p in self.phones if p.value != phone_obj.value]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        phone_obj = Phone(phone)  # Validate phone before finding
        for p in self.phones:
            if p.value == phone_obj.value:
                return p.value
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, street, city, state, zip_code):
        self.address = Address(street, city, state, zip_code)    

    def __str__(self):
        phone_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        address_str = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{birthday_str}{address_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def upcoming_birthdays(self):
        return get_upcoming_birthdays(self)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Insufficient arguments provided."
        except Exception as e:
            return str(e)

    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"Phones for {name}: {phones}"
    return "Contact not found."


@input_error
def show_all_contacts(book: AddressBook):
    if book.data:
        return '\n'.join(str(record) for record in book.data.values())
    return "Address book is empty."


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"Birthday for {name}: {record.birthday}"
        return "Birthday not set."
    return "Contact not found."


@input_error
def birthdays(args, book: AddressBook):
    this_week_info, next_week_info = book.upcoming_birthdays()
    return f"{this_week_info}\n{next_week_info}"

@input_error  
def add_contact(args, book: AddressBook):
    name, phone, *address_args = args  
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    if address_args:
        street, city, state, zip_code = address_args  
        record.add_address(street, city, state, zip_code)
    return message
def add_address(args, book: AddressBook):
    name, street, city, state, zip_code = args  
    record = book.find(name)
    if record:
        record.add_address(street, city, state, zip_code)
        return "Address added."
    return "Contact not found." 

def parse_input(user_input):
    return user_input.strip().split()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "add-address":
              print(add_address(args, book)) 

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
