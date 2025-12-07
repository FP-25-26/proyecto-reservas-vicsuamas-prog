from typing import NamedTuple
from datetime import datetime,date
import calendar
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

            fecha_entrada, fecha_salida= datetime.strptime(fecha_entrada,"%Y-%m-%d").date(),datetime.strptime(fecha_salida,"%Y-%m-%d").date()
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

def reservas_mas_largas(reservas: list[Reserva], n: int = 3) -> list[tuple[str, date]]:
    '''
    Devuelve las n reservas mas largas con el nombre del husped y la su fecha de entrada
    
    :param reservas: lista de tuplas de tipo Reserva
    :type reservas: list[Reserva]
    :param n: número de reservas a mostrar después del filtrado
    :type n: int
    :return: lista con las n reservas deseadas 
    :rtype: list[tuple[str, date]]
    '''

    reservas_plus = sorted([(reserva.nombre,reserva.fecha_entrada,reserva.fecha_salida - reserva.fecha_entrada) for reserva in reservas] ,key = lambda x: x[2],reverse = True)
    return [(x[0],x[1]) for x in reservas_plus][:n]

def cliente_mayor_facturacion(reservas: list[Reserva],servicios: set[str] | None = None) -> tuple[str, float]:
    '''
    Devuelve el cliente con más facturación en el hotel con un filtro de servicios y esa facturación
    
    :param reservas: lista de tuplas de tipo Reserva
    :type reservas: list[Reserva]
    :param servicios: conjunto de servicios a filtrar
    :type servicios: set[str] | None
    :return: Description
    :rtype: tuple[str, float]
    '''
    res = [(dni,sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas if reserva.dni == dni )) 
               for dni in {reserva.dni for reserva in reservas}]
    
    if servicios != None:
        hss = [(dni,sum(reserva.precio_noche * (reserva.fecha_salida - reserva.fecha_entrada).days for reserva in reservas if reserva.dni == dni ),reserva.servicios_adicionales) 
               for dni in {reserva.dni for reserva in reservas} for reserva in reservas]
        
        res = [(cliente[0],cliente[1]) for cliente in hss if bool(servicios &  set(cliente[2]))]
        
    return max(res,key=lambda x : x[1]) #Error en el Test

def servicios_estrella_por_mes(reservas: list[Reserva], tipos_habitacion: set[str] | None = None) -> dict[str, str]:

    '''
    Devuelve un diccionario con el servicio estrella del mes de todos los tipos de habitaciones o unos tipos concretos
    
    :param reservas: lista de tuplas de tipo Reserva
    :type reservas: list[Reserva]
    :param tipos_habitacion: tipos de habitaciones a filtrar
    :type tipos_habitacion: set[str] | None
    :return: diccionario con los servicios estrella de cada mes
    :rtype: dict[str, str]
    '''

    n_meses = set(range(1,13))
    meses = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio","julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    servicios_mes = [(meses[mes],[servicio for reserva in reservas if reserva.fecha_entrada.month == mes 
                                  for servicio in reserva.servicios_adicionales]) for mes in n_meses]
    
    if tipos_habitacion != None:

        servicios_mes = [(meses[mes],[servicio for reserva in reservas if reserva.fecha_entrada.month == mes and reserva.tipo_habitacion in tipos_habitacion
                                  for servicio in reserva.servicios_adicionales]) for mes in n_meses]
        
    res = {mes[0] : max(mes[1],key = mes[1].count) for mes in servicios_mes}
        
    return res


def media_dias_entre_reservas(reservas: list[Reserva]) -> float:
    '''
    Devuelve la media de dias entre cada dos reservas (¿tasa de ocupación?)
    
    :param reservas: lista de tuplas de tipo Reserva
    :type reservas: list[Reserva]
    :return: media
    :rtype: float
    '''
    reservas_ordenadas = sorted(reservas, key = lambda x : x.fecha_entrada)
    medias= [(reservas_ordenadas[i+1].fecha_entrada - reservas_ordenadas[i].fecha_entrada).days for i in range(len(reservas_ordenadas) -1)]

    return sum(medias) / len(medias)

def cliente_reservas_mas_seguidas(reservas: list[Reserva], min_reservas: int) -> str:
    '''
    Devuelve el DNI y la media de días entre reservas consecutivas del cliente con al menos `min_reservas` y menor media de días entre reservas.

    :param reservas: lista de tuplas de tipo Reserva
    :type reservas: list[Reserva]
    :param min_reservas: min de reservas para el cliente
    :type min_reservas: int
    :return: cadena con la media, el minimo de reservas y la menor media entre reservas
    :rtype: str
    '''
 
    reservas_por_cliente = [(cliente, sum(1 for reserva in reservas if reserva.dni == cliente ),[reserva for reserva in reservas if reserva.dni == cliente]) 
                            for cliente in {reserva.dni for reserva in reservas}] # (cliente, num reservas , dichas reservas)
    
    filtro_min = [elemento for elemento in reservas_por_cliente if min_reservas <= elemento[1]] #filtro de numero de reservas

    reservas_ordenadas_por_cliente = [(elemento[0],(sorted(elemento[2],key = lambda x : x.fecha_entrada))) for elemento in filtro_min] #reservas ordenadas por fecha

    medias_por_cliente = [(elemento[0],[(elemento[1][i+1].fecha_entrada - elemento[1][i].fecha_salida).days for i in range(len(elemento[1])-1)]) #listas de medias entre dos reservas consecutivas
                          for elemento in reservas_ordenadas_por_cliente]
    
    cliente_elegido = min(((elemento[0],sum(elemento[1])/len(elemento[1])) for elemento in medias_por_cliente), key = lambda x : x[1]) #min de la media de las medias


    return f"El DNI del cliente con al menos {min_reservas} reservas y menor media de días entre reservas consecutivas es  \
    {cliente_elegido[0]}, con una media de días entre reservas de {cliente_elegido[1]}."
