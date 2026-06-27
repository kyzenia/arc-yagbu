def main():
    main_menu()
    main_menu_selection()

def main_menu():
    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("#                                                       #")
    print("#                      Yagbu v0.1.0                     #")
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
                uKey = int(input("Enter your key (positive integer): "))
            except:
                print("\nPlease enter a valid seed/key!")
                loop2 = 1
            else:
                if uKey < 0:
                    uKey = (uKey * (-1))
                uKey = str(uKey)
                userKey = [num for num in uKey]
                loop2 = 0
        encrypt_decrypt_handler(readFile(userFile), userKey, userSeed, userChoice, userFile)
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
                uKey = int(input("Enter your key (positive integer): "))
            except:
                print("\nPlease enter a valid seed/key!")
                loop3 = 1
            else:
                if uKey < 0:
                    uKey = (uKey * (-1))
                uKey = str(uKey)
                userKey = [num for num in uKey]
                loop3 = 0
        encrypt_decrypt_handler(readFile(userFile), userKey, userSeed, userChoice, userFile)
    else:
        credits()
        input("Have a great day!\nPlease press enter to exit the program...")

def encrypt_decrypt_handler(data, userKey, userSeed, userChoice, userFile):
    if userChoice == 1:
        alfabetas, rev_alfabetas = key_gen(userSeed)
        encrypt(userKey, alfabetas, rev_alfabetas, data, userFile)
        print(f'''\nEncryption complete. Please check "{userFile}.yagbu"''')
        main()
    else:
        list_char, list_num = assign(data, userKey)
        alfabetas, rev_alfabetas = key_gen(userSeed)
        decrypt(list_char, list_num, alfabetas, rev_alfabetas, userFile)
        print(f'''\nDecryption complete. Please check "{userFile.removesuffix(".yagbu")}"''')
        main()

def encrypt(userKey, alfabetas, rev_alfabetas, data, userFile):
    data_ready, pre_list_char = [], []
    post_list_num = assignNum(data, userKey)
    for char in data:
        pre_list_char.append(char)
    for i in range(len(pre_list_char)):
        data_ready.append(rev_alfabetas[int(post_list_num[i])][alfabetas[0].get(pre_list_char[i])])
    data_ready = "".join(data_ready)
    file = open(f"{userFile}.yagbu", "wb")
    file.write(bytes.fromhex(data_ready))
    file.close()
    from pathlib import Path
    file = Path(userFile)
    if file.exists():
        file.unlink()

def decrypt(pre_list_char, pre_list_num, alfabetas, rev_alfabetas, userFile):
    data_ready = []
    for i in range(len(pre_list_char)):
        data_ready.append(rev_alfabetas[0].get(alfabetas[int(pre_list_num[i])].get(pre_list_char[i])))
    data_ready = "".join(data_ready)
    file = open(userFile.removesuffix(".yagbu"), "wb")
    file.write(bytes.fromhex(data_ready))
    file.close()
    from pathlib import Path
    file = Path(userFile)
    if file.exists():
        file.unlink()

def readFile(userFile):
    file = open(userFile, "rb")
    data = file.read().hex()
    file.close()
    return data

def assign(data, userKey):
    from itertools import cycle
    cycle_it = cycle(userKey)
    list_char,list_num = [],[]
    for char in data:
        num = next(cycle_it)
        list_char.append(char)
        list_num.append(num)
    return list_char, list_num

def assignNum(data, userKey):
    from itertools import cycle
    cycle_it = cycle(userKey)
    list_num = []
    for char in data:
        num = next(cycle_it)
        list_num.append(num)
    return list_num

def key_gen(userSeed):
    base = '''0123456789abcdef'''
    import random
    alfabetas, rev_alfabetas = [], []
    list_char = list(base)
    dict_alfabeta = {key: item for item, key in enumerate(list_char)}
    alfabetas.append(dict_alfabeta)
    rev_dict_alfabeta = {key: item for item, key in dict_alfabeta.items()}
    rev_alfabetas.append(rev_dict_alfabeta)
    for i in range(9):
        seedset = random.Random(int(userSeed)+i)
        seedset.shuffle(list_char)
        dict_alfabeta = {key: item for item, key in enumerate(list_char)}
        alfabetas.append(dict_alfabeta)
        rev_dict_alfabeta = {key: item for item, key in dict_alfabeta.items()}
        rev_alfabetas.append(rev_dict_alfabeta)
    alfabetas, rev_alfabetas = tuple(alfabetas), tuple(rev_alfabetas)
    return alfabetas, rev_alfabetas

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