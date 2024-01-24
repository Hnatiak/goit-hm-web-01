from collections import UserDict
import pickle
import os
from record import Record

path_to_db = 'db.bin'

class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_contact(self, contact_name):
        contact_to_delete = self.data.get(contact_name)
        if contact_to_delete:
            del self.data[contact_name]
            return cprint('Contact deleted successfully', 'green')
        else:
            return cprint('Contact not found', 'red')

    def update_contact(self, name):
        if name in self.data:
            record = self.data[name]
            record.edit_record()
            return cprint('Contact updated successfully', 'green')
        else:
            return cprint('Contact not found', 'red')

    def write_data(self):
        with open(path_to_db, 'wb') as file:
            pickle.dump(self.data, file)

    def read_data(self):
        with open(path_to_db, 'rb') as file:
            self.data = pickle.load(file)

    def find(self, word_input):
        rset = set()
        for k, v in self.data.items():
            if k == word_input:
                rset.add(k)
                continue
            elif v.phones[0].value == word_input:
                rset.add(k)
        return list(rset)

    def __iter__(self):
        return self.iterator()

    def iterator(self, batch_size=1):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0

        while current_index < total_records:
            yield records[current_index:current_index + batch_size]
            current_index += batch_size

    def __next__(self):
        raise StopIteration
    
    
    
path_to_db = 'db.bin'
address_book = AddressBook()