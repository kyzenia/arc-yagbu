import random
from pathlib import Path
from itertools import cycle
DATA_CHUNKS = 8 * 1024 * 1024

def main():
    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("#                                                       #")
    print("#                      Yagbu v2.0.0                     #")
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
        tables = encrypt_table_gen(alfabetas, rev_alfabetas)
        if encrypt(user_key, tables, user_file) == True:
            credits()
            clean_up(user_file, 1)
            print(f'''Encryption complete. Please check "{user_file}.yagbu"\n''')
        else:
            credits()
            clean_up(user_file, 2)
            print("There has been a problem while encrypting. Encryption aborted.\n")
    elif user_choice == 2:
        tables = decrypt_table_gen(alfabetas, rev_alfabetas)
        if decrypt(user_key, tables, user_file) == True:
            credits()
            clean_up(user_file, 1)
            print(f'''Decryption complete. Please check "{user_file.removesuffix('.yagbu')}"\n''')
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

def encrypt(user_key, tables, user_file):
    CHUNK = DATA_CHUNKS
    key = tuple(user_key)
    len_key = len(key)
    key_pos = 0
    try:
        with open(user_file, "rb") as file_in, open(f"{user_file}.yagbu", "wb") as file_out:
            read = file_in.read
            write = file_out.write
            while data_chunk := read(CHUNK):
                data_ready = bytearray(len(data_chunk))
                for slices in range(len_key):
                    digit = key[(key_pos + slices) % len_key]
                    data_ready[slices::len_key] = (data_chunk[slices::len_key].translate(tables[digit]))
                write(data_ready)
                key_pos = (key_pos + len(data_chunk)) % len_key
    except KeyboardInterrupt:
        return False
    else:
        return True

def decrypt(user_key, tables, user_file):
    CHUNK = DATA_CHUNKS
    key = tuple(user_key)
    len_key = len(key)
    key_pos = 0
    try:
        with open(user_file, "rb") as file_in, open(user_file.removesuffix(".yagbu"), "wb") as file_out:
            read = file_in.read
            write = file_out.write
            while data_chunk := read(CHUNK):
                data_ready = bytearray(len(data_chunk))
                for slices in range(len_key):
                    digit = key[(key_pos + slices) % len_key]
                    data_ready[slices::len_key] = (data_chunk[slices::len_key].translate(tables[digit]))
                write(data_ready)
                key_pos = (key_pos + len(data_chunk)) % len_key
    except KeyboardInterrupt:
        return False
    else:
        return True

def key_gen(user_seed):
    alfabeta = list(range(256))
    alfabetas, rev_alfabetas = [], []
    ab_dict = {key: value for value, key in enumerate(alfabeta)}
    rev_ab_dict = {key: value for value, key in ab_dict.items()}
    alfabetas.append(ab_dict)
    rev_alfabetas.append(rev_ab_dict)
    for i in range(9):
        chars = alfabeta.copy()
        seedset = random.Random((user_seed)+i)
        seedset.shuffle(chars)
        ab_dict = {key: value for value, key in enumerate(chars)}
        rev_ab_dict = {key: value for value, key in ab_dict.items()}
        alfabetas.append(ab_dict)
        rev_alfabetas.append(rev_ab_dict)
    return tuple(alfabetas), tuple(rev_alfabetas)

def encrypt_table_gen(alfabetas, rev_alfabetas):
    tables = []
    ab_0 = alfabetas[0]
    for k in range(10):
        table = bytearray(256)
        for byte in range(256):
            table[byte] = rev_alfabetas[k][ab_0[byte]]
        tables.append(bytes(table))
    return tuple(tables)

def decrypt_table_gen(alfabetas, rev_alfabetas):
    tables = []
    rev_ab_0 = rev_alfabetas[0]
    for k in range(10):
        table = bytearray(256)
        for byte in range(256):
            table[byte] = rev_ab_0[alfabetas[k][byte]]
        tables.append(bytes(table))
    return tuple(tables)

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
        file = Path(f"{user_file.removesuffix('.yagbu')}")
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