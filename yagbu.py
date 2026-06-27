import random
from pathlib import Path
from itertools import cycle

def main():
    main_menu()
    main_menu_selection()

def main_menu():
    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("#                                                       #")
    print("#                      Yagbu v0.2.0                     #")
    print("#                                                       #")
    print("#   Please select among available options below (1-3):  #")
    print("#                                                       #")
    print("#                   1) Encrypt File                     #")
    print("#                   2) Decrypt File                     #")
    print("#                   3) Exit                             #")
    print("#                                                       #")
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

def main_menu_selection():
    loop, loop1, loop2, loop3, loopF, userChoice = 1, 1, 1, 1, 1, None
    while loop == 1:
        try:
            while loop1 == 1:
                userChoice = int(input("Your selection: "))
                if userChoice < 1 or userChoice > 3:
                    print("\nPlease enter a valid selection!\n")
                    loop1 = 1
                else:
                    loop1 = 0
        except:
            print("\nPlease enter a valid selection!\n")
            loop = 1
        else:
            loop = 0
    if userChoice == 1:
        while loop2 == 1:
            try:
                while loopF == 1:
                    from pathlib import Path
                    userFile = str(input("Enter your file's full name: ")).strip()
                    file = Path(userFile)
                    if file.exists():
                        loopF = 0
                    else:
                        print("\nFile not found! Check the file name.\n")
                        loopF = 1
                userSeed = int(input("Enter your seed (integer): "))
                userKey = int(input("Enter your key (positive integer): "))
            except:
                print("\nPlease enter a valid seed/key!")
                loop2 = 1
            else:
                if userKey < 0:
                    userKey = (userKey * (-1))
                userKey = [int(i) for i in str(userKey)]
                loop2 = 0
        encrypt_decrypt_handler(read_file(userFile), userKey, userSeed, userChoice, userFile)
    elif userChoice == 2:
        while loop3 == 1:
            try:
                while loopF == 1:
                    from pathlib import Path
                    userFile = str(input("Enter your file's full name: ")).strip() + ".yagbu"
                    file = Path(userFile)
                    if file.exists():
                        loopF = 0
                    else:
                        print("\nFile not found! Check the file name.\n")
                        loopF = 1
                userSeed = int(input("Enter your seed (integer): "))
                userKey = int(input("Enter your key (positive integer): "))
            except:
                print("\nPlease enter a valid seed/key!")
                loop3 = 1
            else:
                if userKey < 0:
                    userKey = (userKey * (-1))
                userKey = [int(i) for i in str(userKey)]
                loop3 = 0
        encrypt_decrypt_handler(read_file(userFile), userKey, userSeed, userChoice, userFile)
    else:
        credits()
        input("Have a great day!\nPlease press enter to exit the program...")

def encrypt_decrypt_handler(data, userKey, userSeed, userChoice, userFile):
    if userChoice == 1:
        alfabetas, rev_alfabetas = key_gen(userSeed)
        encrypt(userKey, alfabetas, rev_alfabetas, data, userFile)
        credits()
        print(f'''Encryption complete. Please check "{userFile}.yagbu"\n''')
        input("Have a great day! Please press enter to exit the program...")
    else:
        alfabetas, rev_alfabetas = key_gen(userSeed)
        decrypt(userKey, alfabetas, rev_alfabetas, data, userFile)
        credits()
        print(f'''Decryption complete. Please check "{userFile.removesuffix(".yagbu")}"\n''')
        input("Have a great day! Please press enter to exit the program...")

def encrypt(userKey, alfabetas, rev_alfabetas, data, userFile):
    data_ready = "".join(rev_alfabetas[key][alfabetas[0][char]]for char, key in zip(data, cycle(userKey)))
    with open(f"{userFile}.yagbu", "wb") as file:
        file.write(bytes.fromhex(data_ready))
    file = Path(userFile)
    if file.exists():
        file.unlink()

def decrypt(userKey, alfabetas, rev_alfabetas, data, userFile):
    data_ready = "".join(rev_alfabetas[0][alfabetas[key][char]]for char, key in zip(data, cycle(userKey)))
    with open(userFile.removesuffix(".yagbu"), "wb") as file:
        file.write(bytes.fromhex(data_ready))
    file = Path(userFile)
    if file.exists():
        file.unlink()

def read_file(userFile):
    with open(userFile, "rb") as file:
        return file.read().hex()

def key_gen(userSeed):
    base = list('''0123456789abcdef''')
    alfabetas, rev_alfabetas = [], []
    dict_alfabeta = {key: item for item, key in enumerate(base)}
    alfabetas.append(dict_alfabeta)
    rev_alfabetas.append({key: item for item, key in dict_alfabeta.items()})
    for i in range(9):
        chars = base.copy()
        seedset = random.Random(int(userSeed)+i)
        seedset.shuffle(chars)
        dict_alfabeta = {key: item for item, key in enumerate(chars)}
        alfabetas.append(dict_alfabeta)
        rev_alfabetas.append({key: item for item, key in dict_alfabeta.items()})
    return tuple(alfabetas), tuple(rev_alfabetas)

def credits():
    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("#                                                       #")
    print("#                           #                           #")
    print("#                         #                             #")
    print("#                       #                               #")
    print("#                     #                                 #")
    print("#           #       #               #                   #")
    print("#           #     #               # #                   #")
    print("#           #   #               #   #   #               #")
    print("#           # #               #     # #                 #")
    print("#           #       #       #       #       #           #")
    print("#           # #       #           # #     #             #")
    print("#           #   #       #       #   #   #               #")
    print("#           #     #       #   #     # #                 #")
    print("#           #       #       #       #                   #")
    print("#                     #     #                           #")
    print("#                       #   #                           #")
    print("#                         # #                           #")
    print("#                           #                           #")
    print("#                                                       #")
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

if __name__ == '__main__':
    main()