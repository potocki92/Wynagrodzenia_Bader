import json
from tinydb import TinyDB
from tinydb import Query, where
from miesiac import numer_miesiac
from replace_str import replace_str
import dni_pracujace
import dateutil.relativedelta
from datetime import datetime
from stawka import stawka

db = TinyDB("salary_db.json")
db.default_table_name = "salary"
q = Query()

# dictionary do zapisywania wszystkich skladnikow odpowiedzialnych za wynagrodzenie
salary_task = {
    "DATA": "",
    "PRZEPRACOWANE_DNI": 0,
    "PRZEPRACOWANE_GODZINY": 0,
    "CHOROBOWE" : "NIE",
    "CZAS_CHOROBY" : 
    {
      "OD" : "0000-00-00",
      "DO" : "0000-00-00",
      "DNI_CHOROBOWEGO" : 0,
      "GODZINY_CHOROBOWE" : 0,
      "STAWKA_CHOROBOWE" : 0.0,
    },
    "URLOP" :
    {
      "OD" : "0000-00-00",
      "DO" : "0000-00-00",
      "DNI_URLOPU" : 0,
      "GODZINY_URLOP" : 0,
      "STAWKA_URLOP" : 0.0,
    },
    "STAWKA_GODZINOWA": 0.0,
    "WYN_ZASADNICZE": 0.0,
    "DODATEK_GODZINOWY": 0.0,
    "WYN_DODATEK": 0.0,
    "GODZINY_NADLICZBOWE": 0,
    "GODZINY_50": 0,
    "GODZINY_100": 0,
    "WYNA_ZA_NADGODZINY": 0.0,
    "DOD_NADGODZINY_100": 0.0,
    "DOD_NADGODZINY_50": 0.0,
    "DOD_STAN_ZA_NADGOD_T4": 0.0,
    "DOPLATA_50_DOD_T4": 0.0,
    "DOPLATA_100_DOD_T4": 0.0,
    "DOD_FUNKCYJNY": 0.0,
    "PREMIA": 0.0,
    "PODSTAWA_SKLADEK": 0.0,
    "EKWIWALENT_ZA_PRANIE": 0.0,
    "UBEZ_EMERYT_PRACOWN": 0.0,
    "UBEZ_RENTOWE_PRACOWN": 0.0,
    "UBEZ_CHOROB_PRACOWN": 0.0,
    "UBEZ_SPOLECZNE" : 0.0,
    "UBEZ_ZDROWOTNE": 0.0,
    "ULGA": 425.0,
    "PODATEK": 0.0,
    "KOSZTY": 250.0,
}

# funkcja do zapisu danych w dictionary
def zapis_danych():
  db.insert(salary_task)

# zwracanie bazy danych (db = TinyDB)
def db_tiny():
  return db


def q_tiny():
  print(db.search(where("DATA") == "February 2022"))
  if db.table("_default").search(where("DATA") == "February 2022"):
    pass

def if_chorobowe_tak(miesiac, rok):
  if db.table("salary").search(where("CHOROBOWE") == "TAK") and db.search(q.DATA == miesiac + " " + rok):
    print(db.table("salary").get(q.DATA == miesiac + " " + rok).get("CHOROBOWE"))
    return True
  else:
    return False
  #return db.tables("salary").db.search(where("DATA") == "FEBRUARY 2022")

def search_function(date):
  if numer_miesiac.data_str_do_datetime((db.table("salary").get(q.DATA_ROZPOCZECIA_PRACY.exists())).get("DATA_ROZPOCZECIA_PRACY")) > numer_miesiac.data_str_do_datetime(date):
    return False
  else:
    return True

# funkcja porownujaca istnienie takiej samej daty w 'salary_db.json' z 'value'
def if_exist(value):
  
  if db.search(q.DATA == value):
    print("ISTNIEJE")
    return True
  else:
    return False

# dane do zapisu w salary_task
# ilosc dni przepracowanych
def dni_pracy(dzien, miesiac_dt, dt, chr, urlop):
  # dni_pracujace wyliczaja dni, ktore uzytkownik przepracowal w danym miesiacu
    # dzien: ilosc dni w miesiacu
    # int(miesiac_dt): numer miesiaca
    # dt.strftime: podanie roku-miesiaca-dnia z datatime
    # chr: chorobowe
    # urlop: urlop uzytkownika
  salary_task["PRZEPRACOWANE_DNI"] = dni_pracujace.dni_pracujace(dzien, int(miesiac_dt), dt.strftime("%Y-%m-%d")) - chr - urlop

def print_dni_pracy(value):
  
  if db.search(q.DATA == value):
    print(value)
    s = db.table("salary").get(q.DATA == value)
    print("PRZEPRACOWANE_DNI: ",s.get("PRZEPRACOWANE_DNI"))

def premia_warunek(miesiac, rok):
  premia = stawka.premia(miesiac, rok)
  print("premia:",premia, "miesiac:",miesiac,"rok",rok)
  db.update({"PREMIA" : premia}, q.DATA == miesiac + " " + rok)


