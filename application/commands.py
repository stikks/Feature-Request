from application import app

with app.app_context():

    # import services needed
    from application.services import account, client, feature

    @app.cli.command()
    def setup_app():
        """
        setup application by creating dummy table entries

        create dummy employee account with
        username - ada@iws.com and
        password - lovelace
        :return:
        """
        # create new employee
        employee = account.register(**dict(
            email='ada@iws.com',
            first_name='Ada',
            last_name='Lovelace',
            password='lovelace'
        ))

        print(f'successfully created dummy employee account - {employee.first_name} {employee.last_name}')

        clients = ['Client A', 'Client B', 'Client C']
        for obj in clients:
            cs = client.ClientService.objects_new(**dict(name=obj))
            print(f'successfully created dummy client account - {cs.name}')

        product_areas = ['Policies', 'Billing', 'Claims', 'Reports']
        for area in product_areas:
            pa = feature.ProductAreaService.objects_new(**dict(title=area))
            print(f'successfully created dummy product areas - {pa.title}')

        return True
