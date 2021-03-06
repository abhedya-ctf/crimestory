import os
import base64
import traceback
import pickle
from getpass import getpass
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES

class WeAreNeagan(object):
    SEED = 'mkhgts465wef4fwtdd'  # MAKE THIS YOUR OWN RANDOM STRING
    KP_FILE = './kfileNsxConfigVerfiy.p'
    SDB_FILE = './sdbfileNsxConfigVerify'
    PASSPHRASE_SIZE = 64  # 512-bit passphrase
    KEY_SIZE = 32  # 256-bit key
    BLOCK_SIZE = 16  # 16-bit blocks
    IV_SIZE = 16  # 128-bits to initialize
    SALT_SIZE = 8  # 64-bits of salt

    def __init__(self):
        try:
            with open(self.KP_FILE) as f:
                self.kp = f.read()
            if len(self.kp) == 0: raise IOError
        except IOError:
            with open(self.KP_FILE, 'w') as f:
                # Generate Random kp
                self.kp = os.urandom(self.PASSPHRASE_SIZE)
                f.write(base64.b64encode(self.kp))

                try:
                    # If the kp has to be regenerated, then the old data in the SDB file can no longer be used and should be removed
                    if os.path.exists(self.SDB_FILE):
                        os.remove(self.SDB_FILE)
                except:
                    print(traceback.format_exc())
                    print("There might be an error with permissions for the SDB_FILE {}".format(self.SDB_FILE))
        else:
            # decode from base64
            self.kp = base64.b64decode(self.kp)

        # Load or create SDB_FILE:
        try:
            with open(self.SDB_FILE) as f:
                self.sdb = pickle.load(f)
            # sdb will be a dictionary that will have key, value pairs
            if self.sdb == {}: raise IOError
        except (IOError, EOFError):
            self.sdb = {}
            with open(self.SDB_FILE, 'w') as f:
                pickle.dump(self.sdb, f)

    def getSaltForPname(self, pname):
        # Salt is generated as the hash of the key with it's own salt acting like a seed value
        return PBKDF2(pname, self.SEED).read(self.SALT_SIZE)

    # Encrypt Password
    def encrypt(self, pname, p):
' Pad p, then encrypt it with a new, randomly initialised cipher. 
        Will not preserve trailing whitespace in plaintext!'''

        # Initialise Cipher Randomly
        initVector = os.urandom(self.IV_SIZE)

        salt = self.getSaltForPname(pname)

        # Prepare cipher key that will be used to encrypt and decrypt
        k = PBKDF2(self.kp, salt).read(self.KEY_SIZE)

        # Create cipher that will be used to encrypt the data
        cipher = AES.new(k, AES.MODE_CBC, initVector)

        # Pad and encrypt
        self.sdb[pname] = initVector + cipher.encrypt(p + ' '*(self.BLOCK_SIZE - (len(p) % self.BLOCK_SIZE)))
        with open(self.SDB_FILE, 'w') as f:
            pickle.dump(self.sdb, f)

    # Decrypt Password
    def decrypt(self, pname):
' Reconstruct the cipher object and decrypt. Will not preserve trailing whitespace in the retrieved value!'''
        self.sdb[pname]
        salt = self.getSaltForPname(pname)

        # Recreate an identical cipher key:
        key = PBKDF2(self.kp, salt).read(self.KEY_SIZE)

        # Get initVector (salt) that was concatenated into the encrypted Data stored in the SDB_FILE
        initVector = self.sdb[pname][:self.IV_SIZE]

        # Get only the data you want to decrypt
        encryptedData = self.sdb[pname][self.IV_SIZE:]

        # Recreate cipher
        cipher = AES.new(key, AES.MODE_CBC, initVector)

        # Decrypt and depad
        return cipher.decrypt(encryptedData).rstrip(' ')


if __name__ == '__main__':
    pname = raw_input("Please Enter Username: ")
    p = getpass("Please enter a value for {}: ".format(pname))
    p2 = getpass("To verfiy, Please renter the value for {}: ".format(pname))
    while p != p2:
        print('Values DO NOT match')
        p = getpass("Please enter a value for {}: ".format(pname))
        p2 = getpass("To verfiy, Please reenter the value for {}: ".format(pname))
    johnny = WeAreNeagan()
    # Encrypting and Storing
    johnny.encrypt(pname, p)
    print('Encryption Complete!')
    # print('Your password is...')
    # print johnny.decrypt(pname)
