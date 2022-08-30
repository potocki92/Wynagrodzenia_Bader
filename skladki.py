from salary_dictionary import salary_task

def podstawa_skladek():
  
  salary_task["PODSTAWA_SKLADEK"] = float("{:.2f}".format(salary_task["WYN_ZASADNICZE"] + salary_task["WYN_DODATEK"] + salary_task["DOD_NADGODZINY_50"] + salary_task["DOD_NADGODZINY_100"] + salary_task["DOD_STAN_ZA_NADGOD_T4"] + salary_task["DOPLATA_50_DOD_T4"] + salary_task["DOPLATA_100_DOD_T4"] + salary_task["PREMIA"] + salary_task["WYNA_ZA_NADGODZINY"]))

def wyliczenie_podatku():
  salary_task["UBEZ_EMERYT_PRACOWN"] = float("{:.2f}".format(((19.52 / 100) * salary_task["PODSTAWA_SKLADEK"]) / 2))
  salary_task["UBEZ_RENTOWE_PRACOWN"] = float("{:.2f}".format((1.5 / 100) * salary_task["PODSTAWA_SKLADEK"]))
  salary_task["UBEZ_CHOROB_PRACOWN"] = float("{:.2f}".format((2.45 / 100) * salary_task["PODSTAWA_SKLADEK"]))
  
  salary_task["UBEZ_SPOLECZNE"] = float("{:.2f}".format(salary_task["UBEZ_EMERYT_PRACOWN"] + salary_task["UBEZ_RENTOWE_PRACOWN"] + salary_task["UBEZ_CHOROB_PRACOWN"]))
  
  salary_task["UBEZ_ZDROWOTNE"] = float("{:.2f}".format((9 / 100) * (salary_task["PODSTAWA_SKLADEK"] - salary_task["UBEZ_SPOLECZNE"])))
  
  salary_task["PODATEK"] = float("{:.2f}".format(((salary_task["PODSTAWA_SKLADEK"] - salary_task["UBEZ_SPOLECZNE"] - salary_task["KOSZTY"]) * (17 / 100)) - salary_task["ULGA"]))

def zapisz_skladki():
  podstawa_skladek()
  wyliczenie_podatku()
  