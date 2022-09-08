import datetime

def miFecha():
    x = datetime.datetime.now()
    y = x.strftime("%x")
    y = y.replace('/','_')
    z= x.strftime("%X")
    z = z.replace(':','_')
    fecha = str(f"{y}_{z}")
    return str(fecha)

