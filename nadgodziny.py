from salary_dictionary import salary_task

class nadgodziny():
  def nadgodziny(miesiac):
    nad = input("Miałeś nadgodziny w tym miesiącu ({})? ".format(miesiac)).upper()

    if nad == "TAK":
      return True
    else:
      return False
      
  def nadgodziny_50():
    return int(input("Podaj ilość nadgodzin 50%: "))
    
  def nadgodziny_100():
    return int(input("Podaj ilość nadgodzin 100%: "))

  def wynagrodzenie_za_nadgodziny():
    salary_task["WYNA_ZA_NADGODZINY"] = float("{:.2f}".format((salary_task["WYN_ZASADNICZE"] + salary_task["DOD_FUNKCYJNY"]) / salary_task["PRZEPRACOWANE_GODZINY"] * salary_task["GODZINY_NADLICZBOWE"]))

    print(type(salary_task["WYNA_ZA_NADGODZINY"]))
    
  def wynagrodzenie_dodatek():
    salary_task["WYN_DODATEK"] = float("{:.2f}".format(salary_task["PRZEPRACOWANE_GODZINY"] * salary_task["DODATEK_GODZINOWY"]))

  def doplata_50_dodatek():
    salary_task["DOPLATA_50_DOD_T4"] = float("{:.2f}".format((salary_task["GODZINY_50"] / 2) * salary_task["DODATEK_GODZINOWY"]))
    
  def doplata_50_podstawa():
    salary_task["DOD_NADGODZINY_50"] = float("{:.2f}".format((salary_task["GODZINY_50"] / 2) * salary_task["STAWKA_GODZINOWA"]))
    
  def doplata_100_dodatek():
    salary_task["DOPLATA_100_DOD_T4"] = float("{:.2f}".format(salary_task["GODZINY_100"] * salary_task["DODATEK_GODZINOWY"]))
    
  def doplata_100_podstawa():
    salary_task["DOD_NADGODZINY_100"] = float("{:.2f}".format(salary_task["GODZINY_100"] * salary_task["STAWKA_GODZINOWA"]))
    
  def doplata_nadgodzin():
    salary_task["DOD_STAN_ZA_NADGOD_T4"] = float("{:.2f}".format(salary_task["GODZINY_NADLICZBOWE"] * salary_task["DODATEK_GODZINOWY"]))

  def wynagrodzenie_podstawa():
    salary_task["WYN_ZASADNICZE"] = float("{:.2f}".format(salary_task["PRZEPRACOWANE_GODZINY"] * salary_task["STAWKA_GODZINOWA"]))
    
  def zapisz_stawka():
    nadgodziny.wynagrodzenie_podstawa()
    nadgodziny.wynagrodzenie_dodatek()
    nadgodziny.doplata_50_podstawa()
    nadgodziny.doplata_50_dodatek()
    nadgodziny.doplata_100_podstawa()
    nadgodziny.doplata_100_dodatek()
    nadgodziny.doplata_nadgodzin()
    nadgodziny.wynagrodzenie_za_nadgodziny()