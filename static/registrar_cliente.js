function limpar_dados(event){
    const inputField = event.target;
    const campo = inputField.value.replace(/[^0-9]/g, '');
    inputField.value = campo
}

function verificar_form(){
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
        formData.append("cidade", document.getElementById('cidade').value);
        formData.append("estado", document.getElementById('estado').value);
        fetch("", {
            method: "POST",
            body: formData,
        }).then(response => {
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