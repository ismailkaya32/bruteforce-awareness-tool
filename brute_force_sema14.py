import time
import sys
import tty
import termios
import string
from colorama import Fore, init

# Colorama başlat
init(autoreset=True)

# Şifreyi gizleyerek alır
def get_password(valid_characters):
    password = ""
    print(f"{Fore.YELLOW}5 karakterli bir şifre belirleyin ({', '.join(valid_characters)}): ", end="", flush=True)
    
    while True:
        char = getch()
        
        if char == "\r":  # Enter tuşuna basıldığında döngü sonlanır
            break
        
        if char == "\x7f":  # Backspace karakteri
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        elif char in valid_characters:
            password += char
            sys.stdout.write("*")
            sys.stdout.flush()
        else:
            print(f"\n{Fore.RED}Geçersiz karakter! Lütfen belirtilen karakterleri kullanın.")

    print()
    return password

# Tek bir karakteri okur (getch benzeri)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def brute_force(target_password, characters):
    print(f"{Fore.CYAN}Brute force saldırısı başlıyor...")
    time.sleep(1)

    max_length = len(target_password)
    
    start_time = time.time()  # Başlangıç zamanı
    attempts = 0  # Deneme sayacı
    
    def try_combinations(prefix):
        nonlocal attempts
        if len(prefix) == max_length:
            attempts += 1
            if prefix == target_password:
                print(f"{Fore.GREEN}Deniyor: {prefix}")  # Doğru şifre yeşil renkte
                print(f"{Fore.GREEN}Şifre bulundu: {prefix}")
                end_time = time.time()  # Bitiş zamanı
                duration = end_time - start_time
                print(f"{Fore.GREEN}Şifre {duration:.2f} saniyede bulundu ve {attempts} deneme yapıldı.")
                return True  # Şifre bulundu, döngüyü sonlandır
            else:
                print(f"{Fore.RED}Deniyor: {prefix}")  # Yanlış şifre kırmızı renkte
            return False

        for char in characters:
            if try_combinations(prefix + char):
                return True
        return False

    try_combinations("")

def main():
    print(f"{Fore.MAGENTA}########################################")
    print(f"{Fore.MAGENTA}#           HACKING TOOL MENU          #")
    print(f"{Fore.MAGENTA}########################################")
    print(f"{Fore.YELLOW}  1.  Brute Force Saldırısı (Sadece Sayılar)")
    print(f"{Fore.YELLOW}  2.  Brute Force Saldırısı (Harf ve Sayılar)")
    print(f"{Fore.YELLOW}  3.  Brute Force Saldırısı (Sadece Harfler)")
    print(f"{Fore.YELLOW}  4.  Brute Force Saldırısı (Harf, Sayı ve Özel Karakterler)")
    print(f"{Fore.MAGENTA}########################################")
    
    choice = input(f"{Fore.CYAN}Lütfen bir seçenek seçin (1, 2, 3 veya 4): ")

    if choice == "1":
        print(f"{Fore.CYAN}Sadece Sayılar seçildi.")
        valid_characters = list(string.digits)  # Sadece sayılar
    elif choice == "2":
        print(f"{Fore.CYAN}Harf ve Sayılar seçildi.")
        valid_characters = list(string.ascii_letters + string.digits)  # Harf ve sayılar
    elif choice == "3":
        print(f"{Fore.CYAN}Sadece Harfler seçildi.")
        valid_characters = list(string.ascii_letters)  # Sadece harfler
    elif choice == "4":
        print(f"{Fore.CYAN}Harf, Sayı ve Özel Karakterler seçildi.")
        valid_characters = list(string.ascii_letters + string.digits + string.punctuation)  # Harf, sayı ve özel karakterler
    else:
        print(f"{Fore.RED}Geçersiz seçenek! Çıkılıyor.")
        return

    user_password = get_password(valid_characters)

    if len(user_password) != 5:
        print(f"{Fore.RED}Hatalı giriş! Lütfen 5 karakterli bir şifre girin.")
        return

    brute_force(user_password, valid_characters)

if __name__ == "__main__":
    main()
