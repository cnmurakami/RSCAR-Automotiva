from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
from flask_mysqldb import MySQL
import functions as f
import db_classes as c
import db_config as db_config

#global variables
page_index = 'home'
page_cadastro_cliente = 'register'
page_cliente = 'cliente'
page_busca = 'search'
page_cadastro_veiculo = 'vehicle_registration'
page_ordem = 'ordem'
page_veiculo = 'veiculo'
page_erro = 'erro'
lista_erro = {
'550' : 'Erro ao conectar-se ao db',
'551' : 'Erro ao salvar informações no db', 
'552' : 'Erro ao recuperar informações no db', 
'561' : 'Informação não localizada', 
'599' : 'Erro desconhecido de servidor'
}

app = Flask(__name__)
app.config['MYSQL_USER'] = db_config.user
app.config['MYSQL_PASSWORD'] = db_config.password
app.config['MYSQL_DB'] = db_config.db
app.config['MYSQL_HOST'] = db_config.host
mysql = MySQL(app)



@app.route('/', methods=['GET'])
def home():
    return render_template(f'{page_index}.html')

@app.route(f'/{page_cadastro_cliente}/', methods=['GET','POST'])
def register():
    status_code=599
    if request.method == 'GET':
        return render_template(f'{page_cadastro_cliente}.html')
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
        bairro = request.form['bairro']
        estado = request.form['estado']
        cidade = request.form['cidade']
        telefone = celular
        endereco = f'{logradouro};;{numero};;{complemento};;{bairro};;{cidade};;{estado};;{cep}'
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
                    # return render_template(f'{page_cadastro_cliente}.html', resposta_cliente = cliente_confirmado.enviar), 200
                    # return redirect(url_for('exibir_cliente', id_cliente = cliente_confirmado.id_cliente)), 200
                    return jsonify(cliente_confirmado), 200
                    
                except:
                    return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), 552
        else:
            status_code=460
            raise
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

@app.route(f'/{page_busca}/', methods = ['GET', 'POST'])
def busca():
    if request.method == "GET":
        return render_template(f'{page_busca}.html', tipo="", resultado=[]), 200
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
                return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
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
                return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
        elif tipo == 'ordem':
            try:
                status_code = 550
                resultado = f.pesquisar_ordem_geral(criterio)
                
                if len(resultado)>0:
                    status_code = 200
                else:
                    status_code = 561
                    raise
            except:
                return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
        else:
            status_code = 599
            raise
        return render_template(f'{page_busca}.html', tipo = tipo, resultado=resultado), status_code
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

@app.route(f'/{page_cliente}/<id_cliente>/', methods = ['GET'])
def exibir_cliente(id_cliente):
    status_code = 550
    try:
        status_code = 561
        cliente_atual = c.Cliente(id_cliente=id_cliente)
        busca_veiculos = f.pesquisar_veiculo_cliente(cliente_atual.id_cliente)
        return render_template(f'{page_cliente}.html', cliente = cliente_atual.enviar(), veiculos = busca_veiculos), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

@app.route(f'/{page_veiculo}/<id_veiculo>', methods = ['GET'])
def exibir_veiculo(id_veiculo):
    status_code = 550
    try:
        status_code = 561
        veiculo_atual = c.Veiculo(id_veiculo=id_veiculo)
        cliente = c.Cliente(id_cliente=veiculo_atual.id_cliente)
        ordens = f.pesquisar_ordem_geral(veiculo_atual.placa)
        return render_template(f'{page_veiculo}.html', cliente = cliente.enviar(), veiculo = veiculo_atual.enviar(), ordens = ordens), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

@app.route(f'/{page_cliente}/<id_cliente>/{page_cadastro_veiculo}/', methods=['GET','POST'])
def vehicle_registration(id_cliente):
    status_code = 500
    try:
            status_code = 561
            cliente_atual = c.Cliente(id_cliente=id_cliente)
    except:
        cliente = {}
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

    if request.method == 'GET':
        return render_template (f'{page_cadastro_veiculo}.html', cliente = cliente_atual.enviar()), 200
        
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
                # return render_template(f'{page_cadastro_veiculo}.html', cliente = cliente_atual), 200
                return jsonify(cliente_atual.enviar()), 200
        else:
            status_code = 460
            raise
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

#---WIP---
@app.route(f'/{page_cadastro_veiculo}/')
def vehicle_registration_default():
    return render_template(f'{page_cadastro_veiculo}_default.html')

#---NOT IMPLEMENTED---
@app.route(f'/{page_ordem}/', methods=['GET','POST'])
def ordem_default():
    return render_template(f'{page_ordem}_default.html')

@app.route(f'/<id_veiculo>/{page_ordem}/', methods=['GET','POST'])
def ordem(id_veiculo):
    try:
        status_code = 550
        lista_servicos = f.get_tipos_servicos()
        status_code = 552
        veiculo = c.Veiculo(id_veiculo = id_veiculo)
        cliente = c.Cliente(id_cliente = veiculo.id_cliente)
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
    if (request.method == 'GET'):
        status_code = 500
        try:
            return render_template(f'{page_ordem}.html', veiculo = veiculo.enviar(), cliente = cliente.enviar(), lista_servicos = lista_servicos), 200
        except:
            return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
    try:
        servicos_selecionados = []
        for i in range(lista_servicos[len(lista_servicos)-1]['id_servico']):
            try:
                servicos_selecionados.append(request.form[f'{i}'])
            except:
                pass
        nova_ordem = c.Ordem(id_cliente=cliente.id_cliente, id_veiculo=veiculo.id_veiculo)
        nova_ordem.salvar()
        nova_ordem.localizar_ultima_ordem()
        nova_ordem.salvar_servicos(servicos_selecionados)
        return jsonify(nova_ordem.enviar()), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code

@app.route(f'/{page_ordem}/<id_ordem>/', methods = ['GET'])
def mostrar_ordem(id_ordem):
    ordem = c.Ordem(id_ordem=id_ordem)
    cliente = c.Cliente(id_cliente=ordem.id_cliente)
    veiculo = c.Veiculo(id_veiculo=ordem.id_veiculo)
    lista_servicos_cadastrados = ordem.recuperar_servicos()
    lista_servicos_completa = f.get_tipos_servicos()
    lista_servicos = []
    for i in lista_servicos_completa:
        if i['id_servico'] in lista_servicos_cadastrados:
            lista_servicos.append(i)
        if len(lista_servicos)==len(lista_servicos_cadastrados):
            break
    return render_template(f'ordem_exibir.html', ordem = ordem.enviar(), veiculo=veiculo.enviar(), cliente = cliente.enviar(), lista_servicos=lista_servicos)

@app.route('/teste/', methods = ['GET'])
def teste():
    ordem = c.Ordem(id_ordem='39')
    resultado = ordem.enviar_completo()
    return resultado

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)