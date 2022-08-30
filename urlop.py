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

from miesiac import numer_miesiac

class urlop():
  def czy_mial_urlop(miesiac, rok):
    nazwa_miesiaca = numer_miesiac.nazwa_miesiaca_strptime(miesiac)
    if not if_exist(nazwa_miesiaca + " " +  rok):
      #if not if_chorobowe_tak(nazwa_miesiaca, rok):
      url = str(input("Czy brałeś urlop miesiąca {}? ".format(nazwa_miesiaca))).upper()
      if url == "TAK":
        urlop.data_urlopu()
          
      elif url == "NIE":
        salary_task["URLOP"]["DNI_URLOPU"] = 0
        salary_task["URLOP"]["OD"] = "0000-00-00"
        salary_task["URLOP"]["DO"] = "0000-00-00"
        
  def data_urlopu():
    while True:
      start_urlop = str(input("Podaj dzień początku urlopu: "))
      end_urlop = str(input("Podaj dzień końca urlopu: "))
      if search_function(start_urlop):
        data_poczatek_urlop = numer_miesiac.data_str_do_datetime(start_urlop)
        data_koniec_urlop = numer_miesiac.data_str_do_datetime(end_urlop)
        if numer_miesiac.miesiac(replace_str(data_poczatek_urlop)) == numer_miesiac.miesiac(replace_str(data_koniec_urlop)):
          urlop.dni_urlopu_jeden_miesiac(start_urlop, end_urlop, data_poczatek_urlop, data_koniec_urlop)
        else:
          urlop.dni_urlopu(data_poczatek_urlop, data_koniec_urlop)
        return True
      else:
        print("Nieprawidłowa data")

  def dni_urlopu_jeden_miesiac(str_poczatek, str_koniec, poczatek, koniec):
    print("""DNI URLOPU JEDEN MIESIAC""")
    ilosc_dni_urlopu = 0
    miesiac_var = numer_miesiac.miesiac(replace_str(poczatek))

    dni_urlopu_weekend = urlop.dni_urlopu_swieta(poczatek, koniec)

    for data in range(int((koniec - poczatek).days)+1):
      date_cnt = str(poczatek + datetime.timedelta(data))

      ilosc_dni_urlopu += dni_tygodnia.dni_tygodnia(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)), 7)

      print("Ilosc dni urlopu w weekend:", dni_urlopu_weekend)
    print("Za miesiac {} przypada {} urlopu".format(miesiac_var,ilosc_dni_urlopu))
    print("Ilość dni urlopu:", ilosc_dni_urlopu)
    salary_task["URLOP"]["DNI_URLOPU"] = ilosc_dni_urlopu - dni_urlopu_weekend
    salary_task["URLOP"]["OD"] = str_poczatek
    salary_task["URLOP"]["DO"] = str_koniec
    salary_task["URLOP"]["GODZINY_URLOP"] = ilosc_dni_urlopu * 8

  def dni_urlopu(poczatek, koniec):
    print("""DNI URLOPU""")
    ilosc_dni_urlopu = 0
    dni_urlopu_weekend = 0

    start = poczatek
    end = poczatek

    for data in range(int((koniec - poczatek).days)+1):

      date_cnt = str(poczatek + datetime.timedelta(data))
      
      if numer_miesiac.miesiac(replace_str(date_cnt)) == numer_miesiac.miesiac(replace_str(start)):
        end = datetime.datetime.strptime(date_cnt, '%Y-%m-%d %H:%M:%S')
        
        ilosc_dni_urlopu += dni_tygodnia.dni_tygodnia(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)), 7)
        
      if numer_miesiac.miesiac(replace_str(date_cnt)) !=  numer_miesiac.miesiac(replace_str(start)):
        dni_urlopu_weekend = urlop.dni_urlopu_swieta(start, end)
        print("ILOSC DNI URLOPU:", ilosc_dni_urlopu)
        url = ilosc_dni_urlopu - dni_urlopu_weekend
        url.warunek_urlop(start, ilosc_dni_urlopu, end, url)
        
        print(numer_miesiac.data_wczesniejsze(replace_str(start)),start, end, ilosc_dni_urlopu, 'dni urlopu', dni_urlopu_weekend)
        ilosc_dni_urlopu = 1
        start = datetime.datetime.strptime(date_cnt, '%Y-%m-%d %H:%M:%S')

      if numer_miesiac.data_str_do_datetime(replace_str(end)) ==  numer_miesiac.data_str_do_datetime(replace_str(koniec)):
        
        print("ILOSC DNI URLOPU:", ilosc_dni_urlopu)
        dni_urlopu_weekend = urlop.dni_urlopu_swieta(start, end)

        url = ilosc_dni_urlopu - dni_urlopu_weekend
        urlop.warunek_urlop(start, ilosc_dni_urlopu, end, url)
        
        print(numer_miesiac.data_wczesniejsze(replace_str(start)),start, end, ilosc_dni_urlopu, 'dni urlopu', dni_urlopu_weekend)

        
  def warunek_urlop(start, ilosc_dni_urlopu, end, urlop):
    if not if_exist(numer_miesiac.data_wczesniejsze(replace_str(start))):

          salary_task["URLOP"]["DNI_URLOPU"] = ilosc_dni_urlopu
          salary_task["URLOP"]["OD"] = replace_str(start)
          salary_task["URLOP"]["DO"] = replace_str(end)
          dzien = numer_miesiac.dni_w_miesiacu(int(start.strftime("%m")))
          print(int(start.strftime("%m")))
          salary_task["URLOP"]["GODZINY_URLOP"] = ilosc_dni_urlopu * 8
          print_dni_pracy(numer_miesiac.data_wczesniejsze(replace_str(start)))
          #print("W chorobowym: ",dzien, start.strftime("%m"), str(start.strftime("%Y-%m-%d")))
    else:
          print("Zapis",numer_miesiac.data_wczesniejsze(replace_str(start)),"juz isnieje")

  def dni_urlopu_swieta(start, end):
    ilosc_dni_urlopu = 0
    
    for data in range(int((end - start).days)+1):
      date_cnt = str(start + datetime.timedelta(data))
      ilosc_dni_urlopu += dni_tygodnia.weekend(dzien_tygodnia.dzien_tygodnia(replace_str(date_cnt)))

      if swieta.swieta_polska(replace_str(date_cnt)):
        
        ilosc_dni_urlopu += 1
    return ilosc_dni_urlopu