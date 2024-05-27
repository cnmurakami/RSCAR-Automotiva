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
    
def pesquisar_veiculo_cliente(parametro):
    try:
        resultado = db.execute('SELECT * FROM veiculo WHERE id_cliente = %s', (parametro,))
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception