# Crypt0r-CLI - A Tool for simple keyfile-based scriptable file encryption & decryption
#
# Creation:    16.10.2019
# Last Update: 16.10.2019
#
#
# MIT License
#
# Copyright (c) 2019 by PiereLucas
# https://github.com/pierelucas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import shutil
import sys
import string
import random
from colorama import Fore, Style
from cryptography.fernet import Fernet
from argparse import ArgumentParser

# Use the import below when argparse kicks an exception
# Rename your argparse.py in argparse_shadow.py first. The file is in your Python Folder
# This Problem often happens under conda or venv env.
#from argparse_shadow import ArgumentParser

banner_txt = """
   ______                 __  ____             ________    ____
  / ____/______  ______  / /_/ __ \_____      / ____/ /   /  _/
 / /   / ___/ / / / __ \/ __/ / / / ___/_____/ /   / /    / /  
/ /___/ /  / /_/ / /_/ / /_/ /_/ / /  /_____/ /___/ /____/ /   
\____/_/   \__, / .___/\__/\____/_/         \____/_____/___/   
          /____/_/    Version 1.0     
          
          Coded by PiereLucas   |   github.com/pierelucas                                 
          """

parser = ArgumentParser(description=banner_txt)

parser.add_argument("gen", nargs="?", choices=["gen"], help="Generate a new keyfile and backup your old")
parser.add_argument("-encf", "--encryption-file", dest="encryption", metavar="Encryption", help="Encrypt File")
parser.add_argument("-decf", "--decryption-file", dest="decryption", metavar="Decryption", help="Decrypt File")

args = parser.parse_args()

class Crypt0rCLI():

    def __init__(self):

        # Argparse
        self.gen = args.gen
        self.enc = args.encryption
        self.dec = args.decryption

        # Crypt0r CLI
        self.key = None
        self.crypt = None
        self.file_path = None

    def out(self, *, mode):
        if mode == 'enc': return "Successfully encrypt file " + Fore.CYAN + self.file_path + Style.RESET_ALL
        if mode == 'dec': return "Successfully decrypt file " + Fore.CYAN + self.file_path + Style.RESET_ALL

    def rnd_str(self, stringlen=6):
        letters = string.ascii_lowercase + string.digits
        return "".join(random.choice(letters) for i in range(stringlen))

    def startup_check(self):
        if os.path.isfile("key.crypt"):
            _true = self.read_key()
            if _true: print("Key found » Key loaded")
        else:
            _true = self.gen_key()
            if _true: print("No key found » Key generated")
        return True

    def gen_key(self):
        self.key = Fernet.generate_key()
        self.crypt = Fernet(self.key)
        global backup_key, backup_path
        backup_key = False
        if os.path.isfile("key.crypt"):
            backup_key = True
            backup_path = "key_old_" + self.rnd_str() + ".crypt"
            shutil.move("key.crypt", backup_path)
        with open("key.crypt", 'wb') as f:
            f.write(self.key)
        if backup_key: return True, backup_path
        return True

    def read_key(self):
        with open("key.crypt", 'rb') as f:
            self.key = f.read()
            self.crypt = Fernet(self.key)
        return True

    def enc_file(self):
        with open(self.file_path, 'rb') as f:
            file_data = f.read()
        encrypted_data = self.crypt.encrypt(file_data)
        with open(self.file_path, 'wb') as f:
            f.write(encrypted_data)
            return True

    def dec_file(self):
        with open(self.file_path, 'rb') as f:
            file_data = f.read()
        decrypted_data = self.crypt.decrypt(file_data)
        with open(self.file_path, 'wb') as f:
            f.write(decrypted_data)
            return True

    def run(self):
        startup_true = self.startup_check()
        if startup_true: print(Fore.GREEN + "Startup Succesfully" + Style.RESET_ALL)
        else: sys.exit(0)

        if args.gen:
            _true, backup_path_ = self.gen_key()
            if _true:
                print("New Key Generated | Previous Key: " + Fore.CYAN + backup_path_ + Style.RESET_ALL)
                sys.exit(0)
        else: pass

        if args.encryption:
            self.file_path = self.enc
            enc_true = self.enc_file()
            if enc_true: print(self.out(mode='enc'))
        elif args.decryption:
            self.file_path = self.dec
            dec_true = self.dec_file()
            if dec_true: print(self.out(mode='dec'))
        else:
            print(Fore.RED + "Not ENOUGH Args!" + Style.RESET_ALL)
            sys.exit(0)


# TO BE CONTINUED ...

# Name Guard
if __name__ == "__main__":
    crypcli = Crypt0rCLI()
    crypcli.run()
