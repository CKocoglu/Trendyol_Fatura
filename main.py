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
            , "Teslimat_adres", "Fatura_adı", "Fatura_adres"]

def initialize_csv_file():
    with open(f"{file_name}.csv", "w", newline='')as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # başlarına fieldnameleri ekliyor
        file.close()

def append_csv_file(siparis_no,isim,farkli_urun_adedi,siparis_adet,urun_adi,satis_tutari
                    ,kargo_kodu,teslimat_isim,teslimat_adres,fatura_isim,fatura_adres):

    with open (f"{file_name}.csv" , "a" , newline='')as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)

        writer.writerow({"Siparis_no": siparis_no, "isim": isim, "Farkli_urun_adedi": farkli_urun_adedi,
                         "Siparis_adedi": siparis_adet , "Urun_adi": urun_adi, "Satis_tutari": satis_tutari,
                         "Kargo_kodu": kargo_kodu, "Teslimat_adı": teslimat_isim , "Teslimat_adres": teslimat_adres,
                         "Fatura_adı": fatura_isim, "Fatura_adres": fatura_adres})
        file.close()

def convert_stringToFloat(string):
    a = string.split(",")
    b = a[1].split()
    tutar = float(a[0] + "." + b[0])
    return tutar

def fix_adress(string):
    a = string.split()
    address = ""
    for i in range(1, len(a)):
        address += a[i] + " "
    return address

def fix_name(string):
    a = string.split()
    name = ""
    for i in range(2, len(a)):
        name += a[i] + " "

    print(name)

    return name
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
    print("Anasayfanın yüklenmesi bekleniyor...")
    try:
        siparis_show_xpath ='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[1]/a/span[1]'
        siparis_xpath='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[1]/a/span[1]'
        kargo_asamasi_xpath='//*[@id="header"]/div[1]/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[2]/a[1]/span'

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, siparis_show_xpath)))
        print("Anasayfa yüklendi , kargo aşamasındaki siparişlere gidiliyor...")
        driver.find_element_by_xpath(siparis_xpath).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, kargo_asamasi_xpath)))
        driver.find_element_by_xpath(kargo_asamasi_xpath).click()

        print("Program başlatılıyor...")
    except:
        logging.error("Bir şeyler ters gitti.")

time.sleep(2)
#siparis sayisi 20 den büyükse gösterim sayısını 50 ye cıkar sayfada.
siparis_sayisi = driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/nav/div/ul/li[2]/a/p').text
print("Toplam aktif sipariş sayınız: %s"%(siparis_sayisi))

for key in str(siparis_sayisi):
    if key.isdigit():
        siparis_sayisi=int(key)

print(siparis_sayisi)

initialize_csv_file()
print("Sipariş bilgileri alınıyor...")


for i in range(2,siparis_sayisi+2):
    print("%d.siparişin bilgileri alınıyor..."%(i-1))

    siparis_no  = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[2]/div[1]/span').text
    print("siparisno ",siparis_no)
    isim        = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[4]').text
    print("isim  ",isim)
    #sonradan düzenle
    farkli_urun_adedi="bura sonradan eklenecek."
    siparis_adet=driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[5]').text
    print("siparis adet ",siparis_adet)
    urun_adi    =driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[6]/div/div[2]/a').text
    print("urun adi  ",urun_adi)

    satis_tutari=driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/ul/li/b').text
    satis_tutari = convert_stringToFloat(satis_tutari)
    print("satis tutari ",satis_tutari)
    kargo_kodu  =driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[8]/div[2]/span[2]').text
    print("kargo kodu = ",kargo_kodu)

    #fatura islemleri kısmı

    driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div[2]/div/button[2]').click()
    # time.sleep(2)
    print("fatura işlemleri kısmına girdim.")
    title = driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/div/div[4]/div/div/div/form/div[1]/h5').text
    print("title" ,title)

    teslimat_isim  = driver.find_element_by_xpath('//*[@id="printable-content"]/p[1]').text
    teslimat_isim = fix_name(teslimat_isim)
    print("teslimat isim ",teslimat_isim)

    teslimat_adres = driver.find_element_by_xpath('//*[@id="printable-content"]/p[2]').text
    teslimat_adres = fix_adress(teslimat_adres)
    print("teslimat adres ",teslimat_adres)
    fatura_isim    = driver.find_element_by_xpath('//*[@id="printable-content"]/p[3]').text
    fatura_isim = fix_name(fatura_isim)
    print("fatura isim ",fatura_isim)
    fatura_adres   = driver.find_element_by_xpath('//*[@id="printable-content"]/p[4]').text
    fatura_adres = fix_adress(fatura_adres)
    print("fatura adres ",fatura_adres)

    driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/div/div[4]/div/div/div/form/div[1]/button/span').click()

    print("%d.sipariş bilgileri alındı.Dosyaya ekleniyor..."%(i-1))
    # ekleme
    append_csv_file(siparis_no, isim, farkli_urun_adedi, siparis_adet, urun_adi, satis_tutari
                    , kargo_kodu, teslimat_isim, teslimat_adres, fatura_isim, fatura_adres)

    print("%d.siparis bilgisi dosyaya eklendi.\n \n"%(i-1))

print("Program başarıyla sonlandı. %d sipariş kaydedildi."%siparis_sayisi)
print("Program kapatılıyor.")
driver.quit()

