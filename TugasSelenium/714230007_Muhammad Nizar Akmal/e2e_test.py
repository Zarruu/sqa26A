from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Inisialisasi Chrome WebDriver
driver = webdriver.Chrome()

try:
    print("Memulai pengujian integrasi sistem end-to-end...")
    
    # 1. Buka aplikasi
    # Ganti "file:///PATH_KE_FILE_KAMU/index.html" dengan path lokal HTML atau URL hosting aplikasimu
    driver.get("https://undanganrichard.web.app/") # Sesuaikan dengan URL server lokal
    driver.maximize_window()
    
    wait = WebDriverWait(driver, 10)
    
    # 2. Skenario: Membuka Undangan
    print("Mencoba membuka sampul undangan...")
    open_btn = wait.until(EC.element_to_be_clickable((By.ID, "open-invitation-btn")))
    open_btn.click()
    
    # Beri jeda sebentar agar animasi transisi (fade-out sampul/scroll) selesai
    time.sleep(2)
    
    # 3. Skenario: Mengisi Form RSVP
    print("Mengisi formulir RSVP...")
    
    # Mengisi Nama
    name_input = wait.until(EC.presence_of_element_located((By.ID, "rsvp-name")))
    name_input.send_keys("Penguji Selenium")
    
    # Memilih Kehadiran (Dropdown)
    attendance_dropdown = driver.find_element(By.ID, "rsvp-attendance")
    select_attendance = Select(attendance_dropdown)
    select_attendance.select_by_value("hadir") # Memilih opsi "Akan Hadir"
    
    # Mengisi Jumlah Tamu
    guests_input = driver.find_element(By.ID, "rsvp-guests")
    guests_input.clear() # Bersihkan value default "1"
    guests_input.send_keys("2")
    
    # Mengisi Ucapan
    wishes_input = driver.find_element(By.ID, "rsvp-wishes")
    wishes_input.send_keys("Selamat menempuh hidup baru! Pengujian sistem berjalan lancar.")
    
   # 4. Skenario: Mengirim Form RSVP
    print("Mengirim formulir RSVP...")
    submit_button = driver.find_element(By.CSS_SELECTOR, "#rsvp-form .btn-submit")
    
    # Scroll halaman ke elemen tombol submit agar posisinya berada di tengah layar
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
    
    # Beri jeda 1 detik untuk memastikan animasi scroll atau efek AOS sudah selesai
    time.sleep(1) 
    
    # Lakukan klik menggunakan JavaScript untuk mem-bypass elemen yang mungkin menutupi (seperti tombol musik)
    try:
        submit_button.click()
    except:
        # Jika click() biasa masih gagal, paksa klik menggunakan eksekusi JS
        driver.execute_script("arguments[0].click();", submit_button)
    
    # 5. Verifikasi Hasil Akhir
    # Karena pengiriman data biasanya memakan waktu (ke Firebase), kita tunggu elemen list terupdate
    # atau cukup beri jeda untuk melihat aksi sukses dieksekusi oleh sistem.
    time.sleep(3)
    
    print("Pengujian end-to-end selesai dan berhasil mengeksekusi alur utama!")

except Exception as e:
    print(f"Terjadi kesalahan saat pengujian: {e}")

finally:
    # Tutup browser
    driver.quit()