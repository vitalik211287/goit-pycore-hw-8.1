from error_handler import input_error
from adress_book import AddressBook, Record



@input_error
def add_contact(args, book: AddressBook):
    # Додає контакт до словника.
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
def change_contact(args, book: AddressBook):
    # Змінює номер телефону контакту в book.
    if len(args) < 2:
        return "Please provide both name and new phone number."
    name, new_phone = args
    record = book.find(name)
    if record is not None:
        # Заміна першого номера телефону на новий
        if record.phones:
            record.edit_phone(record.phones[0].value, new_phone)
        else:
            record.add_phone(new_phone)
        return f"Contact {name} updated."
    else:
        raise KeyError(f"Contact {name} not found.")


@input_error
def show_phone(args, book: AddressBook):  
    # Показує номер телефону для вказаного контакту.
    if len(args) < 1:
        return "Please provide a name." 
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(phone.value for phone in record.phones)
        return f"{name}'s phone numbers are: {phones}"
    else:
        return f"Contact {name} not found."
    

@input_error
def show_all(book: AddressBook): 
    # Показує всі контакти.  
    if book.data:
        return "Contacts:\n" + "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts found."
    
    
@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    
    if upcoming_birthdays:
        return "\n".join([f"{name}: {date}" for name, date in upcoming_birthdays])
    else:
        return "No birthdays within the upcoming week."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        return "Please provide a name." 
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday is on {record.birthday}"
        else:
            return f"No birthday set for {name}."
    else:
        return f"Contact '{name}' not found."
    


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Please provide both name and birthday in the format: [name] [DD.MM.YYYY]"
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record:
        try:
            record.set_birthday(birthday)
            return f"Birthday for {name} added successfully."
        except ValueError as e:
            return str(e)  # Виведе повідомлення про неправильний формат дати
    else:
        return f"Contact '{name}' not found."
   
