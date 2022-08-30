import json
from tinydb import TinyDB
from tinydb import Query, where
from salary_dictionary import salary_task, zapis_danych, q_tiny, if_exist, dni_pracy, premia_warunek
from stawka import stawka
import skladki
import miesiac
import dni_pracujace
from chorobowe import chorobowe
import swieta
from datetime import datetime
from dateutil import rrule
from replace_str import replace_str
from nadgodziny import nadgodziny
from urlop import urlop

""" APLIKACJA DO WYLICZANJA WYNAGRODZENIA Z FIRMY BADER."""

"""Zaczynamy od podania daty rozpoczecia pracy w firmie. Aplikacja ma za zadanie zapisać wszystkie dni pracujace, chorobowe, urlopy, wynagrodzenia za kazdy miesiac, skladki. Chorobowe oraz urlopy podaje użytkownik. Premia oraz dodatek jest zależny od chorobowego (dodatek funkcyjny jest w trakcie tworzenia)."""

db = TinyDB('salary_db.json')
db.default_table_name = "salary"
q = Query()

def getFieldData(fieldName):
    result = [r[fieldName] for r in db]
    return result

# Użytkownik podaje datę rozpoczęcia pracy
def rozpoczecie_pracy():
  if not db.search(q.DATA_ROZPOCZECIA_PRACY.exists()):
    data_rozpoczecia = str(input('Podaj datę rozpoczęcia pracy: '))
    db.insert({'DATA_ROZPOCZECIA_PRACY' : data_rozpoczecia})
    
    wyliczenie_miesiecy()
  else:
    wyliczenie_miesiecy()

