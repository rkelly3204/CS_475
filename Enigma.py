#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Ryan Kelly
#5/27/2019
#HW3

class Enigma:
     
     #Setting up the Enigma machine 

     def __init__(self):
         self.numcycles = 0
         self.rotors = []
        
         #Made my enigma machine with 5 Rotors
         # 1-5
         self.rotorsettings = [("Rotor5", 0),
                             ("Rotor4", 0),
                             ("Rotor3", 0),
                             ("Rotor2", 0),
                             ("Rotor1", 0)]

         self.reflectorsetting = "A"
         self.plugboardsetting = []

         self.plugboard = Plugboard(self.plugboardsetting)

         for i in range(len(self.rotorsettings)):
             self.rotors.append(Rotor(self.rotorsettings[i]))

         self.reflector = Reflector(self.reflectorsetting)

     #Printing out the settings of the enigma machine 
     def print_setup(self):

         print()
         print("Rotor sequence: (right to left)")
         print("-------------------------------")

         for r in self.rotors:
             print(r.setting, "\t", r.sequence)

         print()
         print("Reflector sequence:")
         print("-------------------")
         print(self.reflector.setting+": "+self.reflector.sequence, "\n")

         print("Plugboard settings:")
         print("-------------------")
         print(self.plugboard.mapping, "\n")

     #Reset the Enigma machine back to its orginal settings   
     def reset(self):

         self.numcycles = 0
         for r in self.rotors:
             r.reset()
     #Encodes everything to uppercase letters    
     def encode(self, c):
         c = c.upper()
         self.rotors[0].rotate()

         if self.rotors[1].base[0] in self.rotors[1].notch:
             self.rotors[1].rotate()

         for i in range(len(self.rotors) - 1):
             if(self.rotors[i].turnover):
                 self.rotors[i].turnover = False
                 self.rotors[i + 1].rotate()

         index = self.plugboard.forward(c)

         for r in self.rotors:
             index = r.forward(index)

         index = self.reflector.forward(index)

         for r in reversed(self.rotors):
             index = r.reverse(index)

         c = self.plugboard.reverse(index)

         return c

#The creation of the rotors
class Rotor:

     def __init__(self, settings):
        
         self.setting = settings[0]
         self.ringoffset = settings[1]
         self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
         self.settings = {
                 "Rotor1":    ["2YZ01AWIPKSN3TERMUC5V6X7FQOL48GD9BJH ", ["S"], ["Q"]],
                 "Rotor2":   ["0LX128HB3NROKDT7C6PIVJ 4AUWME95QSZGYF", ["F"], ["E"]],
                 "Rotor3":   ["0NROKDT7C6PIVJ 4AUWME95QSZGYFLX128HB3", ["E"], ["G"]],
                 "Rotor4":   ["0LX128HB3C6PIVJ 4AUWME95QSZGYFNROKDT7", ["Z"], ["Y"]],
                 "Rotor5":  ["35HEFGDQ8M2KLJNSUWOVRXZ CI9T7BPA01Y64", ["W"], ["V"]]}

         self.turnovers = self.settings[self.setting][1]
         self.notch = self.settings[self.setting][2]
         self.sequence = None
         self.turnover = False
         self.reset()

     #Resets the Rotors
     def reset(self):
         self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
         self.sequence = self.sequence_settings()
         self.ring_settings()

     def sequence_settings(self):
         return self.settings[self.setting][0]

     def ring_settings(self):
         for _ in range(self.ringoffset):
             self.rotate()

     def forward(self, index):
         return self.base.index(self.sequence[index])

     def reverse(self, index):
         return self.sequence.index(self.base[index])

     def rotate(self):
         self.base = self.base[1:] + self.base[:1]
         self.sequence = self.sequence[1:] + self.sequence[:1]

         if(self.base[0] in self.turnovers):
             self.turnover = True

#Uses the reflector to rearange the letter passing through
#kept this relativly simple by just placing the base charset
#backwards

class Reflector:

     def __init__(self, setting):
         self.setting = setting
         self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
         self.settings = {"A":   " 9876543210ZYXWVUTSRQPONMLKJIHGFEDCBA"}

         self.sequence = self.sequence_settings()

     def sequence_settings(self):
         return self.settings[self.setting]

     def forward(self, index):
         """ Passthrough the reflector. """
         return self.sequence.index(self.base[index])

#Swaps letters at then end with the corresponding values on the
#plugboard.
class Plugboard:
     def __init__(self, mapping):
        
         self.base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
         self.mapping = {'A': 'B', 'B': 'A', 'C': 'C', 'D': 'D', 
                         'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 
                         'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 
                         'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 
                         'Q': 'Q', 'R': 'V', 'S': 'S', 'T': 'T', 
                         'U': ' ', 'V': 'R', 'W': 'W', 'X': 'X', 
                         'Y': 'Y', 'Z': 'Z', '0': '0', '1': '1', 
                         '2': '2', '3': '3', '4': '4', '5': '5', 
                         '6': '6', '7': '7', '8': '8', '9': '9', 
                         ' ': 'U'}

         for m in mapping:
             self.mapping[m[0]] = m[1]
             self.mapping[m[1]] = m[0]

     def forward(self, c):
         return self.base.index(self.mapping[c])

     def reverse(self, index):
         return self.mapping[self.base[index]]

#The menu for the Enigma machine.
def main():

     machine = Enigma()
     ciphertext = ""
     
     print("ENIGMA MACHINE")
     print("--------------")
     print("A: Test")
     print("B: Encrypt")
     print("C: Decrypt")
         
     menuIn = input("Enter your option above \n")
         
     if menuIn == "A":
        plaintext = "The Enigma machince of 2019 encrypts and decrypts"
        machine.print_setup()

        print("Plaintext: "+plaintext)
         
        for character in plaintext:
            ciphertext += machine.encode(character)

        print("Ciphertext: "+ciphertext)

        machine.reset()
        plaintext = ""
        for character in ciphertext:
            plaintext += machine.encode(character)

        print("Plaintext: "+plaintext, "\n")
             
     if menuIn == "B":
            plaintext = "THE ENIGMA MACHINCE OF 2019 ENCRYPTS AND DECRYPTS"
            machine.print_setup()

            print("Plaintext: "+plaintext)
         
            for character in plaintext:
                ciphertext += machine.encode(character)

            print("Ciphertext: "+ciphertext)
            
     if menuIn == "C":
            ciphertext = "CY5ZSP0P4RV2IP8AVZ04THY8Q7BEY20FH6B LLVD EVGRVTLW"
            machine.print_setup()  
            
            machine.reset()
            plaintext = ""
            for character in ciphertext:
                 plaintext += machine.encode(character)
            
            print("Ciphertext: "+ciphertext)
            print("Plaintext: "+plaintext, "\n")
            
if __name__ == '__main__':
    main()
                               
