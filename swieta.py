import holidays
import pandas as pd
from miesiac import numer_miesiac
from time import strptime
from dzien_tygodnia import dzien_tygodnia
from replace_str import replace_str 
from pd_timestamp import pd_timestamp

# funkacja sprawdza czy swieta wystepuja w innych dniach, niz weekend
def swieta_polska(data):
  
  for date in holidays.Poland(years=2022).items():
    
    numer_miesiaca_date = int(strptime(str((pd_timestamp(date[0])).strftime("%B")),'%B').tm_mon)
    
    if numer_miesiaca_date == numer_miesiac.miesiac(data):
      if dzien_tygodnia(str(date[0])) <= 5 and data == replace_str(date[0]):
        print(date)
        return True
      
  return False