"""POMYSLEC JAK SKROCIC FUNKCJE"""
def wyliczenie_miesiecy():
  # pobranie daty rozpoczecia pracy
  start_date = datetime.strptime((db.table("salary").get(q.DATA_ROZPOCZECIA_PRACY.exists())).get("DATA_ROZPOCZECIA_PRACY"), '%Y-%m-%d')
  # data dzisiejsza
  end_date = datetime.today()

  
  for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
      # miesiac z petli dt
      miesiac_dt = dt.strftime("%m")
      # rok z petli dt
      rok_dt = dt.strftime("%Y")
      print()
      print(dt.strftime("%B"),rok_dt)
      # ilosc dni w miesiacy z miesiac_dt
      dzien = miesiac.numer_miesiac.dni_w_miesiacu(int(miesiac_dt))
      # warunek jesli miesiac i rok z petli dt jest ten sam co start_date (miesiac + rok) 
      if (dt.strftime("%B") + " " + dt.strftime("%Y")) == (start_date.strftime("%B") + " " + start_date.strftime("%Y")):
        # funkcja liczaca dni pracujace, chorobowe oraz urlop wylacznie w miesiacu rozpoczecia pracy
        dni_miesiaca_zatrudnienia()
      else:
        print("ILOSC DNI W MIESIACU:" ,dzien)
        print("ILOSC DNI ROBOCZYCH W MIESIACU:",dni_pracujace.dni_pracujace(dzien, int(miesiac_dt), dt.strftime("%Y-%m-%d")))
        # jeśli 'miesiac + rok' nie istnieje w bazie danych to wykonujemy funkcje, ktore wylicza nam wynagrodzenie za dany miesiac i zapisze w bazie danych
        if not if_exist(dt.strftime("%B") + " " + rok_dt):
          # uzytkownik podaje czy chorowal
          if chorobowe.czy_chorowal(miesiac_dt, rok_dt) == False:
            # uzytkownik podaje czy posiadal urlop
            if urlop.czy_mial_urlop(miesiac_dt, rok_dt) == False:
              # baza danych
              salary_task["DATA"] = dt.strftime("%B") + " " + rok_dt
              # funkcja do wyliczenia przepracowanych dni przez uzytkownika (dzien - losc dni w miesiacu, int(numer miesiaca, dt - podanie daty z datatime, 0 - chorobowe, 0 - urlopy))
              dni_pracy(dzien, int(miesiac_dt), dt, 0, 0)
              #salary_task - zapis do dictionary
              print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
              salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
              salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
              salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
              salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
              print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
          
          #salary_task[""]
              # uzytkownik podaje czy wykonywal nadgodziny w tym miesiacu
              if nadgodziny.nadgodziny(dt.strftime("%B") + " " + rok_dt):
                # uzytkownik podaje ilosc nadgodzin 50%
                salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
                # uzytkownik podaje ilosc nadgodzin 100%
                salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
              # suma nadgodzin 50% oraz 100% 
              salary_task["GODZINY_NADLICZBOWE"] =   salary_task["GODZINY_50"] +   salary_task["GODZINY_100"]
              nadgodziny.zapisz_stawka()
              skladki.zapisz_skladki()
              
              zapis_danych()
              print(dt.strftime("%B") + " " + rok_dt)
              print("PO ZAPISIE:",db.get(where("DATA") == dt.strftime("%B") + " " + rok_dt))
              premia_warunek(dt.strftime("%B"), rok_dt)
          
            else:
              urlop_db = salary_task["URLOP"]["DNI_URLOPU"]
              salary_task["DATA"] = dt.strftime("%B") + " " + rok_dt
              print("urlop_db",urlop_db)
              dni_pracy(dzien, int(miesiac_dt), dt, 0, urlop_db)
              print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
              salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
              salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
              salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
              salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
              print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
              if nadgodziny.nadgodziny(dt.strftime("%B") + " " + rok_dt):
                salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
                salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
                salary_task["GODZINY_NADLICZBOWE"] =   salary_task["GODZINY_50"] +   salary_task["GODZINY_100"]
              nadgodziny.zapisz_stawka()
              skladki.zapisz_skladki()
              
              zapis_danych()
              print(dt.strftime("%B") + " " + rok_dt)
              print("PO ZAPISIE:",db.get(where("DATA") == dt.strftime("%B") + " " + rok_dt))
              premia_warunek(dt.strftime("%B"), rok_dt)
          else:
            chr = salary_task["CZAS_CHOROBY"]["DNI_CHOROBOWEGO"]
            if urlop.czy_mial_urlop(miesiac_dt, rok_dt) == False:
              salary_task["DATA"] = dt.strftime("%B") + " " + rok_dt
              print("chr",chr)
              dni_pracy(dzien, int(miesiac_dt), dt, chr, 0)
              print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
              salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
              salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
              salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
              salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
              print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
          
          #salary_task[""]
              if nadgodziny.nadgodziny(dt.strftime("%B") + " " + rok_dt):
                salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
                salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
                salary_task["GODZINY_NADLICZBOWE"] = salary_task["GODZINY_50"] + salary_task["GODZINY_100"]
              nadgodziny.zapisz_stawka()
              skladki.zapisz_skladki()
              
              zapis_danych()
              print(dt.strftime("%B") + " " + rok_dt)
              print("PO ZAPISIE:",db.get(where("DATA") == dt.strftime("%B") + " " + rok_dt))
              premia_warunek(dt.strftime("%B"), rok_dt)
          
            else:
              urlop_db = salary_task["URLOP"]["DNI_URLOPU"]
              print("chr",chr,"urlop_db",urlop_db)
              salary_task["DATA"] = dt.strftime("%B") + " " + rok_dt
              dni_pracy(dzien, int(miesiac_dt), dt, chr, urlop_db)
              print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
              salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
              salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
              salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
              salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
              print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
              if nadgodziny.nadgodziny(dt.strftime("%B") + " " + rok_dt):
                salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
                salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
                salary_task["GODZINY_NADLICZBOWE"] = salary_task["GODZINY_50"] + salary_task["GODZINY_100"]
              nadgodziny.zapisz_stawka()
              skladki.zapisz_skladki()
              
              zapis_danych()
              print(dt.strftime("%B") + " " + rok_dt)
              print("PO ZAPISIE:",db.get(where("DATA") == dt.strftime("%B") + " " + rok_dt))
              premia_warunek(dt.strftime("%B"), rok_dt)


