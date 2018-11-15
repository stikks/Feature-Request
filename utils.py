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


def create_test_dummy_data():
    """
    insert dummy records
    :return:
    """

    # insert dummy employee, client and product area
    # records
    create_dummy_data()

    # insert first dummy feature request data
    feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea',
        description='Design new page for nivea cream product',
        product_area_id=1,
        priority=1,
        target_date=date.today() + timedelta(days=20)
    )

    # insert second dummy feature request data
    feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea Oil',
        description='Design new page for nivea oil product',
        product_area_id=2,
        priority=1,
        target_date=date.today() + timedelta(days=30)
    )

    return True
