from datetime import date, timedelta

from application.core.services import client, feature
from application.core.services import account


def create_dummy_data():
    """
    insert dummy records
    :return:
    """
    employee = account.register(**dict(
        email='ada@iws.com',
        first_name='Ada',
        last_name='Lovelace',
        password='lovelace'
    ))

    print(f'successfully created dummy employee account - {employee.first_name} {employee.last_name}')

    clients = ['Client A', 'Client B', 'Client C']
    for obj in clients:
        client_service = client.ClientService.objects_new(**dict(name=obj))
        print(f'successfully created dummy client account - {client_service.name}')

    product_areas = ['Policies', 'Billing', 'Claims', 'Reports']
    for area in product_areas:
        product_area = feature.ProductAreaService.objects_new(**dict(title=area))
        print(f'successfully created dummy product areas - {product_area.title}')

    return True
