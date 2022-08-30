import pandas as pd

def dzien_tygodnia(date_cnt):
  temp = pd.Timestamp(date_cnt)
  day_of_week = temp.weekday() + 1

  return day_of_week