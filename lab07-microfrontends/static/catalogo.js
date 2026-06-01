async function renderCatalogo() {
    const response = await fetch('/api/v1/catalogo');
    const data = await response.json();
    const container = document.getElementById('vitrine-list');
    container.innerHTML = '';
    data.produtos.forEach(p => {
        const div = document.createElement('div');
        div.className = 'product';
        div.innerHTML = `<span><strong>${p.nome}</strong> - R$ ${p.preco}</span><button onclick="adicionarAoCarrinho('${p.nome}', ${p.preco})">Adicionar</button>`;
        container.appendChild(div);
    });
}
function adicionarAoCarrinho(nome, preco) {
    console.log(`[CATALOGO] Evento: Adicionar ${nome}`);
}
renderCatalogo();
