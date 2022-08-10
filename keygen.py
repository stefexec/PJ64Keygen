import socket
import os
import winreg
import hashlib
import zlib
import time


def OtherMd5(input_data):

    md5_hash = hashlib.md5()
    data = input_data
    md5_hash.update(data)
    ergebnis_md5 = md5_hash.digest()
    print("MD5:")
    ergebnis_klein = ergebnis_md5.hex()
    ergebnis = ergebnis_klein.upper()
    print(ergebnis + '\n')

    return ergebnis


def GenerateMachineID():

    ComputerName = socket.gethostname()

    # Rechner GUID aus Registry holen
    path = winreg.HKEY_LOCAL_MACHINE
    OpenKey = winreg.OpenKeyEx(path, r"SOFTWARE\\Microsoft\\Cryptography")
    Key = winreg.QueryValueEx(OpenKey, "MachineGuid")

    MachineGUID = Key[0]

    # HDD Seriennummer rausfinden
    HDDSerialNumber = os.stat("C:").st_dev

    # zusammenklatschen die Scheiße
    MachineID = (str(ComputerName) + "." + str(HDDSerialNumber) + "d." + str(MachineGUID))

    # Fertig?
    print('\n' + "##################################################################################")
    print("Your generated Machine ID:")
    print(MachineID)
    print("##################################################################################" + '\n')
    return MachineID

def CreateRegfile(key_data):

    print()
    print("Creating your .reg file now!")
    print()

    print(key_data)

    key_split = ",".join([key_data[i:i+2] for i in range(0, len(key_data), 2)])

    print(key_split)

    ln1 = key_split[:66] + '\\'
    ln2 = key_split[66:141] + '\\'
    ln3 = key_split[141:216] + '\\'
    ln4 = key_split[216:263]

    print(ln1)
    print(ln2)
    print(ln3)
    print(ln4)

    with open('pj64_keyfile.reg', 'w') as kf:
        kf.write('Windows Registry Editor Version 5.00' + '\n'
                 + '\n'
                 + r'[HKEY_CURRENT_USER\SOFTWARE\Project64]' + '\n'
                 + '"user"=hex:' + ln1 + '\n' + "  "
                 + ln2 + '\n' + "  "
                 + ln3 + '\n' + "  "
                 + ln4 + '\n' + '\n')


def CreateKey():

    MachineID = GenerateMachineID()

    code = ''
    email = ''

    Code = code.ljust(300, '\x00')
    Email = email.ljust(300, '\x00')
    Name = os.getlogin().ljust(300, '\x00')
    MachineID_MD5 = OtherMd5(MachineID.encode()).ljust(300, '\x00')
    RunCount = 0
    LastUpdated = 0
    LastShown = 0
    Validated = True

    Code_ENC = bytes(Code.encode())
    Email_ENC = bytes(Email.encode())
    MachineID_MD5_ENC = bytes(MachineID_MD5.encode())
    Name_ENC = bytes(Name.encode())

    langesding = (Code_ENC
                  + Email_ENC
                  + Name_ENC
                  + MachineID_MD5_ENC
                  + RunCount.to_bytes(8, byteorder='little')
                  + LastUpdated.to_bytes(8, byteorder='little')
                  + LastShown.to_bytes(8, byteorder='little')
                  + Validated.to_bytes(8, byteorder='little')
                  )

    langesding_DEC = langesding.decode()
    Hash = OtherMd5(langesding_DEC.encode())

    RegKey = langesding_DEC + Hash
    print("Raw key:")
    print(RegKey + '\n')

    RegKey_compressed = zlib.compress(RegKey.encode(), 9)

    key_list = []

    final = ''

    for i in range(0, len(RegKey_compressed)):
        key_list.append((RegKey_compressed[i] ^ 0xAA))
        final = final + hex(key_list[i])[2:]

    print("Final compressed key:")
    print(final)

    time.sleep(2)

    CreateRegfile(final)


if __name__ == '__main__':

    CreateKey()

