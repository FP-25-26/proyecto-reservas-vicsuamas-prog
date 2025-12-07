from reservas import *
from datetime import datetime,date

def main():
    ruta = "./data/reservas.csv"
    datos = lee_reservas(ruta)
    #test_lee_reservas(ruta)
    #test_total_facturado(datos)
    #test_reservas_mas_largas(datos)
    #test_cliente_mayor_facturacion(datos)
    #test_servicios_estrella_por_mes(datos)
    #test_media_dias_entre_reservas(datos)
    print(cliente_reservas_mas_seguidas(datos,5))

def test_lee_reservas(ruta):
    datos = lee_reservas(ruta)
    print("TEST de lee_recetas")
    print("Registros leidos : ", len(datos))
    print("Mostrando los tres primeros",datos[:3])

def test_total_facturado(datos):
    fecha_ini = datetime.strptime("2022-2-1","%Y-%m-%d")
    fecha_fin = datetime.strptime("2022-2-28","%Y-%m-%d")
    print("TEST de total_facturado")
    print("En todo el periodo de datos: ",total_facturado(datos,None,None))
    print("Desde 1 de febrero de 2022 hasta 28 de febrero de 2022:",total_facturado(datos,fecha_ini,fecha_fin))
    print("Desde 1 de febrero de 2022 (fecha final None):", total_facturado(datos,fecha_ini,None))
    print("Hasta 28 de febrero de 2022 (fecha inicio None):",total_facturado(datos,None,fecha_ini))

def test_reservas_mas_largas(datos):
    print("TEST de reservas_mas_largas")
    print("Con n=3 : ",reservas_mas_largas(datos))

def test_cliente_mayor_facturacion(datos):
    print("TEST de cliente_mayor_facturacion")
    print("Sin flitrar por servicios: ", cliente_mayor_facturacion(datos))
    print("Con parking: ",cliente_mayor_facturacion(datos,{"Parking",}))
    print("Con parking o spa : ",cliente_mayor_facturacion(datos,{"Parking","Spa"}))

def test_servicios_estrella_por_mes(datos):
    print("TEST de servicio_estrella_por_mes")
    print("Todos los tipos de habitación: ",servicios_estrella_por_mes(datos))
    print("Habitación familiar o deluxe: ",servicios_estrella_por_mes(datos,{"Deluxe","Familiar"}))

def test_media_dias_entre_reservas(datos):
    print("TEST de media_dias_entre_reservas",media_dias_entre_reservas(datos))


if __name__ == '__main__':
    main()
    