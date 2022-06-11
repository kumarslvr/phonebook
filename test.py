from phonebook import phone
import time
mynew_phone = phone("manon")



def number_to_string(agrument):
    match agrument:
        case 1:
            mynew_phone.add_new_contact()
        case 2:
            mynew_phone.show_contact()
        case 3:
            mynew_phone.edit_contact()
        case default:
            print("invalid entry")

while True:

    print("press 1 to add new contact, press 2 to show contact, press 3 to edit an exisiting contact")
    choice= int(input())
    number_to_string(choice)