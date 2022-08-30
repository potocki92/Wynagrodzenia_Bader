from replace_str import replace_str
from salary_dictionary import salary_task, zapis_danych, if_exist, db_tiny, search_function, if_chorobowe_tak, dni_pracy, print_dni_pracy
from miesiac import numer_miesiac
from datetime import date
import datetime
import dzien_tygodnia
import dni_tygodnia
import swieta
from stawka import stawka
import skladki
from nadgodziny import nadgodziny

class chorobowe():
  def czy_chorowal(miesiac, rok):
    nazwa_miesiaca = numer_miesiac.nazwa_miesiaca_strptime(miesiac)
    if not if_exist(nazwa_miesiaca + " " +  rok):
      print("Chr")
      if not if_chorobowe_tak(nazwa_miesiaca, rok):
        chr = str(input("Czy chorowałeś miesiąca {}? ".format(nazwa_miesiaca))).upper()
        if chr == "TAK":
          salary_task["CHOROBOWE"] = chr
          chorobowe.data_chorobowego()
          return True
        elif chr == "NIE":
          salary_task["CHOROBOWE"] = chr
          salary_task["CZAS_CHOROBY"]["DNI_CHOROBOWEGO"] = 0
          salary_task["CZAS_CHOROBY"]["OD"] = "0000-00-00"
          salary_task["CZAS_CHOROBY"]["DO"] = "0000-00-00"
        #print("NIE CHORUJE")
          return False
      else:
      #print("Chorowałeś {} miesiaca".format(miesiac))
        pass
      
  def data_chorobowego():
    while True:
      start_chr = str(input("Podaj dzień początku chorobowego: "))
      end_chr = str(input("Podaj dzień końca choroboweg: "))
      if search_function(start_chr):
        data_poczatek_chr = numer_miesiac.data_str_do_datetime(start_chr)
        data_koniec_chr = numer_miesiac.data_str_do_datetime(end_chr)
        if numer_miesiac.miesiac(replace_str(data_poczatek_chr)) == numer_miesiac.miesiac(replace_str(data_koniec_chr)):
          chorobowe.dni_chorobowego_jeden_miesiac(start_chr, end_chr, data_poczatek_chr, data_koniec_chr)
        else:
          chorobowe.dni_chorobowego(data_poczatek_chr, data_koniec_chr)
        return True
      else:
        print("Nieprawidłowa data")
    

  def dni_chorobowego_jeden_miesiac(str_poczatek, str_koniec, poczatek, koniec):
    print("""DNI CHOROBOWEGO JEDEN MIESIAC""")
    ilosc_dni_chorobowego = 0
    miesiac_var = numer_miesiac.miesiac(replace_str(poczatek))

    dni_chr_weekend = chorobowe.dni_chorobowego_swieta(poczatek, koniec)

    for data in range(int((koniec - poczatek).days)+1):
      date_cnt = str(poczatek + datetime.timedelta(data))

      ilosc_dni_chorobowego += dni_tygodnia.dni_tygodnia(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)), 7)
    
    print("Ilosc dni chorobowego w weekend:", dni_chr_weekend)
    print("Za miesiac {} przypada {} chorobowego".format(miesiac_var,ilosc_dni_chorobowego))

    print("Ilość dni chorobowego:", ilosc_dni_chorobowego)
    salary_task["CZAS_CHOROBY"]["DNI_CHOROBOWEGO"] = ilosc_dni_chorobowego - dni_chr_weekend
    salary_task["DATA"] = numer_miesiac.data_wczesniejsze(replace_str(date_cnt))
    salary_task["CZAS_CHOROBY"]["OD"] = str_poczatek
    salary_task["CZAS_CHOROBY"]["DO"] = str_koniec
    salary_task["CZAS_CHOROBY"]["GODZINY_CHOROBOWE"] = ilosc_dni_chorobowego * 8
    zapis_danych()

  def dni_chorobowego(poczatek, koniec):
    print("""DNI CHOROBOWEGO""")
    ilosc_dni_chorobowego = 0
    dni_chr_weekend = 0

    start = poczatek
    end = poczatek

    for data in range(int((koniec - poczatek).days)+1):

      date_cnt = str(poczatek + datetime.timedelta(data))
      #print("date_cnt:",date_cnt)

      if numer_miesiac.miesiac(replace_str(date_cnt)) == numer_miesiac.miesiac(replace_str(start)):
        end = datetime.datetime.strptime(date_cnt, '%Y-%m-%d %H:%M:%S')
        
        ilosc_dni_chorobowego += dni_tygodnia.dni_tygodnia(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)), 7)
        
      if numer_miesiac.miesiac(replace_str(date_cnt)) !=  numer_miesiac.miesiac(replace_str(start)):
        dni_chr_weekend = chorobowe.dni_chorobowego_swieta(start, end)
        
        print("ILOSC DNI CHOROBOWEGO:", ilosc_dni_chorobowego)
        chr = ilosc_dni_chorobowego - dni_chr_weekend
        chorobowe.warunek_chorobowy(start, ilosc_dni_chorobowego, end, chr)
        
        
        print(numer_miesiac.data_wczesniejsze(replace_str(start)),start, end, ilosc_dni_chorobowego, 'dni chr', dni_chr_weekend)
        ilosc_dni_chorobowego = 1
        start = datetime.datetime.strptime(date_cnt, '%Y-%m-%d %H:%M:%S')
        
      if numer_miesiac.data_str_do_datetime(replace_str(end)) ==  numer_miesiac.data_str_do_datetime(replace_str(koniec)):
        
        print("ILOSC DNI CHOROBOWEGO:", ilosc_dni_chorobowego)
        dni_chr_weekend = chorobowe.dni_chorobowego_swieta(start, end)
        chr = ilosc_dni_chorobowego - dni_chr_weekend
        chorobowe.warunek_chorobowy(start, ilosc_dni_chorobowego, end, chr)
        
        print(numer_miesiac.data_wczesniejsze(replace_str(start)),start, end, ilosc_dni_chorobowego, 'dni chr', dni_chr_weekend)

  def warunek_chorobowy(start, ilosc_dni_chorobowego, end, chr):
        if not if_exist(numer_miesiac.data_wczesniejsze(replace_str(start))):
          salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
          salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()

          salary_task["CZAS_CHOROBY"]["DNI_CHOROBOWEGO"] = ilosc_dni_chorobowego
          salary_task["DATA"] = numer_miesiac.data_wczesniejsze(replace_str(start))
          salary_task["CZAS_CHOROBY"]["OD"] = replace_str(start)
          salary_task["CZAS_CHOROBY"]["DO"] = replace_str(end)
          dzien = numer_miesiac.dni_w_miesiacu(int(start.strftime("%m")))
          print(int(start.strftime("%m")))
          dni_pracy(dzien, start.strftime("%m"), start, chr, 0)
          salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
          salary_task["CZAS_CHOROBY"]["GODZINY_CHOROBOWE"] = ilosc_dni_chorobowego * 8
          nadgodziny.zapisz_stawka()
          skladki.zapisz_skladki()
          zapis_danych()
          print_dni_pracy(numer_miesiac.data_wczesniejsze(replace_str(start)))
          #print("W chorobowym: ",dzien, start.strftime("%m"), str(start.strftime("%Y-%m-%d")))
        else:
          print("Zapis",numer_miesiac.data_wczesniejsze(replace_str(start)),"juz isnieje")
          
  def dni_chorobowego_swieta(poczatek, koniec):
    ilosc_dni_chorobowego = 0
    
    for data in range(int((koniec - poczatek).days)+1):
      date_cnt = str(poczatek + datetime.timedelta(data))
      ilosc_dni_chorobowego += dni_tygodnia.weekend(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)))

      if swieta.swieta_polska(replace_str(date_cnt)):
        
        ilosc_dni_chorobowego += 1
    return ilosc_dni_chorobowego

  def if_dlugie_chorobowe(date, miesiac):
    print(date, miesiac)
