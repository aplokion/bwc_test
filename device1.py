import sqlite3

from cfg import get_query, ID_UZELS_FOR_OLT_PORTS, OLT_PORTS


class SNMPDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.oid = "1.3.6.1.2.1.1.5.0"
        self.conn = sqlite3.connect('bwc.db')
        self.cursor = self.conn.cursor()

    def query(self):
        data = []
        for i in range(len(OLT_PORTS)):
            tmp = []
            for uzel_id in ID_UZELS_FOR_OLT_PORTS[i]:
                self.cursor.execute(get_query(uzel_id))
                tmp.append([uzel_id, self.cursor.fetchall()])
            data.append([OLT_PORTS[i], tmp])
            tmp = []
        return data

    def get_data(self, oid):
        result = self.query()
        if self.oid == oid:
            return result
        else:
            return None

    def send_trap(self, trap):
        # Здесь происходит имитация отправки ловушки.
        # В реальности здесь должен быть код для отправки ловушки на устройство с помощью SNMP.
        print(f"Sending trap {trap} to device {self.device_id}")