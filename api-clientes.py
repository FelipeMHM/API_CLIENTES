import json
from flask import Flask, jsonify, request

app = Flask(__name__)

clientes = [
  { 'id': 1, 'nome': 'José' },
  { 'id': 2, 'nome': 'João' },
  { 'id': 3, 'nome': 'Francisco' },
  { 'id': 4, 'nome': 'Felipe' }
]

nextClienteId = 5

@app.route('/cliente', methods=['GET'])
def get_clientes():
  return jsonify(clientes)

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente_by_id(id: int):
  cliente = get_cliente(id)
  if cliente is None:
    return jsonify({ 'error': 'Cliente não existe'}), 404
  return jsonify(cliente)

def get_cliente(id):
  return next((e for e in clientes if e['id'] == id), None)

def cliente_is_valid(cliente):
  for key in cliente.keys():
    if key != 'nome':
      return False
  return True

@app.route('/cliente', methods=['POST'])
def create_cliente():
  global nextClientesId
  cliente = json.loads(request.data)
  if not cliente_is_valid(cliente):
    return jsonify({ 'error': 'Propriedades de cliente inválidas.' }), 400

  cliente['id'] = nextClienteId
  nextClienteId += 1
  clientes.append(cliente)

  return '', 201, { 'location': f'/clientes/{cliente["id"]}' }

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id: int):
  cliente = get_cliente(id)
  if cliente is None:
    return jsonify({ 'error': 'Cliente não existe.' }), 404

  updated_cliente = json.loads(request.data)
  if not cliente_is_valid(updated_cliente):
    return jsonify({ 'error': 'Propriedades de cliente inválidas.' }), 400

  cliente.update(updated_cliente)

  return jsonify(cliente)

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id: int):
  global clientes
  cliente = get_cliente(id)
  if cliente is None:
    return jsonify({ 'error': 'Cliente não existe.' }), 404

  clientes = [e for e in clientes if e['id'] != id]
  return jsonify(cliente), 200

app.run()