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
fieldnames = ["Siparis_no", "isim", "tc_no", "Siparis_adedi"
            , "Urun_adi", "Satis_tutari", "Kargo_kodu", "Teslimat_adı"
            , "Teslimat_adres", "Fatura_adı", "Fatura_adres"]

def initialize_csv_file():
    with open(f"{file_name}.csv", "w", newline='')as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # başlarına fieldnameleri ekliyor
        file.close()

def append_csv_file(siparis_no,isim,tc_no,siparis_adet,urun_adi,satis_tutari
                    ,kargo_kodu,teslimat_isim,teslimat_adres,fatura_isim,fatura_adres):

    with open (f"{file_name}.csv" , "a" , newline='')as file:
        writer = csv.DictWriter(file,fieldnames=fieldnames)

        writer.writerow({"Siparis_no": siparis_no, "isim": isim, "tc_no": tc_no,
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

time.sleep(3)
#siparis sayisi 20 den büyükse gösterim sayısını 50 ye cıkar sayfada.
siparis_sayisi = driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/nav/div/ul/li[2]/a/p').text
print("Toplam aktif sipariş sayınız: %s"%(siparis_sayisi))

siparis_temp=""
for key in str(siparis_sayisi):
    if key.isdigit():
        siparis_temp=siparis_temp+key
siparis_sayisi = int(siparis_temp)

if siparis_sayisi > 20:
    azami_siparis_xpath ='//*[@id="shipment-packages"]/div/div/div[1]/div[1]/nav/div/div/select'
    azami_50_xpath = '//*[@id="shipment-packages"]/div/div/div[1]/div[1]/nav/div/div/select/option[3]'
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,azami_siparis_xpath)))
    driver.find_element_by_xpath(azami_siparis_xpath).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, azami_50_xpath)))
    driver.find_element_by_xpath(azami_50_xpath).click()



print(siparis_sayisi)

initialize_csv_file()
print("Sipariş bilgileri alınıyor...")
time.sleep(1)
for i in range(2, siparis_sayisi + 2):
    tbodys = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]')
    trdata = tbodys.find_elements_by_tag_name("tr")
    siparis_no = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[2]/div[1]/span').text
    print("siparisno ", siparis_no)
    isim = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[4]').text
    print("isim  ", isim)
    # sonradan düzenle
    tc_no = 11111111111
    siparis_adet = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[5]').text
    print("siparis adet ", siparis_adet)
    try:
        satis_tutari = driver.find_element_by_xpath(
            f'//*[@id="mp-data-table"]/tbody[{i}]/tr[1]/td[9]/ul/li[3]/b').text
        satis_tutari = convert_stringToFloat(satis_tutari)
    except:
        satis_tutari = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/ul/li/b').text
        satis_tutari = convert_stringToFloat(satis_tutari)
        pass
    print("satis tutari ", satis_tutari)
    kargo_kodu = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[8]/div[2]/span[2]').text
    print("kargo kodu = ", kargo_kodu)

    urun_adi = ""
    print("len trdata = ", len(trdata))
    if len(trdata) > 2:
        for k in range(1, len(trdata)):
            name = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]')
            title = name.find_element_by_class_name("product-name")
            print(f"{i}.{k}.Title = {title.text}")
            if k != 1:
                urun_adet1 = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[1]').text
                urun_adi = urun_adi + "@" +urun_adet1+title.text;
            else:
                urun_adet1 = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[5]').text
                urun_adi = urun_adet1+title.text;
        print(urun_adi.split("@"))
    else:
        urun_adi = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[6]/div/div[2]/a').text
        print("urun adi = ", urun_adi)

    try:
        fatura_islemleri_xpath = f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div/span'
        fatura_bilgileri_xpath = f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/div/div[1]/div[2]/div/button[2]'
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, fatura_islemleri_xpath)))
        driver.find_element_by_xpath(fatura_islemleri_xpath).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, fatura_bilgileri_xpath)))
        driver.find_element_by_xpath(fatura_bilgileri_xpath).click()
        time.sleep(1)

    except:
        driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr/td[9]/span').click()
        pass

    # time.sleep(2)
    print("fatura işlemleri kısmına girdim.")
    # title = driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/div/div[4]/div/div/div/form/div[1]/h5').text
    # print("title" ,title)

    teslimat_isim = driver.find_element_by_xpath('//*[@id="printable-content"]/p[1]').text
    teslimat_isim = fix_name(teslimat_isim)
    print("teslimat isim ", teslimat_isim)

    teslimat_adres = driver.find_element_by_xpath('//*[@id="printable-content"]/p[2]').text
    teslimat_adres = fix_adress(teslimat_adres)
    print("teslimat adres ", teslimat_adres)
    fatura_isim = driver.find_element_by_xpath('//*[@id="printable-content"]/p[3]').text
    fatura_isim = fix_name(fatura_isim)
    print("fatura isim ", fatura_isim)
    fatura_adres = driver.find_element_by_xpath('//*[@id="printable-content"]/p[4]').text
    fatura_adres = fix_adress(fatura_adres)
    print("fatura adres ", fatura_adres)

    driver.find_element_by_xpath('//*[@id="shipment-packages"]/div/div/div[4]/div/div/div/form/div[1]/button/span').click()

    print("%d.sipariş bilgileri alındı.Dosyaya ekleniyor..." % (i - 1))
    # ekleme
    append_csv_file(siparis_no, isim, tc_no, siparis_adet, urun_adi, satis_tutari
                    , kargo_kodu, teslimat_isim, teslimat_adres, fatura_isim, fatura_adres)

    print("%d.siparis bilgisi dosyaya eklendi.\n \n"%(i-1))

print("Program başarıyla sonlandı. %d sipariş kaydedildi."%siparis_sayisi)
print("Program kapatılıyor.")
driver.quit()
