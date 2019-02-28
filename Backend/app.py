import os
import json
import requests
import time
from flask import Flask, request
from query_sort import clean_text, sort_query

app = Flask(__name__)
count = 0
data = {
    'transformers': json.load(open('db/transformers.json')),
    'inventory': json.load(open('db/transformers.json')),
    'ticket': json.load(open('db/tickets.json')),
    'health-history': json.load(open('db/health-history.json'))
}


# Views
@app.route('/', methods=['GET'])
def base_index():
    return "Home Page for edge-triggered", 200


@app.route('/transformers', methods=['GET'])
def get_transformer_list():
    return data['transformers'], 200


@app.route('/inventory', methods=['GET'])
def get_inventory_list():
    return data['inventory'], 200


@app.route('/tickets', methods=['GET'])
def get_tickets_list():
    return data['tickets'], 200


@app.route('/tickets-per-transformer', methods=['GET'])
def get_tickets_per_transformer_list(t_id):
    tickets = {}
    
    for ticket_id, ticket_value in data['tickets'].items():
        if ticket_id = t_id:
            tickets[ticket_id] = ticket_value

    return tickets, 200

@app.route('/health-history', methods=['GET'])
def get_health_history_list():
    return data['health-history'], 200


@app.route('/unresolved-tickets', methods=['GET'])
def get_unresolved_tickets():
    unresolved_tickets = {}
    
    for ticket_id, ticket_data in data['tickets'].items():
        if not ticket_data['is_resolved']:
            unresolved_tickets[ticket_id] = ticket_data

    return unresolved_tickets, 200


@app.route('/low-inventory', methods=['GET'])
def get_low_inventory():
    low_inventory = {}
    
    for inv_name, inv_data in data['inventory'].items():
        if inv_data['amount'] < inv_data['threshold']:
            low_inventory[inv_name] = inv_data

    return low_inventory, 200


# updates
@app.route('/update-transformers', methods=['GET'])
def update_transformers_list(t_id, new_data):
    for new_key, new_value in new_data.items():
        data['transformers'][t_id][new_key] = new_value

    update_health_history(t_id, new_data['health'])
    return "ok", 200


@app.route('/update-inventory', methods=['GET'])
def update_inventory_list(product_count_json):
    for product, count in product_count_json.items():
        data['inventory'][product][new_key] = new_value

    return "ok", 200


@app.route('/update-ticket', methods=['GET'])
def update_ticket_list(t_id, ticket_data):
    for ticket_data_key, ticket_data_value in ticket_data.items():
        data['tickets'][t_id][ticket_data_key] = ticket_data_value

    update_inventory_list(ticket_data['products-used'])
    return "ok", 200


@app.route('/update-health', methods=['GET'])
def update_health(t_id, health_data):
    for health_data_key, health_data_value in health_data.items():
        data['health-history'][t_id][health_data_key][time.ctime()] = ticket_data_value
    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)