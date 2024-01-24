from record import Record, Name, Phone, Birthday
from address_book import address_book
from termcolor import cprint

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return cprint("Contact not found", 'red')
        except ValueError as e:
            return str(e)
        except IndexError:
            return cprint("Insufficient arguments", 'red')
        except KeyboardInterrupt:
            return print(' ')

    return inner


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
        return cprint('Contact with the same name already exists', 'red')
    
    address_book.add_record(record)
    return cprint('Contact added successfully', 'green')

@input_error
def change(*args):
    name, *phones = args[0][1:]
    if name in address_book.data:
        record = address_book.data[name]
        for i, phone in enumerate(phones):
            record.edit_phone(record.phones[i], Phone(phone))
        return cprint('Contact updated successfully', 'green')
    else:
        return cprint('Contact not found', 'red')


@input_error
def phone(*args):
    name = args[0][1]
    if name in address_book.data:
        record = address_book.data[name]
        if record.phones:
            return ", ".join([phone.value for phone in record.phones])
        else:
            return cprint('No phone number found for this contact', 'red')
    else:
        return cprint('Contact not found', 'red')


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
                    result = cprint(f'{record.name.value.title()}, days to birthday = {record.days_to_birthday()}: {", ".join(phones)}', 'yellow')
                    print(result)
                print("---")

                choice = input("Press Enter to view the next page, or 'q' to exit: ")
                if choice.lower() == 'q':
                    break
        except StopIteration:
            pass
    else:
        return cprint('No contacts found', 'red')


def close(word):
    return word in STOP_WORDS


def find(word):
    lfind = address_book.find(word[1])
    return lfind if lfind else cprint('nothing found', 'red')


@input_error
def del_record(*args):
    contact_name = args[0][1]
    return address_book.delete_contact(contact_name)


def change_record(word):
    return address_book.update_contact(word[1])