def dni_tygodnia(temp, dni_tygodnia):
  if temp <= dni_tygodnia:
    return 1
  else:
    return 0

def weekend(temp):
  if temp > 5 or temp == 7:
    return 1
  else:
    return 0