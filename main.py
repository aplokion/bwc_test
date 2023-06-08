from pysnmp.hlapi import *
from datetime import datetime
from cfg import LOS_STATUS, OFFLINE_STATUS
from device1 import SNMPDevice
import time


def snmp_get(device_id, oid):
    device = SNMPDevice(device_id)
    # По сути код ниже до 28й строчки(включительно) бесполезен в контексте симмуляции оборудования python классом,
    # но имеет смысл, если поднять сервер локально, который будет выступать в качетсве оборудования
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('localhost', 161), timeout=10, retries=0),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f"{errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            value = varBind[1]
            # Здесь мы преобразуем полученное значение в строку и отправляем ловушку с полученным значением.
            trap = f"{oid}={str(value)}"
            device.send_trap(trap)
    result = device.get_data(oid)
    device.conn.close()
    return result


def get_timing(los_time):
    current_time = datetime.now()
    time_difference = current_time - los_time
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours} часов {minutes} минут простоя"


def find_troubles(data):
    troubles = []
    for i in data:
        los_macs = []
        for j in i[1]:
            los_macs += [[k[0], get_timing(datetime.strptime(k[3], '%Y-%m-%d %H:%M:%S'))] for k in j[1] if k[2] == LOS_STATUS]
        if len(los_macs) > 3:
            troubles.append([f"Простой из-за сбоя на LOT порте {i[0]}", los_macs])
    for i in data:
        for j in i[1]:
            los_macs_m = [[k[0], get_timing(datetime.strptime(k[3], '%Y-%m-%d %H:%M:%S'))] for k in j[1] if k[2] == OFFLINE_STATUS]
            if len(los_macs_m) > len(j)/2:
                troubles.append([f"Простой из-за сбоя на муфте {j[0]}", los_macs_m])
    return troubles


while True:
    data = snmp_get('device1', "1.3.6.1.2.1.1.5.0")
    troubles = find_troubles(data)
    for trouble in troubles:
        print(trouble[0])
        for t in trouble[1]:
            print("     Клиент: ", t[0])
            print("             ", t[1])
    time.sleep(600)