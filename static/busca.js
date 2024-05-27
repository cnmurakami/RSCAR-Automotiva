function sanitizar_dados(event){
    const inputField = event.target;
    const campo = inputField.value.replace(/[^a-zA-Z0-9]/g, '');
    inputField.value = campo
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
    const form = document.getElementById("busca");
    form.submit();
}

function validar_formulario() {
    var formulario = document.forms['busca']
    campo = formulario['criterio'].value
    if (campo == "") {
        alert("Por favor preencha o critério de busca");
        return false;
    }
    else if (campo.length < 3){
        alert("Por favor forneça pelo menos 3 caracteres")
    }
    return true;
}