from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def read_csv_file():
    with open(f"{file_name}.csv", "r", newline='')as file:
        reader = csv.DictReader(file,fieldnames=fieldnames)
        for line in reader:
            print(line)

        file.close()


def convert_stringToFloat(string):
    if ',' in string:
        a = string.split(",")
        b = a[1].split()
        tutar = float(a[0] + "." + b[0])
    else:
        b = string.split()
        tutar = float(b[0])
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

def fix_name_surname(str):
    full_name =str.split()
    ad = full_name[0:-1]
    soyad=full_name[-1]

    fixed_name=ad[0]
    for i in range (1,len(ad)):
        fixed_name =fixed_name+" "+ad[i]
    return fixed_name,soyad

def log_in_e_arsiv(self):
    file = open(r"Userfile\e-arsiv")
    lines = file.readlines()
    id = lines[0]
    password = lines[1]
    file.close()
    time.sleep(1)
    self.find_element_by_id('userid').send_keys(id)
    time.sleep(1)
    self.find_element_by_id('password').send_keys(password)
    time.sleep(1)
    self.find_element_by_name('action').click()



#1 den fazla urun varsa ayrı ayrı satır ekleyip yazıyor. Test et
def write_receipt(self):
    url = 'https://earsivportal.efatura.gov.tr/intragiris.html'
    self.get(url)
    time.sleep(1)
    log_in_e_arsiv(self)
    #self.find_element_by_class_name('btn waves-effect waves-light').click()
    print("E-arsiv sayfasi yüklendi.")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'gen__1006')))
        self.find_element_by_id('gen__1006').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="gen__1006"]/option[2]')))
        self.find_element_by_xpath('//*[@id="gen__1006"]/option[2]').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Belge İşlemleri')))  #belge islemleri
        print("buton bulundu basiliyor.")
        self.find_element_by_link_text('Belge İşlemleri').click()
        print("butona basildi.")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, '5000/30.000TL Fatura Oluştur')))  #Fatura olustur
        self.find_element_by_link_text('5000/30.000TL Fatura Oluştur').click()
        print("Fatura olusturma sayfasi yuklendi.")

        print("Bilgiler alınıyor...")
        count=1
        with open(f"Tarih_10-04-2021.csv", "r", newline='')as file:
            reader = csv.DictReader(file)
            for line in reader:
                print("%d.siparis faturalandırılıyor..."%(count))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gen__1033')))
                self.find_element_by_id('gen__1033').send_keys(line.get('tc_no'))
                ad,soyad=fix_name_surname(line.get('isim'))
                time.sleep(1)
                self.find_element_by_id('gen__1035').click()
                time.sleep(1)
                self.find_element_by_id('gen__1035').send_keys(ad)
                # time.sleep(1)
                # self.find_element_by_id('gen__1035').send_keys(ad)
                self.find_element_by_id('gen__1036').send_keys(soyad)
                self.find_element_by_id('gen__1042').click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gen__1042"]/option[2]')))
                self.find_element_by_xpath('//*[@id="gen__1042"]/option[2]').click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gen__1043')))
                self.find_element_by_id('gen__1043').send_keys(line.get('Fatura_adres'))

                tbody = self.find_element_by_id('gen__1069-b')
                tbodyID = tbody.get_attribute('id')  #id yi al id ile gitmek icin

                urun_adi = line.get('Urun_adi').split('@')

                for k in range (len(urun_adi)): #urun adı kadar satır olustur.
                    self.find_element_by_id('gen__1089').click()  # satir ekle
                    time.sleep(1)

                if len(urun_adi) > 1:
                    urun = []
                    fiyat_adet_baslik = []
                    for i in range(len(urun_adi)):
                        urun.append(urun_adi[i].split("@"))
                        fiyat_adet_baslik.append(urun[i][0].split("_"))
                        print(f"Birim fiyat = {fiyat_adet_baslik[i][0]}")
                        print(f"Adet = {fiyat_adet_baslik[i][1]}")
                        print(f"Baslik = {fiyat_adet_baslik[i][2]}")


                    # trs   = tbody.find_elements_by_tag_name('tr')


                    for k in range(len(urun_adi)):    #len(trs)
                        td = self.find_element_by_xpath(f'//*[@id="{tbodyID}"]/tr[{k+1}]/td[4]')  # urun adi git id al
                        input_tag = td.find_element_by_tag_name('input')
                        tdID = input_tag.get_attribute('id')
                        ID = int(tdID[5:])  # get id as a integer
                        self.find_element_by_id(f'gen__{ID}').send_keys(fiyat_adet_baslik[k][2])       #urun[k]               #urun adi
                        self.find_element_by_id(f'gen__{ID+1}').send_keys(fiyat_adet_baslik[k][1])     #adet[k]                #adet
                        self.find_element_by_id(f'gen__{ID+2}').click()                          #birim dropdown
                        self.find_element_by_xpath(f'//*[@id="gen__{ID+2}"]/option[8]').click()  #adet sec
                        self.find_element_by_id(f'gen__{ID + 3}').click()
                        self.find_element_by_id(f'gen__{ID+3}').send_keys(fiyat_adet_baslik[k][0].replace('.',','))       #birim fiyatı  yazmamız gerek. Float girdir int giriyor 24.9 u 249 giriyor.
                        self.find_element_by_id(f'gen__{ID+10}').click()
                        self.find_element_by_xpath(f'//*[@id="gen__{ID+10}"]/option[4]').click()
                    self.save_screenshot(f"Screenshots\Siparis_{line.get('Siparis_no')}.png")
                    #tbody.find_element_by_id('gen__1108').click()                #onayla
                    count = count + 1
                else:
                    td = self.find_element_by_xpath(f'//*[@id="{tbodyID}"]/tr[1]/td[4]')  # urun adi git id al
                    input_tag = td.find_element_by_tag_name('input')
                    tdID = input_tag.get_attribute('id')
                    ID = int(tdID[5:])  # get id as a integer
                    self.find_element_by_id(f'gen__{ID}').send_keys(line.get('Urun_adi'))  # urun[k]               #urun adi
                    self.find_element_by_id(f'gen__{ID + 1}').send_keys(line.get('Siparis_adedi'))  # adet[k]                #adet
                    self.find_element_by_id(f'gen__{ID + 2}').click()  # birim dropdown
                    self.find_element_by_xpath(f'//*[@id="gen__{ID + 2}"]/option[8]').click()  # adet sec
                    self.find_element_by_id(f'gen__{ID + 3}').click()
                    self.find_element_by_id(f'gen__{ID + 3}').send_keys(line.get('Satis_tutari').replace('.',','))  # Satis tutari  1 tane cunku 1 urun var , noktayı virgul yap
                    self.find_element_by_id(f'gen__{ID + 10}').click()
                    self.find_element_by_xpath(f'//*[@id="gen__{ID + 10}"]/option[4]').click()
                    self.save_screenshot(f"Screenshots\Siparis_{line.get('Siparis_no')}.png")
                    #tbody.find_element_by_id('gen__1108').click()  # onayla
                    count = count + 1

            file.close()
    except:
        pass
        #tbody id : gen__1069-b     burdan tr ler içinden urun_class name =csc-textbox csc-required
        #adet class  =csc-number
        #drop down birim class = csc-combobox csc-required   , get attribute den id yi al xpathe koy Adedi seç. //*[@id="gen__1256"]/option[8]
        #birim fiyat class = csc-currency  buraya satıs fiyatının %18 yazılacak.
        #kdv oran class = csc-combobox yine attributeden id al //*[@id="gen__1264"]/option[4]  bburaya koy.
        #olustur id = gen__1108
        # satır ekle id :gen__1089
        #mal hizmet adı : gen__1146
