import random
from pathlib import Path
from itertools import cycle
DATA_CHUNKS = 1 * 64 * 1024

def main():
    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("#                                                       #")
    print("#                      Yagbu v1.2.0                     #")
    print("#                                                       #")
    print("#   Please select among available options below (1-3):  #")
    print("#                                                       #")
    print("#                   1) Encrypt File                     #")
    print("#                   2) Decrypt File                     #")
    print("#                   3) Exit                             #")
    print("#                                                       #")
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

    user_choice = get_user_choice()
    if user_choice == 3:
        credits()
        input("Have a great day!\nPlease press enter to exit the program...")
        return
    user_file = get_user_file(choice_encrypt=(user_choice == 1))
    user_seed, user_key = get_user_seed_and_key()
    alfabetas, rev_alfabetas = key_gen(user_seed)
    if user_choice == 1:
        if encrypt(user_key, alfabetas, rev_alfabetas, user_file) == True:
            credits()
            clean_up(user_file, 1)
            print(f'''Encryption complete. Please check "{user_file}.yagbu"\n''')
        else:
            credits()
            clean_up(user_file, 2)
            print("There has been a problem while encrypting. Encryption aborted.\n")
    elif user_choice == 2:
        if decrypt(user_key, alfabetas, rev_alfabetas, user_file) == True:
            credits()
            clean_up(user_file, 1)
            print(f'''Decryption complete. Please check "{user_file.removesuffix(".yagbu")}"\n''')
        else:
            credits()
            clean_up(user_file, 3)
            print("There has been a problem while decrypting. Decrypting aborted.\n")
    input("Have a great day! Please press enter to exit the program...")

def get_user_choice():
    while True:
        try:
            user_choice = int(input("Your selection: "))
            if 1 <= user_choice <= 3:
                return user_choice
        except ValueError:
            pass
        print("\nPlease enter a valid selection!\n")

def get_user_file(choice_encrypt):
    while True:
        user_file = input("Enter your file's full name: ").strip()
        if not choice_encrypt:
            user_file += ".yagbu"
        if Path(user_file).exists():
            return user_file
        print("\nFile not found! Check the file name.\n")

def get_user_seed_and_key():
    while True:
        try:
            user_seed = int(input("Enter your seed (integer): "))
            user_key = abs(int(input("Enter your key (positive integer): ")))
            return user_seed, [int(i) for i in str(user_key)]
        except ValueError:
            print("\nPlease enter a valid seed/key!\n")

def encrypt(user_key, alfabetas, rev_alfabetas, user_file):
    CHUNK = DATA_CHUNKS
    hex_from_bytes = bytes.hex
    bytes_from_hex = bytes.fromhex
    alfabeta0 = alfabetas[0]
    rev = rev_alfabetas
    key_iter = cycle(user_key)
    try:
        with open(user_file, "rb") as file_in, open(f"{user_file}.yagbu", "wb") as file_out:
            read = file_in.read
            write = file_out.write
            while data_chunk := read(CHUNK):
                data_ready = "".join(rev[next(key_iter)][alfabeta0[value]]for value in hex_from_bytes(data_chunk))
                write(bytes_from_hex(data_ready))
    except KeyboardInterrupt:
        return False
    else:
        return True

def decrypt(user_key, alfabetas, rev_alfabetas, user_file):
    CHUNK = DATA_CHUNKS
    hex_from_bytes = bytes.hex
    bytes_from_hex = bytes.fromhex
    rev_alfabeta0 = rev_alfabetas[0]
    alfabe = alfabetas
    key_iter = cycle(user_key)
    try:
        with open(user_file, "rb") as file_in, open(user_file.removesuffix(".yagbu"), "wb") as file_out:
            read = file_in.read
            write = file_out.write
            while data_chunk := read(CHUNK):
                data_ready = "".join(rev_alfabeta0[alfabe[next(key_iter)][value]]for value in hex_from_bytes(data_chunk))
                write(bytes_from_hex(data_ready))
    except KeyboardInterrupt:
        return False
    else:
        return True

def key_gen(user_seed):
    base = list('''0123456789abcdef''')
    alfabetas, rev_alfabetas = [], []
    dict_alfabeta = {key: item for item, key in enumerate(base)}
    alfabetas.append(dict_alfabeta)
    rev_alfabetas.append({key: item for item, key in dict_alfabeta.items()})
    for i in range(9):
        chars = base.copy()
        seedset = random.Random(int(user_seed)+i)
        seedset.shuffle(chars)
        dict_alfabeta = {key: item for item, key in enumerate(chars)}
        alfabetas.append(dict_alfabeta)
        rev_alfabetas.append({key: item for item, key in dict_alfabeta.items()})
    return tuple(alfabetas), tuple(rev_alfabetas)

def clean_up(user_file, option):
    if option == 1:
        file = Path(user_file)
        if file.exists():
            file.unlink()
    elif option == 2:
        file = Path(f"{user_file}.yagbu")
        if file.exists():
            file.unlink()
    else:
        file = Path(f"{user_file.removesuffix(".yagbu")}")
        if file.exists():
            file.unlink()

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