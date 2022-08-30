from pd_timestamp import pd_timestamp


def replace_str(data):
  return str(pd_timestamp(data)).replace('00:00:00','').replace(' ','')
