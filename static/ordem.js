function filtrarServicos() {
  const searchInput = document.getElementById("filtrar_servicos");

  searchInput.onkeyup = function() {
      const searchTerm = searchInput.value.toLowerCase();
      const tableRows = document.querySelectorAll(".item_lista");

      for (let i = 0; i < tableRows.length; i++) {
          const row = tableRows[i];
          const nameCell = row.querySelector("td:nth-child(2)");
          if (nameCell) {
              const nameText = nameCell.textContent.toLowerCase();

              if (nameText.indexOf(searchTerm) !== -1) {
                  row.style.display = "table-row";
              } else {
                  row.style.display = "none";
              }
          }
      }
  };
}

document.querySelectorAll('.servicos input[type="checkbox"]').forEach(checkbox => {
  checkbox.addEventListener('change', function() {
      const row = this.closest('tr');
      const id = this.id;
      const nome = row.querySelector('label[for="' + id + '"]').textContent.trim();
      const valorUnitario = parseFloat(row.querySelector('td:nth-child(3)').textContent.replace(/[^\d.-]/g, '').trim());
      const quantidadeSelecionada = this.checked ? 1 : 0;
      updateSelectedItems(id, nome, valorUnitario, quantidadeSelecionada, 'servico');
      sumTableColumn('.itens_selecionados', 2);
  });
});


const selectedItemsTable = document.querySelector(".itens_selecionados");

document.querySelectorAll('.ajustar-quantidade').forEach(button => {
  button.addEventListener('click', function() {
      const row = this.closest('tr');
      const id = 'peca'+row.dataset.id;
      const nome = row.querySelector('td:nth-child(1)').textContent.trim();
      const valorUnitario = parseFloat(row.querySelector('td:nth-child(3)').textContent.replace(/[^\d.-]/g, '').trim());
      const tipoItem = row.classList.contains('servico') ? 'servico' : 'peca';
      const quantidadeSpan = row.querySelector('.quantidade-selecionada');
      const estoqueCell = tipoItem === 'peca' ? row.querySelector('.estoque') : null;
      let quantidadeSelecionada = parseInt(quantidadeSpan.textContent);
      let estoque = estoqueCell ? parseInt(estoqueCell.textContent) : null;
      if (this.textContent === '+') {
          if (tipoItem === 'peca' && estoque > 0) {
              quantidadeSelecionada++;
              estoque--;
          } else if (tipoItem === 'servico') {
              quantidadeSelecionada++;
          }
      } else if (this.textContent === '-') {
          if (quantidadeSelecionada > 0) {
              quantidadeSelecionada--;
              if (tipoItem === 'peca') estoque++;
          }
      }
      quantidadeSpan.textContent = quantidadeSelecionada;
      if (estoqueCell) estoqueCell.textContent = estoque;

      updateSelectedItems(id, nome, valorUnitario, quantidadeSelecionada, tipoItem);
      sumTableColumn('.itens_selecionados', 2); 
  });
});


function updateSelectedItems(id, nome, valorUnitario, quantidade, tipoItem) {
  const selectedItemsTable = document.querySelector(".itens_selecionados");
  let existingRow = selectedItemsTable.querySelector(`tr[data-id="${id}"]`);

  if (quantidade > 0) {
      const valorTotal = valorUnitario * quantidade;
      if (!existingRow) {
          existingRow = document.createElement("tr");
          existingRow.setAttribute("data-id", id);
          existingRow.classList.add(tipoItem);
          existingRow.innerHTML = `<td>${nome}</td><td class="valor">R$ ${valorTotal.toFixed(2)}</td>`;
          selectedItemsTable.appendChild(existingRow);
      } else {
          existingRow.querySelector(".valor").textContent = `R$ ${valorTotal.toFixed(2)}`;
      }
  } else if (existingRow) {
      selectedItemsTable.removeChild(existingRow);
  }
  sumTableColumn('.itens_selecionados', 2);
}

function sumTableColumn(tableSelector, columnIndex) {
  let total = 0;
  document.querySelectorAll(`${tableSelector} tr`).forEach(row => {
    const valueCell = row.querySelector(`td:nth-child(${columnIndex})`);
    if (valueCell) {
      const valueText = valueCell.textContent.replace(/[^\d.-]/g, '').trim();
      const value = parseFloat(valueText);
      if (!isNaN(value)) {
        total += value;
      }
    }
  });

  document.getElementById("mostrarTotal").value = `R$ ${total.toFixed(2)}`;
}

document.addEventListener('DOMContentLoaded', function() {
  sumTableColumn('.itens_selecionados', 2)
}, false);

function enviar_form() {
  form = document.getElementById("ordem");
  const formData = new FormData(form);
  document.querySelectorAll('.servicos input[type="checkbox"]:checked').forEach(checkbox => {
    const id_servico = checkbox.value;
    formData.append(`servico${id_servico}`, id_servico);
  });

  document.querySelectorAll('.pecas .ajustar-quantidade').forEach(button => {
    const row = button.closest('tr');
    const id_peca = row.dataset.id;
    const quantidade = row.querySelector('.quantidade-selecionada').textContent.trim();
    if (quantidade > 0) {
      formData.append(`peca${id_peca}`, quantidade);
    }
  });

  fetch("", {
    method: "POST",
    body: formData,
  }).then(response => {
    return response.json();
  }).then(jsonResponse => {
    var nova_ordem = jsonResponse;
    var id_nova_ordem = nova_ordem["id_ordem"];
    var hostname = window.location.hostname;
    var port = window.location.port ? ':' + window.location.port : '';
    var exibir_ordem = "http://" + hostname + port + "/ordem/" + id_nova_ordem +"/";
    window.location.replace(exibir_ordem);
  }).catch (error => {
    console.log(error);
  });
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

function confirmar_finalizacao() {
  const confirmacao = confirm("Você tem certeza que deseja finalizar esta ordem de serviço?");
  if (confirmacao) {
      avancar_status();
  } else {
      return false;
  }
}

function alterar_ordem(){
  form = document.getElementById("ordem")
  const formData = new FormData(form);
  var id_ordem = formData.get("id_ordem")
  fetch("", {
      method: "POST",
      body: formData,
  }).then(response => {
      return response.json();
  }).then(jsonResponse => {
      var nova_ordem = jsonResponse;
      //var id_nova_ordem = nova_ordem["id_ordem"]
      var hostname = window.location.hostname;
      var port = window.location.port ? ':' + window.location.port : '';
      var exibir_ordem = "http://" + hostname + port + "/ordem/" + id_ordem;
      window.location.replace(exibir_ordem);
  }).catch (error => {
      console.log(error)
  })
}
