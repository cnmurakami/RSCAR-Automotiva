function filtrarServicos(){
    const searchInput = document.getElementById("filtrar_servicos");

    searchInput.onkeyup = function() {
        const searchTerm = searchInput.value.toLowerCase();
        const tableRows = document.querySelectorAll(".item_lista");

        for (let i = 0; i < tableRows.length; i++) {
            const row = tableRows[i];
            const nameCell = row.querySelector("td:nth-child(2)");
            if (nameCell){
                const nameText = nameCell.textContent.toLowerCase();
                
                if (nameText.indexOf(searchTerm) !== -1) {
                    row.style.display = "table-row";
                }
                else {
                    row.style.display = "none";
                }
            }
        }
    };
}



const checkboxes = document.querySelectorAll("input[type='checkbox']");
const selectedItemsTable = document.querySelector(".itens_selecionados");

checkboxes.forEach(checkbox => {
  checkbox.addEventListener("change", function(event) {
    if (this.checked) {
        const nameCell = this.parentElement.nextElementSibling;
        const valueCell = nameCell.nextElementSibling;
        const name = nameCell.textContent.trim();
        const value = valueCell.textContent.trim();
        const newRow = document.createElement("tr");
        const nameCellElement = document.createElement("td");
        nameCellElement.textContent = name;
        const valueCellElement = document.createElement("td");
        valueCellElement.textContent = value;
        newRow.appendChild(nameCellElement);
        newRow.appendChild(valueCellElement);

        newRow.id = Math.random().toString(36).substring(2, 15);

        checkbox.setAttribute('data-row-id', newRow.id);
        selectedItemsTable.appendChild(newRow);
    } else if (this === event.target) {
        const rowId = this.dataset.rowId;
        const rowToRemove = selectedItemsTable.querySelector(`tr[id="${rowId}"]`);
        if (rowToRemove) {
            selectedItemsTable.removeChild(rowToRemove);
            this.removeAttribute('data-row-id');
        }
    }
    
    sumTableColumn('.itens_selecionados', 1)
  });
});

function sumTableColumn(table, columnIndex) {
  const tableElement = document.querySelector(table);

  const rows = tableElement.querySelectorAll("tr");
  let sum = 0;
  for (let i = 0; i < rows.length; i++) {
    const cell = rows[i].querySelector(`td:nth-child(${columnIndex + 1})`);
    if (cell) {
      const value = parseFloat(cell.textContent.replace(/[^\d.-]/g, '').trim());
      if (!isNaN(value)) {
        sum += value;
      }
    }
  }
  document.getElementById('mostrarTotal').value = "R$ "+sum.toLocaleString(undefined, {minimumFractionDigits: 2}).toString();
}

document.addEventListener('DOMContentLoaded', function() {
  sumTableColumn('.itens_selecionados', 1)
}, false);

function enviar_form(){
  form = document.getElementById("ordem")
  const formData = new FormData(form);
  fetch("", {
      method: "POST",
      body: formData,
  }).then(response => {
      return response.json();
  }).then(jsonResponse => {
      var nova_ordem = jsonResponse;
      var id_nova_ordem = nova_ordem["id_ordem"]
      var hostname = window.location.hostname;
      var port = window.location.port ? ':' + window.location.port : '';
      var exibir_ordem = "http://" + hostname + port + "/ordem/" + id_nova_ordem +"/";
      window.location.replace(exibir_ordem);
  }).catch (error => {
      console.log(error)
  })
}

function avancar_status(){
  form = document.getElementById("avancar_ordem")
  const formData = new FormData(form);
  var id_ordem = formData.get("id_ordem")
  var hostname = window.location.hostname;
  var port = window.location.port ? ':' + window.location.port : '';
  var exibir_ordem = "http://" + hostname + port + "/ordem/" + id_ordem +"/";
  fetch(exibir_ordem+"avancar",{
    method: "POST",
    body: formData,
  }).then(response =>{
    return response.json();
  }).then(jsonResponse => {
    var result = jsonResponse;
    var success = result["success"];
    var status_code = result["status_code"];
    if (success){  
      window.location.replace(exibir_ordem);
    }
    else{
      alert("Erro ao atualizar status.\nPor favor tente novamente.\n\nCode: "+status_code)
    }
  }).catch(error => {
    console.log(error)
  })
}

function cancelar_status() {
  const form = document.getElementById('cancelar_ordem');
  const id_ordem = form.querySelector('input[name="id_ordem"]').value;

  fetch(`/ordem/${id_ordem}/cancelar`, {
      method: 'POST',
      body: new URLSearchParams(new FormData(form))
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          window.location.reload();
      } else {
          alert('Erro ao cancelar ordem');
      }
  });
}

function confirmar_cancelamento() {
  const confirmacao = confirm("Você tem certeza que deseja cancelar esta ordem de serviço?");
  if (confirmacao) {
      cancelar_status();
  } else {
      return false;
  }
}
