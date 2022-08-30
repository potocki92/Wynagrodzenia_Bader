import miesiac
import pandas as pd
import dzien_tygodnia
import dni_tygodnia
import swieta
from replace_str import replace_str

def miesic_zatrudnienia(dni, miesiac_zatrudnienia, data, dzien):
  dni_przepracowane = 0
  #print(str(miesiac.numer_miesiac.rok(data)) + '-' + str(akt_miesiac))
  print(dni, miesiac_zatrudnienia, data, dzien)
  for i in range(int(dzien), dni + 1):

    
    podana_data = str(miesiac.numer_miesiac.rok(data)) + '-' + str(miesiac_zatrudnienia) + '-' + str(i)

    temp = pd.Timestamp(podana_data)
    day_of_week = temp.weekday() + 1
    
    if day_of_week <= 5:
      if swieta.swieta_polska(replace_str(str(temp))) == True:
        pass
      else:
        print(podana_data)
        dni_przepracowane += 1
           
  return dni_przepracowane


def dni_pracujace(dni, akt_miesiac, data):
  dni_przepracowane = 0
  #print(str(miesiac.numer_miesiac.rok(data)) + '-' + str(akt_miesiac))
  for i in range(1, dni + 1):

    podana_data = str(miesiac.numer_miesiac.rok(data)) + '-' + str(akt_miesiac) + '-' + str(i)

    temp = pd.Timestamp(podana_data)
    day_of_week = temp.weekday() + 1
    
    if day_of_week <= 5:
      if swieta.swieta_polska(replace_str(str(temp))) == True:
        pass
      else:
        dni_przepracowane += 1
           
  return dni_przepracowane

