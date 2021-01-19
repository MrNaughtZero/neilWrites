import datetime as dt

def queryDate():
    x = dt.datetime.now()
    return x.strftime("%A, %B %d")