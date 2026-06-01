const cart = { items: [], total: 0 };
function updateCartUI() {
    const list = document.getElementById('cart-list');
    const totalEl = document.getElementById('cart-total');
    list.innerHTML = cart.items.length === 0 ? 'Vazio' : '';
    cart.items.forEach(item => {
        const div = document.createElement('div');
        div.innerText = `${item.nome} - R$ ${item.preco}`;
        list.appendChild(div);
    });
    totalEl.innerText = cart.total.toFixed(2);
}
updateCartUI();
