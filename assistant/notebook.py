# from collections import UserDict
import os
import pickle
from prettytable import PrettyTable
from abstractclasses import AbstractNotebook


# the code defines a class called Field that encapsulates the value,
# and provides methods to get and set this value.
# The class also provides a string representation of the value.
class Field:

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Title(Field):
    pass


class Note(Field):
    pass


class Tag(Field):
    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other


# code defines a class that represents an entry with a title, note, and tag.
# The __str__ method makes it easy to print a record object.


class Record:

    def __init__(self, title, note, tag):
        self.title = title
        self.note = note
        self.tag = [tag]

    def __str__(self) -> str:
        return f'Title: {self.title}, Note: {self.note}, Tag: {self.tag}'


# This code defines a NoteBook class that inherits from the UserDict class.


class NoteBook(AbstractNotebook):
    # The add_record method takes a record parameter and adds it to the data attribute of the NoteBook object
    def add_record(self, record):
        self.data[record.title.value] = record

    def edit_record(self, title, new_note):
        self.data[title].note = new_note

    # The remove_record method takes a title parameter and
    # removes a record with that title from the data dictionary, if it exists.
    def remove_record(self, title):
        if title in self.data:
            del self.data[title]

    # The add_tag_to_record method takes a title and new_tag parameter and adds new_tag to the record's tag attribute
    def add_tag_to_record(self, title, new_tag):
        if title in self.data:
            record = self.data[title]
            record.tag.append(new_tag)
        else:
            raise KeyError(f"Record with key '{title}' not found in notebook")

    def delete_tag_from_record(self, title, rem_tag):
        self.data[title].tag.remove(rem_tag)

    def search_record_by_note(self, search_text):
        found_records = []
        for record in self.data.values():
            if search_text in str(record.title) or search_text in str(record.note):
                found_records.append(record)
        return found_records

    def search_record_by_tag(self, search_tag):
        found_records = []
        for record in self.data.values():
            if search_tag in str(record.tag):
                found_records.append(record)
        return found_records

    def sort_record_by_tag(self):
        sorted_records = list(self.data.values())
        sorted_records.sort(key=lambda note: [tag.value for tag in note.tag])
        return sorted_records

    def show_all_record(self):
        records = [record for record in self.data.values()]
        return records


file_name = 'NoteBook.bin'
file_path = os.path.expanduser("~\Documents")


def pretty_display(records):
    table = PrettyTable()
    table.field_names = ["Title", "Note", "Tags"]
    for record in records:
        table.add_row([record.title, record.note, ", ".join(tag.value for tag in record.tag)])
    print(str(table))


def write_file(self, filename=rf"{file_path}\{file_name}"):
    with open(filename, "wb") as file:
        pickle.dump(self, file)


def read_file(filename=rf"{file_path}\{file_name}"):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data
    except (EOFError, FileNotFoundError):
        data = NoteBook()
        return data


def add_note(notebook):
    input_title = input("Enter note title: >>> ")
    while input_title == "":
        input_title = input(
            "The note must have a title, please enter the title: >>> ")

    input_note = input("Enter note text: >>> ")
    while input_note == "":
        input_note = input(
            "Notes should not be empty, please enter the text: >>> ")

    input_tag = input("Enter a tag (keyword) to the note: >>> ")
    while input_tag == "":
        input_tag = input("Enter at least one tag: >>> ")

    input_record = Record(Title(input_title), Note(input_note), Tag(input_tag))
    notebook.add_record(input_record)
    write_file(notebook)
    pretty_display([input_record])
    return f'Note created successfully'


def edit_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Select the name of the note whose text needs to be changed:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        pretty_display(notebook[input_title])
        print("Enter new note text: >>> ")
        input_note = input()
        notebook.edit_record(input_title, input_note)
        write_file(notebook)
        pretty_display(notebook[input_title])
        return f"Note text '{input_title}' changed successfully"
    else:
        return f"Note with title '{input_title}' not found"


