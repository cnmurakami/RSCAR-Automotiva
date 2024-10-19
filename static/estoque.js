function atualizarEstoque(idPeca, operacao) {
    
    if (operacao === 'subtrair') {
        quantidade = document.getElementById(`subtrair_${idPeca}`).value;
     } else if (operacao === 'adicionar') 
        quantidade = document.getElementById(`adicionar_${idPeca}`).value;
    
    if (quantidade > 0) {
        const formData = new FormData();
        formData.append('id_peca', idPeca);
        formData.append('qtd', quantidade);
        formData.append('operacao', operacao);
        fetch(`/estoque/atualizar`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Estoque atualizado com sucesso!');
                location.reload();
            } else {
                alert(`Erro ao atualizar estoque: Código ${data.status_code}`);
            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
    } else {
        alert('Por favor, insira uma quantidade válida.');
    }
}



function sumTableColumn(columnIndex) {
    const table = document.querySelectorAll(".pecas_selecionadas");
    if (table.length === 0) {
        console.error("Tabela não encontrada");
        return;
    }
    let sum = 0;
    const rows = table[0].querySelectorAll('tbody tr');
    rows.forEach((row) => {
        const cellValue = parseFloat(row.cells[columnIndex].innerText.replace('R$', '').trim());
        if (!isNaN(cellValue)) {
            sum += cellValue;
        }
    });
    return sum;
}
document.addEventListener('DOMContentLoaded', () => {
    sumTableColumn(2);
});
