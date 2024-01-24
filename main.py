from termcolor import cprint
from address_book import AddressBook, path_to_db
# from record import Record, Name, Phone, Birthday
from input_errors import phone, change, add, del_record, show_all, find, hello, close, address_book
import os
from abc import ABC, abstractmethod


OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show_all': show_all,
    'find': find,
    'del': del_record,
}


def get_handler(operator):
    return OPERATIONS.get(operator, lambda x: "I don't know such a command")


def input_text():
    text = 'Input some command: '
    return input(text).lower().split(' ')


class UIElement(ABC):
    @abstractmethod
    def show(self):
        pass


class ConsoleUIElement(UIElement):
    def __init__(self, content):
        self.content = content

    def show(self):
        print(self.content)

class ConsoleInterface:
    def __init__(self):
        self.elements = []
        self.show_help_message_flag = False

    def add_element(self, element):
        self.elements.append(element)

    def reset_elements(self):
        self.elements = []

    def show_help_message(self):
        if self.show_help_message_flag:
            help_message.show()
            self.show_help_message_flag = False

    def show(self):
        self.show_help_message()
        for element in self.elements:
            element.show()


class ConsoleGreeting(ConsoleUIElement):
    def __init__(self):
        super().__init__('----------------------- \nList of commands: \n"hello"\n'
                         '"add [name] [phone1] [phone2] ... [birth=birthday]"\n'
                         '"change [name] [new_phone1] [new_phone2] ..."\n'
                         '"phone [name]"\n"show_all"\n"del [name]"\n'
                         'New command "Find" if you want to find some records (find [search_word])')


def main():
    if os.path.exists(path_to_db):
        address_book.read_data()

    greeting = ConsoleGreeting()
    interface = ConsoleInterface()
    interface.add_element(greeting)

    cprint("Welcome to the Address Book App!", 'blue')

    while True:
        user_input = input_text()
        if len(user_input) > 0:
            command = user_input[0]
            if close(command):
                address_book.write_data()
                "Good bye!"
                break
            elif command == "help":
                interface.show_help = True
                interface.show()
            else:
                handler = OPERATIONS.get(command, lambda x: "I don't know such a command")
                result = handler(user_input)
                if result != "I don't know such a command":
                    output_element = ConsoleUIElement(result)
                    interface.add_element(output_element)
                interface.show()
                interface.reset_elements()


if __name__ == '__main__':
    main()