#modul seciniz id:gen__1006
#e-arşiv xpath '//*[@id="gen__1006"]/option[2]'
#belge islemleri id :H37177c27d1b09-1100_li
#fatura olustur id:H37177c27d1b09-1105
#tc id  : gen__1033
#ad : gen__1035
#soyad:gen__1036
#ulke dropdown id :gen__1042
#turkiye xpath : '//*[@id="gen__1042"]/option[2]'
#adres id : gen__1043



def initialize():
    #options chrome userfile
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=ChromeUser')
    options.add_argument(r"--profile-directory=Profile 2")
    #initialize web driver
    driver = webdriver.Chrome(r"Drivers\chromedriver.exe",options=options)
    driver.maximize_window()
    time.sleep(2)
    return driver

def start(driver):
    main_page = "https://partner.trendyol.com/account/login?redirect=%2F/"
    driver.get(main_page)
    print("Giriş yaptıysan terminale 'go' yaz")
    is_login=input()
    if is_login == "go" :
        print("Anasayfanın yüklenmesi bekleniyor...")
        try:
            driver.find_element_by_id('icon-close-button-1606319198436').click()
        except:
            pass
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
            print("Bir şeyler ters gitti.")

    time.sleep(3)
    #siparis sayisi 20 den büyükse gösterim sayısını 50 ye cıkar sayfada.
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="shipment-packages"]/div/nav/div/ul/li[2]/a/p')))
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
            satis_tutari = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[1]/td[9]/ul/li[3]/b').text
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
                    urun_fiyat1= driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[3]').text
                    urun_fiyat1= convert_stringToFloat(urun_fiyat1)
                    urun_adet1 = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[1]').text
                    urun_adet1=str(urun_fiyat1) + "_" +urun_adet1
                    urun_adi = urun_adi + "@" +urun_adet1 + "_" + title.text;
                else:
                    urun_fiyat1= driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[7]').text
                    urun_fiyat1= convert_stringToFloat(urun_fiyat1)
                    urun_adet1 = driver.find_element_by_xpath(f'//*[@id="mp-data-table"]/tbody[{i}]/tr[{k}]/td[5]').text
                    urun_adet1 = str(urun_fiyat1) + "_" + urun_adet1
                    urun_adi = urun_adet1 + "_" + title.text;
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

    print("Veri alma işlemi başarıyla sonlandı. %d sipariş kaydedildi."%siparis_sayisi)
    print("Faturalandırma işlemine geçiliyior.")
# write_receipt(driver)
#
# print("Program kapatılıyor.")
# driver.quit()
driver=initialize()
#start(driver)
write_receipt(driver)