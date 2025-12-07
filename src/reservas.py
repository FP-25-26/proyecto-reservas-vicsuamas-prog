from typing import NamedTuple
from datetime import datetime,date

import csv

Reserva = NamedTuple("Reserva", 
                     [("nombre", str),
                      ("dni", str),
                      ("fecha_entrada", date),
                      ("fecha_salida", date),
                      ("tipo_habitacion", str),
                      ("num_personas", int),
                      ("precio_noche", float),
                      ("servicios_adicionales", list[str])
                    ])

def lee_reservas(ruta_fichero: str) -> list[Reserva]:
    '''
    Letura del CSV con los datos de las reservas del hotel
    
    :param ruta_fichero: ruta del archivo
    :type ruta_fichero: str
    :return: reservas organizadas
    :rtype: list[Reserva]
    '''
    lista= []
    with open(ruta_fichero,encoding='UTF-8') as f:
        lector = csv.reader(f)
        next(lector)

        for nombre,dni,fecha_entrada,fecha_salida,tipo_habitacion,num_personas,precio_noche,servicios_adicionales in lector:

            fecha_entrada, fecha_salida= datetime.strptime(fecha_entrada,"%Y-%m-%d"),datetime.strptime(fecha_salida,"%Y-%m-%d")
            num_personas,precio_noche = int(num_personas),float(precio_noche)

            if bool(servicios_adicionales):
                servicios_adicionales = servicios_adicionales.split(",")
            else:
                servicios_adicionales = []

            tupla = Reserva(nombre,dni,fecha_entrada,fecha_salida,tipo_habitacion,num_personas,precio_noche,servicios_adicionales)
            lista.append(tupla)

    return lista

def total_facturado(reservas: list[Reserva], fecha_ini: date | None = None, fecha_fin: date | None = None) -> float:
    '''
    Calcula la cantidad facturada entre dos fechas
    
    :param reservas: Description
    :type reservas: list[Reserva]
    :param fecha_ini: Description
    :type fecha_ini: date | None
    :param fecha_fin: Description
    :type fecha_fin: date | None
    :return: Description
    :rtype: float
    '''

    if fecha_ini == None and fecha_fin == None:
        res = sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas)

    elif fecha_ini == None:
        res = sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas if reserva.fecha_salida < fecha_fin )

    elif fecha_fin == None:
        res = sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas if reserva.fecha_entrada > fecha_ini)

    else: 
        res = sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas if reserva.fecha_salida < fecha_fin and reserva.fecha_entrada > fecha_ini)

        return res
    
    #No funciona correctamente ( solo cuando recibe dos fechas y no da la cantidad correcta) 
    #Se introduce bien en el bloque if, toma correctamente los parametros opcionales, la resta de fechas es correcta, obtiene correctamente los dias con .days, 
    #ningun error a la hora de multiplicar por el precio por noche, ningun error  al acceder a la lista de Reservas...
    #MODO DEBUG = el generador devuelve None ¿por que?