def dni_miesiaca_zatrudnienia():
  start_date = datetime.strptime((db.table("salary").get(q.DATA_ROZPOCZECIA_PRACY.exists())).get("DATA_ROZPOCZECIA_PRACY"), '%Y-%m-%d')
  
  miesiac_dt = start_date.strftime("%m")
  rok_dt = start_date.strftime("%Y")
  dzien_dt = start_date.strftime("%d")
  dzien = miesiac.numer_miesiac.dni_w_miesiacu(int(miesiac_dt))
    
  if not if_exist(start_date.strftime("%B") + " " + rok_dt):
        if chorobowe.czy_chorowal(miesiac_dt, rok_dt) == False:
          if urlop.czy_mial_urlop(miesiac_dt, rok_dt) == False:
            salary_task["DATA"] = start_date.strftime("%B") + " " + rok_dt
            salary_task["PRZEPRACOWANE_DNI"] = dni_pracujace.miesic_zatrudnienia(dzien, int(miesiac_dt), start_date.strftime("%Y-%m-%d"), dzien_dt)
            print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
            salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
            salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
            salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
            salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
            print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
          
          #salary_task[""]
            if nadgodziny.nadgodziny(start_date.strftime("%B") + " " + rok_dt):
              salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
              salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
              salary_task["GODZINY_NADLICZBOWE"] = salary_task["GODZINY_50"] + salary_task["GODZINY_100"]
            nadgodziny.zapisz_stawka()
            skladki.zapisz_skladki()
            
            zapis_danych()
            print(start_date.strftime("%B") + " " + rok_dt)
            print("PO ZAPISIE:",db.get(where("DATA") == start_date.strftime("%B") + " " + rok_dt))
            premia_warunek(start_date.strftime("%B"), rok_dt)
          
          else:
            urlop_db = salary_task["URLOP"]["DNI_URLOPU"]
            salary_task["DATA"] = start_date.strftime("%B") + " " + rok_dt
            print("urlop_db",urlop_db)
            salary_task["PRZEPRACOWANE_DNI"] = dni_pracujace.miesic_zatrudnienia(dzien, int(miesiac_dt), start_date.strftime("%Y-%m-%d"), dzien_dt) - urlop_db
            print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
            salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
            salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
            salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
            salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
            print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
            if nadgodziny.nadgodziny(start_date.strftime("%B") + " " + rok_dt):
              salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
              salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
              salary_task["GODZINY_NADLICZBOWE"] = salary_task["GODZINY_50"] + salary_task["GODZINY_100"]
            nadgodziny.zapisz_stawka()
            skladki.zapisz_skladki()
            
            zapis_danych()
            print(start_date.strftime("%B") + " " + rok_dt)
            print("PO ZAPISIE:",db.get(where("DATA") == start_date.strftime("%B") + " " + rok_dt))
            premia_warunek(start_date.strftime("%B"), rok_dt)
        else:
          chr = salary_task["CZAS_CHOROBY"]["DNI_CHOROBOWEGO"]
          if urlop.czy_mial_urlop(miesiac_dt, rok_dt) == False:
            salary_task["DATA"] = start_date.strftime("%B") + " " + rok_dt
            print("chr",chr)
            salary_task["PRZEPRACOWANE_DNI"] = dni_pracujace.miesic_zatrudnienia(dzien, int(miesiac_dt), start_date.strftime("%Y-%m-%d"), dzien_dt) - chr
            print("ilosc dni: ",salary_task.get("PRZEPRACOWANE_DNI"))
            salary_task["PRZEPRACOWANE_GODZINY"] = salary_task["PRZEPRACOWANE_DNI"] * 8
            salary_task["STAWKA_GODZINOWA"] = stawka.podstawa()
            salary_task["DODATEK_GODZINOWY"] = stawka.dodatek()
            salary_task["DOD_FUNKCYJNY"] = stawka.funkcyjne()
            print(type(salary_task["WYN_ZASADNICZE"]),salary_task["WYN_ZASADNICZE"],"/n",
                 type(salary_task["PRZEPRACOWANE_GODZINY"]))
          
          #salary_task[""]
            if nadgodziny.nadgodziny(start_date.strftime("%B") + " " + rok_dt):
              salary_task["GODZINY_50"] = nadgodziny.nadgodziny_50()
              salary_task["GODZINY_100"] = nadgodziny.nadgodziny_100()
              salary_task["GODZINY_NADLICZBOWE"] = salary_task["GODZINY_50"] + salary_task["GODZINY_100"]
            nadgodziny.zapisz_stawka()
            skladki.zapisz_skladki()
            
            zapis_danych()
            print(start_date.strftime("%B") + " " + rok_dt)
            print("PO ZAPISIE:",db.get(where("DATA") == start_date.strftime("%B") + " " + rok_dt))
            premia_warunek(start_date.strftime("%B"), rok_dt)
            
rozpoczecie_pracy()


#zapis_danych()





