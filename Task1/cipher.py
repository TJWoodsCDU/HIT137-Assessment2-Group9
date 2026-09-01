
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str):
    pass


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str):
    pass


def verify_files(original_path: str, decrypted_path: str):
    pass


def main():
    # Get inputs (shift1 and shift2)
    while True:
        shift1 = input("Enter shift1: ")
        try:
            shift1 = int(shift1)
            if shift1 >= 0:
                break
            else:
                print("shift1 must be non-negative")
                continue
        except ValueError:
            print("shift1 must be an integer")
            continue

    while True:
        shift2 = input("Enter shift2: ")
        try:
            shift2 = int(shift2)
            if shift2 >= 0:
                break
            else:
                print("shift2 must be non-negative")
                continue
        except ValueError:
            print("shift2 must be an integer")
            continue

    # action
    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
    verify_files("raw_text.txt", "decrypted_text.txt")




if __name__ == "__main__":
    main()
