from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
from flask_mysqldb import MySQL
from backend import functions as f
from backend import db_classes as c
from backend import db_config as db_config

#global variables
page_index = 'home'
page_customer_registration = 'register'
page_customer_search = 'search'
page_vehicle_registration = 'vehicle_registration'

app = Flask(__name__)
app.config['MYSQL_USER'] = db_config.user
app.config['MYSQL_PASSWORD'] = db_config.password
app.config['MYSQL_DB'] = db_config.db
app.config['MYSQL_HOST'] = db_config.host
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return render_template(f'{page_index}.html')

@app.route(f'/{page_customer_registration}/', methods=['GET','POST'])
def register():
    status_code=599
    if request.method == 'GET':
        return render_template(f'{page_customer_registration}.html')
    try:
        nome = request.form['nome']
        cpf = request.form['cpf']
        razao_social = request.form['razao_social']
        cnpj = request.form['cnpj']
        celular = request.form['telefone']
        email = request.form['email']
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        numero = request.form['numero']
        complemento = request.form['complemento']
        estado = request.form['estado']
        cidade = request.form['cidade']
        telefone = celular
        endereco = f'{logradouro};;{numero};;{complemento};;{cidade};;{estado};;{cep}'
        if ((nome and cpf) or (razao_social and cnpj)) and telefone and email and cep:
            status_code=550
            cliente_encontrado = f.pesquisar_cliente(cpf,cnpj)
            if (len(cliente_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                novo_cliente = c.Cliente(cpf = cpf, cnpj = cnpj, nome = nome, razao_social = razao_social, endereco = endereco, telefone = telefone, email = email)
                novo_cliente.salvar()
                try:
                    cliente_confirmado = f.pesquisar_cliente(cpf,cnpj)[0]
                    # return render_template(f'{page_customer_registration}.html', resposta_cliente = cliente_confirmado.enviar), 200
                    # return redirect(url_for('exibir_cliente', id_cliente = cliente_confirmado.id_cliente)), 200
                    return jsonify(cliente_confirmado), 200
                    
                except:
                    return render_template(f'{page_customer_registration}.html'), 552
        else:
            status_code=460
            raise
    except:
        return render_template(f'{page_customer_registration}.html'), status_code

@app.route(f'/busca/', methods = ['GET', 'POST'])
def busca():
    if request.method == "GET":
        return render_template(f'{page_customer_search}.html', tipo="", resultado=[]), 200
    try:
        status_code = 460
        tipo = request.form['tipo']
        criterio = request.form['criterio']
        if tipo == 'cliente':
            try:
                status_code = 550
                resultado = f.pesquisar_cliente_geral(criterio)
                if len(resultado)>0:
                    status_code = 200
                else:
                    status_code = 561
                    raise
            except:
                return render_template(f'{page_customer_search}.html', tipo = tipo, resultado = []), status_code
        elif tipo == 'veiculo':
            try:
                status_code = 550
                resultado = f.pesquisar_veiculo_geral(criterio)
                if len(resultado)>0:
                    status_code = 200
                else:
                    status_code = 561
                    raise
            except:
                return render_template(f'{page_customer_search}.html', tipo = tipo, resultado = []), status_code
        elif tipo == 'ordem':
            pass
        else:
            status_code = 599
            raise
        return render_template(f'{page_customer_search}.html', tipo = tipo, resultado=resultado), status_code
    except:
        return render_template(f'{page_customer_search}.html', tipo="", resultado='[]'), status_code

@app.route(f'/cliente/<id_cliente>/', methods = ['GET'])
def exibir_cliente(id_cliente):
    status_code = 550
    try:
        status_code = 561
        cliente_atual = c.Cliente(id_cliente=id_cliente)
        busca_veiculos = f.pesquisar_veiculo_cliente(cliente_atual.id_cliente)
        return render_template('cliente.html', cliente = cliente_atual.enviar(), veiculos = busca_veiculos), 200
    except:
        return render_template('cliente.html', cliente = {}, veiculo = {}), status_code

@app.route(f'/cliente/<id_cliente>/{page_vehicle_registration}/', methods=['GET','POST'])
def vehicle_registration(id_cliente):
    status_code = 500
    try:
            status_code = 561
            cliente_atual = c.Cliente(id_cliente=id_cliente)
    except:
        cliente = {}
        return render_template (f'{page_vehicle_registration}.html', cliente = {}), status_code

    if request.method == 'GET':
        return render_template (f'{page_vehicle_registration}.html', cliente = cliente_atual.enviar()), 200
        
    status_code = 200
    try:
        status_code = 561
        status_code = 460
        placa = request.form['placa']
        chassi = request.form['chassi']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano_fabricacao = request.form['ano_fabricacao']
        ano_modelo = request.form['ano_modelo']
        cor = request.form['cor']
        status_code=550
        if placa and chassi:
            veiculo_encontrado = f.pesquisar_veiculo(placa,chassi)
            if (len(veiculo_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                novo_veiculo = c.Veiculo(id_cliente = cliente_atual.id_cliente, placa = placa, chassi = chassi, marca = marca, modelo = modelo, ano_fabricacao = ano_fabricacao, ano_modelo = ano_modelo, cor = cor)
                novo_veiculo.salvar()
                # return render_template(f'{page_vehicle_registration}.html', cliente = cliente_atual), 200
                return jsonify(cliente_atual.enviar()), 200
        else:
            status_code = 460
            raise
    except:
        return render_template(f'{page_vehicle_registration}.html', cliente = cliente_atual), status_code

#---WIP---
@app.route(f'/{page_vehicle_registration}/')
def vehicle_registration_default():
    return render_template(f'{page_vehicle_registration}.html', cliente = "")

#---NOT IMPLEMENTED---
@app.route('/order/', methods=['GET','POST'])
def ordem_default():
    return render_template('order.html'), 501

@app.route('/<id_veiculo>/order/', methods=['GET','POST'])
def ordem(id_veiculo):
    return render_template('order.html'), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)