const lista_erro = {
    550 : 'Erro ao conectar-se ao db',
    551 : 'Erro ao salvar informações no db', 
    552 : 'Erro ao recuperar informações no db', 
    561 : 'Informação não localizada', 
    599 : 'Erro desconhecido de servidor'
    }

function sanitizar_dados(event){
    const inputField = event.target;
    const campo = inputField.value.replace(/[^0-9]/g, '');
    inputField.value = campo
}

function limitar_documento(){

    const documento = document.getElementById("documento").value;
    const tipoDocumento = document.getElementById("tipoDocumento").value;
    var tamanho = 0;
    if (tipoDocumento == "cpf"){
        tamanho = 11;
    }
    else{
        tamanho = 14;
    }
    documento.value = value.substring(0, tamanho);
}

function validar_email(email) {
    const regex = /^.*@([a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.)+[a-zA-Z]{2,}$/;
    const checagem = email.match(regex);
    return checagem;
  }

function enviar_form(){
    if (!validar_formulario()){
        return false
    }
    form = document.querySelector("registrar_cliente");
    const tipoDocumento = document.getElementById("tipoDocumento").value;
    const documento = document.getElementById('documento').value;
    var cpf = "";
    var razao_social = "";
    var cnpj = "";
    var nome = "";
    if (tipoDocumento == "cpf"){
        cpf = documento
        razao_social = ""
        cnpj = ""
        nome = document.getElementById('nome').value
    }
    else{
        cnpj = documento
        cpf = ""
        nome = ""
        razao_social = document.getElementById('nome').value
    }
    const formData = new FormData();
    formData.append("cpf", cpf);
    formData.append("cnpj", cnpj);
    formData.append("nome", nome);
    formData.append("razao_social", razao_social);
    formData.append("telefone", document.getElementById('telefone').value);
    formData.append("email", document.getElementById('email').value);
    formData.append("cep", document.getElementById('cep').value);
    formData.append("logradouro", document.getElementById('logradouro').value);
    formData.append("numero", document.getElementById('numero').value);
    formData.append("complemento", document.getElementById('complemento').value);
    formData.append("bairro", document.getElementById('bairro').value);
    formData.append("cidade", document.getElementById('cidade').value);
    formData.append("estado", document.getElementById('estado').value);
    fetch("", {
        method: "POST",
        body: formData,
    }).then(response => {
        if (!response.ok){
            alert("Ocorreu um erro, por favor tente novamente ou contate o administrador caso o problema persista. \n\nCódigo " + response.status + ": " + lista_erro[response.status] + ".")
        }
        return response.json();
    }).then(jsonResponse => {
        var novo_cliente = jsonResponse;
        var hostname = window.location.hostname;
        var port = window.location.port ? ':' + window.location.port : '';
        var id_novo_cliente = novo_cliente["id_cliente"]
        var exibir_cliente = "http://" + hostname + port + "/cliente/" + id_novo_cliente +"/";
        window.location.replace(exibir_cliente);
    }).catch (error => {
        console.log(error)
    })
}

function validar_formulario() {
    var formulario = document.forms['registrar_cliente']
    campo = formulario['nome'].value
    if (campo == "") {
        alert("Campo nome não pode ser vazio.");
        return false;
    }
    campo = formulario['documento'].value
    if (campo == "") {
        alert("Campo documento não pode ser vazio.");
        return false;
    }
	campo = formulario['telefone'].value
    if (campo == "") {
        alert("Campo telefone não pode ser vazio.");
        return false;
    }
	campo = formulario['email'].value
    if (campo == "") {
        alert("Campo email não pode ser vazio.");
        return false;
    }
    else if (!validar_email(campo)) {
        alert("Email inválido")
        return false;
    }
	campo = formulario['cep'].value
    if (campo == "") {
        alert("Campo cep não pode ser vazio.");
        return false;
    }
	campo = formulario['logradouro'].value
    if (campo == "") {
        alert("Campo logradouro não pode ser vazio.");
        return false;
    }
	campo = formulario['numero'].value
    if (campo == "") {
        alert("Campo numero não pode ser vazio.");
        return false;
    }
	campo = formulario['cidade'].value
    if (campo == "") {
        alert("Campo cidade não pode ser vazio.");
        return false;
    }
	campo = formulario['estado'].value
    if (campo == "") {
        alert("Selecione o estado.");
        return false;
    }
    return true;
  }

const documento = document.getElementById('documento');
const tipoDocumento = document.getElementById('tipoDocumento');
var tamanhoMaximo = 11;

tipoDocumento.addEventListener('change', (event) => {
    if (event.target.value == "cpf"){
        tamanhoMaximo = 11;
    }
    else{
        tamanhoMaximo = 14;
    }
});

function atualizarDocumento(){
    const novo_documento = documento.value.substring(0, tamanhoMaximo);
    documento.value = novo_documento;
}

tipoDocumento.addEventListener('change', atualizarDocumento);

documento.addEventListener('input', (event) => {
  const value = event.target.value;
  if (value.length > tamanhoMaximo) {
    documento.value = value.substring(0, tamanhoMaximo);  // Truncate value
  }
});