import re  
from collections import UserDict  
from datetime import datetime, timedelta  


class Field:  
    def __init__(self, value):   
        self.value = value  

    def __str__(self):  
        return str(self.value)  
    

class Name(Field):  
    pass  


class Phone(Field):  
    def __init__(self, value):  
        # Перевіряємо, чи номер складається рівно з 10 цифр за допомогою регулярного виразу  
        if not bool(re.fullmatch(r"\d{10}", value)):  
            raise ValueError("Phone number must have exactly 10 digits.")  
        super().__init__(value)  


class Birthday(Field):  
    def __init__(self, value):  
        if value:  
            try:  
                # Перетворюємо рядок у об'єкт datetime  
                self.date = datetime.strptime(value, "%d.%m.%Y").date()  
            except ValueError:  
                raise ValueError("Invalid date format. Use DD.MM.YYYY")  
        else:  
            self.date = None  
    
    def __str__(self):  
        return self.date.strftime("%d.%m.%Y") if self.date else "No birthday"  


class Record:  
    def __init__(self, name):  
        self.name = Name(name)  
        self.phones = []  
        self.birthday = None  

    def add_phone(self, phone_number):  
        phone = Phone(phone_number)  
        self.phones.append(phone)  

    def remove_phone(self, phone_number):  
        self.phones = [phone for phone in self.phones if phone.value != phone_number]  

    def edit_phone(self, old_phone, new_phone):  
        for i, phone in enumerate(self.phones):  
            if phone.value == old_phone:  
                self.phones[i] = Phone(new_phone)  
                return True  
        return False  

    def find_phone(self, phone_number):  
        for phone in self.phones:  
            if phone.value == phone_number:  
                return phone  
        return None  
    
    def set_birthday(self, birthday_value):  
        self.birthday = Birthday(birthday_value)  
    
    def __str__(self):  
        phones = '; '.join(phone.value for phone in self.phones)  
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""  
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"  


class AddressBook(UserDict):  
    def add_record(self, record):  
        self.data[record.name.value] = record 
        print(f'record{record}') 

    def find(self, name):  
        return self.data.get(name)  

    def delete(self, name):  
        if name in self.data:  
            del self.data[name]  

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():  
            if record.birthday:  
                birthday_this_year = record.birthday.date.replace(year=current_date.year)  

                # Якщо день народження вже пройшов, беремо наступний рік  
                if birthday_this_year < current_date:  
                    birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)  

                # Різниця в днях між поточною датою і днем народження  
                difference_days = (birthday_this_year - current_date).days  
                
                # Ініціюємо congratulation_date  
                congratulation_date = None  

                # Якщо день народження на наступному тижні (включаючи сьогодні)  
                if 0 <= difference_days <= 7:  
                    congratulation_date = birthday_this_year  

                    # Якщо день народження випадає на вихідні (субота або неділя)  
                    if congratulation_date.weekday() == 5:  # Субота  
                        congratulation_date += timedelta(days=2)  
                    elif congratulation_date.weekday() == 6:  # Неділя  
                        congratulation_date += timedelta(days=1)  

                    # Додаємо до списку тільки якщо congratulation_date було встановлено   
                    upcoming_birthdays.append((record.name.value, congratulation_date.strftime("%d.%m.%Y"))) 
                    # print(f'upcoming_birthdays{upcoming_birthdays}')
                    
        return upcoming_birthdays  

        









if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.set_birthday("21.11.1987")

    bill_record = Record("Bill")
    bill_record.add_phone("1234567890")
    bill_record.set_birthday("02.11.1988")

    tom_record = Record("Tom")
    tom_record.add_phone("1234567890")
    tom_record.set_birthday("21.12.1980")

    kris_record = Record("Kris")
    kris_record.add_phone("1234567890")
    kris_record.set_birthday("21.09.1981")

    sara_record = Record("Sara")
    sara_record.add_phone("1234567890")
    sara_record.set_birthday("21.08.1982")

    # Додавання запису John до адресної книги
    book.add_record(john_record)
    book.add_record(bill_record)
    book.add_record(tom_record)
    book.add_record(kris_record)
    book.add_record(sara_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items(): 
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    book.get_upcoming_birthdays(record)



