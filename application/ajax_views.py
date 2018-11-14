"""
ajax route endpoints
"""
from flask import current_app, request, jsonify

from .services import client, feature
from . import schemas


@current_app.route('/ajax/clients', methods=['GET'])
def ajax_clients_list():
    """
    returns json response of client list
    :return:
    """

    if not request.is_xhr:
        return jsonify({'error': 'Method not Allowed'}), 405

    client_schema = schemas.ClientSchema()

    data = client_schema.dump(client.ClientService.objects_all(), many=True).data

    return jsonify({
        'aaData': [[c.get('name'), c.get('slug')] for c in data]
    }), 200


@current_app.route('/ajax/<client_slug>/feature-requests', methods=['GET'])
def ajax_feature_requests_list(client_slug):
    """
    returns json response of client list
    :return:
    """

    if not request.is_xhr:
        return jsonify({'error': 'Method not Allowed'}), 405

    client_obj = client.ClientService.objects_filter(**dict(slug=client_slug))

    if not client_obj:
        return jsonify({'error': 'Client not found'}), 404

    feature_schema = schemas.FeatureRequestSchema()

    data = feature_schema.dump(feature.FeatureRequestService.objects_filter(first_only=False, order_by='priority', 
        order_direction='asc', **dict(client_id=client_obj.id)), many=True).data

    return jsonify({
        'aaData': [[c.get('title'), c.get('description'), c.get('client')['name'], c.get('priority'), c.get('target_date'), 
        c.get('product_area')['title']]  for c in data]
    }), 200
