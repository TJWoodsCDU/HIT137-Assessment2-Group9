
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str):
    try:
        # Read the input file
        with open(input_path, 'r') as file:
            text = file.read()
            
        result = ""
        
        for char in text:
            if 'a' <= char <= 'n': # Lowercase a-n: shift forward by shift1 * shift2
                new_pos = (ord(char) - ord('a') + (shift1 * shift2)) % 26
                result += chr(ord('a') + new_pos)
            
            elif 'o' <= char <= 'z': # Lowercase o-z: shift backward by shift1 + shift2
                new_pos = (ord(char) - ord('a') - (shift1 + shift2)) % 26
                result += chr(ord('a') + new_pos)
           
            elif 'A' <= char <= 'M': # Uppercase N-M: Shift backward by shift1
                new_pos = (ord(char) - ord('A') - shift1) % 26
                result += chr(ord('A') + new_pos)
            
            elif 'N' <= char <= 'Z': # Uppercase N-Z: shift forward by shift2^2
                new_pos = (ord(char) - ord('A') + (shift2 ** 2)) %26
                result += chr(ord('A') + new_pos)
            
            elif '0' <= char <= '9': #Digits: shift forward by shift1 - shift2
                new_pos = (ord(char) - ord('0') + (shift1 - shift2)) % 10
                result += chr(ord('0') + new_pos)
            
            else: # Everything else stays the same
                result += char
        
        # Write the encrypted text
        with open(output_path, 'w') as file:
            file.write(result)
        
        print(f" Encrypted '{input_path}' -> '{output_path}'")
   
    except FileNotFoundError:
        print(f" Error: File '{input_path}' not found.")
    except Exception as e:
        print (f" Error during encryption: {e}")


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
