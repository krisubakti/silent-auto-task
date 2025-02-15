from playwright.sync_api import sync_playwright
import time
import random
import string

# Load semua token dari file
with open("tokens.txt", "r") as f:
    tokens = [line.strip() for line in f.readlines()]

# Fungsi untuk generate teks random yang jarang digunakan
def generate_random_text(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def login_and_run_task(token):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Ubah ke False kalau mau lihat
        page = browser.new_page()

        # Set token di header
        page.set_extra_http_headers({"Authorization": f"Bearer {token}"})
        page.goto("https://ceremony.silentprotocol.org/ceremonies")

        # Cek apakah login berhasil
        if "ceremonies" in page.url:
            print(f"Login berhasil dengan token: {token}")

            while True:
                # Cek dan klik task yang tersedia
                contribute_buttons = page.locator("text='Contribute'").all()
                if contribute_buttons:
                    print(f"Ada {len(contribute_buttons)} task yang bisa dikerjakan.")
                    for btn in contribute_buttons:
                        try:
                            btn.click()
                            print("Task diklik, menunggu halaman input teks...")
                            break
                        except:
                            print("Gagal klik, coba lagi nanti.")

                    # Tunggu halaman input teks muncul
                    page.wait_for_selector("input", timeout=60000)  
                    print("Halaman input teks muncul!")

                    # Masukkan teks acak
                    random_text = generate_random_text()
                    page.fill("input", random_text)
                    print(f"Teks '{random_text}' dimasukkan!")

                    # Klik "Contribute" untuk menyelesaikan
                    page.click("text='Contribute'")
                    print("Klik Contribute, menunggu selesai...")

                    # Tunggu sampai tombol "Back to Home" muncul
                    page.wait_for_selector("text='Back to Home'", timeout=60000)
                    print("Task selesai! Kembali ke halaman utama.")

                    # Klik "Back to Home" untuk kembali ke halaman utama
                    page.click("text='Back to Home'")
                    time.sleep(5)  # Tunggu sebentar sebelum lanjut

                else:
                    print("Tidak ada task yang bisa dikerjakan, cek lagi...")
                    time.sleep(5)  # Cek ulang tiap 5 detik

            browser.close()
            return True  # Stop setelah satu berhasil
        else:
            print(f"Login gagal untuk token: {token}")
            browser.close()
            return False

# Coba login dengan setiap token
for token in tokens:
    if login_and_run_task(token):
        break  # Stop setelah satu berhasil login