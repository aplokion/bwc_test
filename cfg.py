OLT_PORTS = ['3206', '3207']

ID_UZELS_FOR_OLT_PORTS = [[1, 2, 3], [4, 5]]


def get_query(uzel_id):
    return f'select t2.mac, t3.onu_port, t3.status, t3.updated_at from uzel as t1 left join client as t2 on ' \
           f't2.uzel_id = t1.id left join client_has_status as t3 on t3.client_id = t2.id where t1.id = {uzel_id}'


WORKING_STATUS = 'working'
LOS_STATUS = 'los'
DYING_STATUS = 'dying gasp'
OFFLINE_STATUS = 'offline'
