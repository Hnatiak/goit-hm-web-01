from record import Record, Name, Phone, Birthday
from address_book import AddressBook
from termcolor import cprint

STOP_WORDS = ["good bye", "close", "exit"]
address_book = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Insufficient arguments"
        except KeyboardInterrupt:
            return print(' ')

    return inner


def hello(*args):
    return "How can I help you?"

@input_error
def add(*args):
    name, *phones = args[0][1:]
    record = Record(name)
    for item in phones:
        if item.startswith("birth="):
            birthday_value = item.split("=")[1]
            record.birthday = Birthday(birthday_value)
        else:
            record.add_phone(Phone(item))
            
    if name in address_book.data:
        return 'Contact with the same name already exists'
    
    address_book.add_record(record)
    return 'Contact added successfully'

@input_error
def change(*args):
    name, *phones = args[0][1:]
    if name in address_book.data:
        record = address_book.data[name]
        for i, phone in enumerate(phones):
            record.edit_phone(record.phones[i], Phone(phone))
        return 'Contact updated successfully'
    else:
        return 'Contact not found'


@input_error
def phone(*args):
    name = args[0][1]
    if name in address_book.data:
        record = address_book.data[name]
        if record.phones:
            return ", ".join([phone.value for phone in record.phones])
        else:
            return 'No phone number found for this contact'
    else:
        return 'Contact not found'


@input_error
def show_all(*args):
    if address_book.data:
        batch_size = 2
        iterator = address_book.iterator(batch_size)

        try:
            while True:
                batch = next(iterator)
                for record in batch:
                    phones = [phone.value for phone in record.phones]
                    result = f'{record.name.value.title()}, days to birthday = {record.days_to_birthday()}: {", ".join(phones)}'
                    print(result)
                print("---")

                choice = input("Press Enter to view the next page, or 'q' to exit: ")
                if choice.lower() == 'q':
                    break
        except StopIteration:
            pass
    else:
        return 'No contacts found'


def close(word):
    return word in STOP_WORDS


def find(word):
    lfind = address_book.find(word[1])
    return lfind if lfind else 'nothing found'


@input_error
def del_record(*args):
    contact_name = args[0][1]
    return address_book.delete_contact(contact_name)


def change_record(word):
    return address_book.update_contact(word[1])