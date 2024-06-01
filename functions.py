import db_operations as db
import db_classes as c

def criar_lista_cliente(resultado):
    lista_clientes = []
    for i in resultado:
        lista_clientes.append(c.Cliente(id_cliente=str(i[0])))
    clientes = []
    for i in lista_clientes:
        clientes.append(i.enviar())
    return clientes

def pesquisar_cliente(cpf='', cnpj=''):
    resultado = db.execute('select * from cliente where cpf = %s and cnpj = %s', (cpf, cnpj))
    if len(resultado)>0:
        return criar_lista_cliente(resultado)
    else:
        return []

def criar_lista_veiculo(resultado):
    lista_veiculos = []
    for i in resultado:
        lista_veiculos.append(c.Veiculo(id_veiculo=str(i[0])))
    veiculos = []
    for i in lista_veiculos:
        veiculos.append(i.enviar())
    return veiculos

def criar_lista_ordem(resultado):
    lista_ordens = []
    for i in resultado:
        lista_ordens.append(c.Ordem(id_ordem=str(i[0])))
    ordens = []
    for i in lista_ordens:
        ordens.append(i.enviar_completo())
    return ordens


def pesquisar_veiculo(placa,chassi):
    resultado = db.execute('select * from veiculo where placa = %s or chassi = %s', (placa, chassi))
    if len(resultado)>0:
        return criar_lista_veiculo(resultado)
    else:
        return []

def pesquisar_cliente_geral(parametro):
    try:
        resultado = db.execute('SELECT * FROM cliente WHERE lower(nome) LIKE %s OR lower(email) LIKE %s OR telefone LIKE %s OR cpf LIKE %s OR cnpj LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        if len(resultado)>0:
            return criar_lista_cliente(resultado)
        else:
            return []
    except:
        return Exception
    
def pesquisar_veiculo_geral(parametro):
    try:
        resultado = db.execute('SELECT * FROM veiculo WHERE lower(id_veiculo) LIKE %s OR lower(placa) LIKE %s OR lower(chassi) LIKE %s OR id_cliente LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception
    
def pesquisar_ordem_geral(parametro):
    try:
        resultado_final = []
        resultado_clientes = pesquisar_cliente_geral(parametro)
        resultado_veiculos = pesquisar_veiculo_geral(parametro)
        try:
            resultado_final+=db.execute('SELECT * FROM ordem where id_ordem like %s', (parametro,))
        except: pass
        for i in resultado_veiculos:
            try:
                resultado_final+=db.execute('SELECT * FROM ordem where id_veiculo = %s', (i['id_veiculo']))
            except:
                pass
        for i in resultado_clientes:
            try:
                resultado_final+=db.execute('SELECT * FROM ordem where id_cliente = %s', (i['id_cliente']))
            except:
                pass
        return criar_lista_ordem(resultado_final)
    except:
        return Exception

def pesquisar_veiculo_cliente(parametro):
    try:
        resultado = db.execute('SELECT * FROM veiculo WHERE id_cliente = %s', (parametro,))
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception
    
def get_tipos_servicos():
    resultado = db.fullget('select * from tipo_servico')
    lista_servicos = []
    for item in resultado:
        lista_servicos.append({'id_servico':item[0], 'nome':item[1], 'valor':item[2]})
    return lista_servicos
