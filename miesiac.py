import datetime
import calendar
from dateutil import rrule

class numer_miesiac():

  def data_dzisiaj_nazwa():
    return datetime.datetime.now().strftime("%B %Y")

  def data_dzisiaj():
    return datetime.datetime.now().strftime("%Y-%m-%d")

  def data_wczesniejsze(data):
    return numer_miesiac.nazwa_miesiaca(data) + " " + numer_miesiac.rok(data)
    
  def data_str_do_datetime(data):
    return datetime.datetime.strptime(data, '%Y-%m-%d')

  def data_str_do_datetime_z_czasem(data):
    return datetime.datetime.strptime(data, '%Y-%m-%d, %H:%M:%S')

  def rok(data):
    return numer_miesiac.data_str_do_datetime(data).strftime("%Y")
    
  def miesiac(data):
    return int(numer_miesiac.data_str_do_datetime(data).strftime("%m"))
    
  def nazwa_miesiaca(data):
    return str(numer_miesiac.data_str_do_datetime(data).strftime("%B"))

  def nazwa_miesiaca_strptime(data):
    return datetime.datetime.strftime(datetime.datetime.strptime(str(data), '%m'), "%B")
    
  def dni_w_miesiacu(data):
    dni_w_miesiacu = calendar.monthrange(2022, data)[1]
    return dni_w_miesiacu

  def petla_miesiac():
    start_date = datetime.datetime.strptime("2022-01-02", '%Y-%m-%d')
    end_date = datetime.datetime.today()
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
      print(dt)