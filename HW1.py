#!/usr/bin/env python3
#
#Ryan Kelly
#6/9/2019
#HW4

import time
import string
import random
from random import randint
import uuid
import hashlib
import sys

randomInt= randint(1,10)
hashlist = []
userIP = ["19216817","19216812","192168114"]

def menu():
    print("MENU:")
    print("--------------------------------")
    print("A) Connect to server: ")
    print("B) Add a authenticated IP: ")
    print("C) Exit the System: " )
    
    action = input("Enter Action: ")
    action = action.upper()
    
    if action == 'A':
        main()
        
    elif action == 'B':
        add_user()
        
    elif action == 'C':
        print("Exiting")
        sys.exit()
        
    else:
        print("Incorrect input, try again! \n")
        menu()

def pwd_generator(size=8, chars= string.ascii_uppercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex

    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + '.' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split('.')

    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def add_user():
    user = input("Enter an IP to pre-authenticate: \n")
    user = user.upper()
    user = user.strip(".")
    userIP.append(user)
    main()

def main():
    user_postive = False
    testIP = input("Enter an IP to verify authenicated user: \n")
    testIP = testIP.upper()
    testIP = testIP.strip(".")
    print(testIP)
    
    for index, item in enumerate(userIP):
        if item == testIP:
           user_postive = True
    
    if user_postive == True:
        
        pwd = pwd_generator() # Randomly Generated password
        print('Your Generated password: ' +pwd+'\n')
        hashlist.append(pwd)
        time.sleep(1) #Delay for program style
    
        hashed_password = hash_password(pwd) # hash the intial randomly genearted password
        hashlist.append(hashed_password) #appends the hash to a hashlist

        for i in range(randomInt):# hashes the hash bounded (0,10)
            hashed_password = hash_password(hashed_password)
            hashlist.append(hashed_password) # Appends the hash to hashlist
            #print('Hashed pasword: '+ hashed_password+'\n') #Prints the hashes 

        # The hash at the end of the list is the key for the hash before it and so 
        #on for the length of the list
        access = True;
        for n in reversed(hashlist):
            if len(hashlist) > 1:
                #Figure out how to only return Acess Granted if the whole list is true
                #else return false if list is not true
                if not check_password(n,hashlist[-2]):
                    access = False;
                
                del hashlist[-1]
        
        if access:
            print("--------------------------------")
            print('Access Granted')
            print("--------------------------------\n")
            menu()
        else:
            print("--------------------------------")
            print('Access Denied')
            print("--------------------------------\n")
            menu()
    else:
        print("User name is not found: ACESS DENIED \n")
        menu()
        
if __name__ == '__main__':
    menu()