def add_tag(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Select the name of the note to which you want to add a tag:\n{titles_list}")
    input_title = input()

    if input_title in titles_list:
        print('Enter a new tag: ')
        new_tag = Tag(input())
        notebook.add_tag_to_record(input_title, new_tag)
        write_file(notebook)
        pretty_display([notebook[input_title]])
        return f"The tag '{new_tag}' was added"


def delete_tag_from_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Select the name of the note from which you want to remove the tag:\n{titles_list}")
    input_title = input(">>> ")
    if input_title in notebook:
        pretty_display([notebook[input_title]])
        print("Enter the tag you want to remove: >>>")
        input_tag = input()
        record = notebook[input_title]
        if record.tag:
            for tag in record.tag:
                if tag == input_tag:
                    notebook.delete_tag_from_record(input_title, input_tag)
                    write_file(notebook)
                    pretty_display([notebook[input_title]])
                    return f"Tag '{input_tag}' removed from note '{input_title}'"
        return f"Tag '{input_tag}' not found in note '{input_title}'"
    else:
        return f"Note '{input_title}' has no tags"


def search_note_by_text(notebook):
    print("Enter the fragment of text that we will search for: >>> ")
    search_text = input()
    found_records = notebook.search_record_by_note(search_text)

    if found_records:
        print(f'The text "{search_text}" was found in the following notes:')
        return pretty_display(found_records)
    else:
        return f'Sorry, nothing found'


def search_note_by_tag(notebook):
    print("Enter the tag we will search for: >>> ")
    search_tag = input()
    found_records = notebook.search_record_by_tag(search_tag)
    if found_records:
        print(f'The {search_tag} tag was found in the following notes:')
        return pretty_display(found_records)
    else:
        return f'Sorry, nothing found'


def sort_note_by_tag(notebook):
    sorted_records = notebook.sort_record_by_tag()

    if not sorted_records:
        return 'No records'
    else:
        return pretty_display(sorted_records)


def show_all_note(notebook):
    if not notebook:
        return 'No records'
    records = notebook.show_all_record()
    return pretty_display(records)


def delete_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Select the name of the note to be deleted:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        notebook.remove_record(input_title)
        write_file(notebook)
        return f"The note with the title '{input_title}' has been deleted"
    else:
        return f"Notes with title '{input_title}' unfortunately not found"


def exiting(notebook):
    write_file(notebook)
    return 'Goodbye'


def unknown_command():
    return "I don't know such a command, try again!"


def helper(*args):
    return r"""
    A smart notebook welcomes you!
    +---------------------------------------------------------+
    |               List of available commands:               |
    +---------------------------------------------------------+
    |"help" List of available commands:                       |
    +---------------------------------------------------------+
    |"add note" Creates a new note (name, text, tag)          |
    +---------------------------------------------------------+
    |"add tag" Adds a new tag to the note                     |
    +---------------------------------------------------------+                  
    |"delete tag" Removes the specified tag from the note     |
    +---------------------------------------------------------+
    |"edit note" Replaces the note text                       |
    +---------------------------------------------------------+
    |"show all note" Displays all entries in the console      |
    +---------------------------------------------------------+
    |"search by text" Finds notes by text                     |
    +---------------------------------------------------------+
    |"search by tag" Finds notes by tag                       |
    +---------------------------------------------------------+
    |"sort by tag" Sorts notes by tag                         |
    +---------------------------------------------------------+
    |"delete note" Deletes a note by name                     |
    +---------------------------------------------------------+
    |"exit" Exit the application                              |
    +---------------------------------------------------------+
    """


COMMANDS = {
    helper: ['help'],
    add_note: ['add note'],
    add_tag: ['add tag'],
    delete_tag_from_note: ['delete tag'],
    edit_note: ['edit note'],
    show_all_note: ['show all note'],
    search_note_by_text: ['search by text'],
    search_note_by_tag: ['search by tag'],
    sort_note_by_tag: ['sort by tag'],
    delete_note: ['delete note'],
    exiting: ['exit']
}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    notebook = read_file()
    print(helper())
    while True:
        user_command = input("Enter the command: >>> ")
        if user_command == "exit":
            return f"Exit"
        command, data = command_parser(user_command)
        print(command(notebook))

        if command is exiting:
            break


if __name__ == "__main__":
    main()
