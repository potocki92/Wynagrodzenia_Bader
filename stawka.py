import dateutil.relativedelta
from datetime import datetime
from tinydb import TinyDB
from tinydb import Query, where

db = TinyDB("salary_db.json")
db.default_table_name = "salary"
q = Query()

class stawka():
  def podstawa():
    return float(input('Podaj podstawę: '))
  def dodatek():
    return float(input('Podaj dodatek: '))

  def funkcyjne():
    return 400.00

  # funkcja do sprawdzania oraz zwracania innej wartosci zaleznej od czasu chorobowego
    # jezeli uzytkownik nie chorowal: 400
    # jezeli uzytkownik chorowal miesiac wczesniej: 200
    # jezeli uzytkownik chorowal w danym miesiacu: 0
  def premia(miesiac, rok):
    value = miesiac + " " + rok
    numer_miesiaca = datetime.strptime(miesiac, "%B").strftime("%m")
    numer_miesiaca = datetime.strptime((rok + "-" + numer_miesiaca),"%Y-%m")
    print("MIESIAC NR:",numer_miesiaca)
    miesiac_wcześnieszy = numer_miesiaca + dateutil.relativedelta.relativedelta(months=-1)
    print("MIESIAC WCZEŚNIEJ",miesiac_wcześnieszy)

    numer_miesiaca_wczesniejszego = miesiac_wcześnieszy.strftime("%B %Y")

    print("NR. MIESIACA WCZESNIEJSZEGO:",numer_miesiaca_wczesniejszego)
    date_wczesniej = db.table("salary").get(where("DATA") == numer_miesiaca_wczesniejszego)
    date = db.table("salary").get(where("DATA") == value)
    
    #print("PRINT",date_wczesniej.get("DATA"), date_wczesniej.get("CHOROBOWE"))
    
    if date.get("CHOROBOWE") == "TAK":
      return 0.0
      
    if db.search(q.DATA == date_wczesniej.get("DATA")):
      
      if date.get("CHOROBOWE") == "NIE" and date_wczesniej.get("CHOROBOWE") == "TAK":
        return 200.00
        
      else:
        return 400.00