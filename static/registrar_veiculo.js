function sanitizar_dados(event){
    const inputField = event.target;
    const campo = inputField.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    inputField.value = campo
}

function enviar_form(){
    if (!validar_formulario()){
        return false
    }
    form = document.querySelector("registrar_veiculo");
    const formData = new FormData();
    const id_cliente = document.getElementById('id_cliente').value;
    formData.append("id_cliente", document.getElementById('id_cliente').value);
    formData.append("placa", document.getElementById('placa').value);
    formData.append("chassi", document.getElementById('chassi').value);
    formData.append("marca", document.getElementById('marca').value);
    formData.append("modelo", document.getElementById('modelo').value);
    formData.append("cor", document.getElementById('cor').value);
    formData.append("ano_fabricacao", document.getElementById('ano_fabricacao').value);
    formData.append("ano_modelo", document.getElementById('ano_modelo').value);
    fetch("", {
        method: "POST",
        body: formData,
    }).then(response => {
        return response.json();
    }).then(jsonResponse => {
        var novo_cliente = jsonResponse;
        var hostname = window.location.hostname;
        var port = window.location.port ? ':' + window.location.port : '';
        var exibir_cliente = "http://" + hostname + port + "/cliente/" + id_cliente +"/";
        window.location.replace(exibir_cliente);
    }).catch (error => {
        console.log(error)
    })
}

function validar_formulario() {
    var formulario = document.forms['registrar_veiculo']
    campo = formulario['placa'].value
    if (campo == "") {
        alert("Campo placa não pode ser vazio.");
        return false;
    }
    campo = formulario['chassi'].value
    if (campo == "") {
        alert("Campo chassi não pode ser vazio.");
        return false;
    }
	campo = formulario['marca'].value
    if (campo == "") {
        alert("Campo marca não pode ser vazio.");
        return false;
    }
	campo = formulario['modelo'].value
    if (campo == "") {
        alert("Campo modelo não pode ser vazio.");
        return false;
    }
	campo = formulario['cor'].value
    if (campo == "") {
        alert("Campo cor não pode ser vazio.");
        return false;
    }
	campo = formulario['ano_fabricacao'].value
    if (campo == "") {
        alert("Selecione o ano de fabricação.");
        return false;
    }
	campo = formulario['ano_modelo'].value
    if (campo == "") {
        alert("Selecione o ano do modelo.");
        return false;
    }
    return true;
}