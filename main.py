from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from datetime import date
import csv

today = date.today()
file_name = "Tarih_" + str(today.strftime("%d-%m-%Y"))
fieldnames = ["Siparis_no", "isim", "Farkli_urun_adedi", "Siparis_adedi"
            , "Urun_adi", "Satis_tutari", "Kargo_kodu", "Teslimat_adı"
            , "Teslimat_adres", "Fatura_adı", "Fatura_adres", "Email"]

def initialize_csv_file():
    with open(f"{file_name}.csv", "w", newline='')as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # başlarına fieldnameleri ekliyor
        file.close()

def append_csv_file(siparis_no,isim,farkli_urun_adedi,siparis_adet,urun_adi,satis_tutari
                    ,kargo_kodu,teslimat_isim,teslimat_adres,fatura_isim,fatura_adres,email):

    with open (f"{file_name}.csv" , "a" , newline='')as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)

        writer.writerow({"Siparis_no": siparis_no, "isim": isim, "Farkli_urun_adedi": farkli_urun_adedi,
                         "Siparis_adedi": siparis_adet
                            , "Urun_adi": urun_adi, "Satis_tutari": satis_tutari, "Kargo_kodu": kargo_kodu,
                         "Teslimat_adı": teslimat_isim
                            , "Teslimat_adres": teslimat_adres, "Fatura_adı": fatura_isim, "Fatura_adres": fatura_adres,
                         "Email": email})
        file.close()

#options chrome userfile
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\ckocoglu\PycharmProjects\FaturaTrendyol\ChromeUser')
options.add_argument(r"--profile-directory=Profile 2")

#initialize web driver
driver = webdriver.Chrome(r"C:\Users\ckocoglu\PycharmProjects\FaturaTrendyol\Drivers\chromedriver.exe",options=options)
driver.maximize_window()
time.sleep(2)
main_page = "https://partner.trendyol.com/account/login?redirect=%2F/"
driver.get(main_page)

print("Giriş yaptıysan terminale 'go' yaz")
is_login=input()
if is_login == "go" :
    logging.info("Anasayfanın yüklenmesi bekleniyor...")
    try:
        siparis_show_xpath ='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[1]/a/span[1]'
        siparis_xpath='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[1]/a/span[1]'
        kargo_asamasi_xpath='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[2]/a[1]/span'

        logging.info("Anasayfa yüklendi , kargo aşamasındaki siparişlere gidiliyor...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, siparis_show_xpath)))
        driver.find_element_by_xpath(siparis_xpath).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, kargo_asamasi_xpath)))
        driver.find_element_by_xpath(kargo_asamasi_xpath).click()

        logging.info("Program başlatılıyor...")
    except:
        logging.error("Bir şeyler ters gitti.")

#siparis sayisi 20 den büyükse gösterim sayısını 50 ye cıkar sayfada.
siparis_sayisi = int(driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/nav/div/ul/li[2]/a/p').text)
logging.info("Toplam aktif sipariş sayınız: %d"+siparis_sayisi)

initialize_csv_file()
logging.info("Sipariş bilgileri alınıyor...")

try:
    for i in range(2,siparis_sayisi):
        logging.info("%d.siparişin bilgileri alınıyor..."+i-1)

        siparis_no  = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[2]/div[1]/span').text
        isim        = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[4]').text
        #sonradan düzenle
        farkli_urun_adedi="bura sonradan eklenecek."
        siparis_adet=driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[5]').text
        urun_adi    =driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[6]/div/div[2]/a').text
        satis_tutari=int(driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/ul/li/b').text)
        kargo_kodu  =driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[8]/div[2]/span[2]').text

        #fatura islemleri kısmı

        driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div[1]').click()
        time.sleep(2)
        driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div[2]/div/button[2]').click()

        teslimat_isim  = driver.find_element_by_xpath('//*[@id="printable-content"]/p[1]/text()')
        teslimat_adres = driver.find_element_by_xpath('//*[@id="printable-content"]/p[2]/text()')
        fatura_isim    = driver.find_element_by_xpath('//*[@id="printable-content"]/p[3]/text()')
        fatura_adres   = driver.find_element_by_xpath('//*[@id="printable-content"]/p[4]/text()')
        email         = driver.find_element_by_xpath('//*[@id="printable-content"]/div[2]/text()')

        logging.info("%d.sipariş bilgileri alındı.Dosyaya ekleniyor..."+i-1)
        # ekleme
        append_csv_file(siparis_no, isim, farkli_urun_adedi, siparis_adet, urun_adi, satis_tutari
                        , kargo_kodu, teslimat_isim, teslimat_adres, fatura_isim, fatura_adres, email)

        logging.info("%d.siparis bilgisi dosyaya eklendi."+i-1)

except:
    logging.error("Bir şeyler ters giti.Chrome kapatılıyor...")
    driver.quit()
