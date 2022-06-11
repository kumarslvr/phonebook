

import phonenumbers
from phonenumbers import geocoder
from datetime import datetime
import json


class phone:

    def __init__(self, name):
        self.name = name
        
        try:
            with open(self.name+'.json') as f:
                self.phone_data = json.load(f)
        except:
            with open(self.name+'.json', 'w') as f:
                phone_contact = {self.name:[]}
                json.dump(phone_contact, f, indent = 2)
            with open(self.name+'.json') as f:
                self.phone_data = json.load(f)


    def add_new_contact(self):
        '''Gets name, number and date of birth of contacts user wants to add
        and add it to the exisiting contacts.'''

        print("enter the name of the person you would like to add")
        name = input()
        print("enter the phone number eg: +919385943902")
        number = input()
        print("enter their date of birth in the format dd-mm-yyyy")
        date = input()

        my_number = phonenumbers.parse(number, "CH")
        country = geocoder.description_for_number(my_number, "en")
        if country != "":
            try:
                res = bool(datetime.strptime(date, "%d-%m-%Y"))
            except:
                print("please try again with the date format 'dd-mm-yyyy' ")
                return

            self.phone_data[self.name].append(
                {"name": name, "date of birth": date, "phone numbers": [number]})

            with open(self.name+'.json', 'w') as f:
                json.dump(self.phone_data, f, indent=2)

        else:
            print("not a valid phone number")

    def show_contact(self):   
        try:
            for person in self.phone_data[self.name]:
                print("Name: {}, Date of birth: {}, Phone number: {}".format(person['name'], person['date of birth'],person['phone numbers']))
        except:
            print("no contact found on {}'s phone".format(self.name))

    def edit_contact(self):
        '''allows user to change exisiting contact's name, date of birth, add, remove or replace phone number.'''

        print("enter the name of the person you want to change details to")
        name = input()
        name_found = False
        for person in self.phone_data[self.name]:
            if person['name'] == name:
                name_found = True
                print("enter 'name' if you want to change the name of the contact, enter 'date' if you want to change the date of birth of the user and enter 'number' if you want to change or add phone number")
                choice = input()
                if choice == 'name':
                    print('enter the new name')
                    new_name = input()
                    person['name'] = new_name
                elif choice == 'date':
                    print('please enter the date')
                    date = input()

                    try:
                        res = bool(datetime.strptime(date, "%d-%m-%Y"))
                    except:
                        print("please try again with valid date format 'dd-mm-yyyyKum' ")
                        return
                    person['date of birth'] = date

                elif choice == 'number':
                    print("enter 'add' to add new number, 'delete' to delete a number and 'replace' to replace an exisiting number")
                    add_replace = input()
                    if add_replace == 'add':
                        print("please enter the number you want to add to the list")
                    elif add_replace == 'replace':
                        print("please enter the old number you want to replace")
                    elif add_replace == 'delete':
                        print("enter number you want to delete")
                    else: 
                        print("invalid input")
                        return

                    number_to_be_replaced = input()    #common input for adding new number or getting old number to be replaced  
                    
                    try: 
                        my_number = phonenumbers.parse(number_to_be_replaced, "CH")
                        country = geocoder.description_for_number(my_number, "en")
                    except:
                        print("number not valid")
                        return

                    if country != "" and add_replace == 'add':    
                        person['phone numbers'].append(number_to_be_replaced)   #adding a new number to exisiting phonelist

                    elif country != "" and add_replace == 'delete':
                        if number_to_be_replaced in person['phone numbers']:
                            person['phone numbers'].remove(number_to_be_replaced)
                        else:
                            print("number not found")

                    elif country != "" and add_replace == 'replace':
                        
                        print("enter the new number")
                        new_number = input()
                        try:
                            my_number = phonenumbers.parse(new_number, "CH")
                            country = geocoder.description_for_number(my_number, "en")   #if the number is not valid geocoder will return empty string
                        except:
                            print("number not valid")

                        if country != "" :          
                            for person in self.phone_data[self.name]:
                                if person['name'] == name:
                                    for n in range (len(person['phone numbers'])):
                                        if person['phone numbers'][n] == number_to_be_replaced:     
                                            person['phone numbers'][n] = new_number                 #replacing phone number from the list

                        else:
                            print("not a valid number")
                            return
                    else:
                        print("invalid number or choice")
                        return
                else:
                    print("invalid entry")
                    return

        if name_found == True:
            with open(self.name+'.json', 'w') as f:
                json.dump(self.phone_data, f, indent=2)
        else: 
            print("name not found")


    def delete_contact(self, name_to_be_deleted):
        '''takes the name of the person that needs to be removed and removes them from 
        the contacts of the user.'''

        person_exsist = False
        for person in self.phone_data[self.name]:
            if person['name'] == name_to_be_deleted:
                person_exsist = True
                index = self.phone_data[self.name].index(person)
                self.phone_data[self.name].pop(index)

        if person_exsist == False:
            print("contact not found")
        else:
            with open(self.name+'.json', 'w') as f:
                json.dump(self.phone_data, f, indent=2)



    def import_contact(self, filename):
        '''takes the name of json file as a parameter extracts the information from it and 
        add it to the exisitng contacts of the user.'''

        with open(filename+'.json') as f:
            old_phone_data = json.load(f)
        # print(old_phone_data)

        for key in old_phone_data.keys():
            for person in old_phone_data[key]:

                self.phone_data[self.name].append(
                    {"name": person['name'], "date of birth": person['date of birth'], "phone numbers": person['phone numbers']})

        with open(self.name+'.json', 'w') as f:
            json.dump(self.phone_data, f, indent=2)
            
            
         
            


 



# myphone = phone('kumar')
# myphone.add_new_contact()
# myphone.edit_contact()
# myphone.show_contact()
