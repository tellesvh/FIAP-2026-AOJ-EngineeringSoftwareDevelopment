# Lab Autoguiado: Micro Frontends e a Loja Frankenstein 🧟

Neste laboratório, vamos resolver o problema do "Front-end Monolítico" e da latência excessiva usando o padrão **Micro Frontends** integrado a um **BFF (Backend-For-Frontend)**.

## 📖 Narrativa de Caos
Nosso portal de e-commerce virou um pesadelo. O time de **Catálogo** e o time de **Carrinho** não conseguem mais trabalhar sem quebrar o código um do outro. Além disso, para mostrar um simples produto, o front-end faz 5 chamadas HTTP separadas para buscar Preço, Nome, Descrição e Estoque. Em conexões mobile, isso é um desastre.

Sua missão é separar esses times usando **CustomEvents** para comunicação e otimizar a performance usando o **BFF** que já deixamos preparado no back-end.

🎯 **Tempo Estimado:** 20 minutos (Missão) + 10 minutos (Masterclass)

---

## 🎯 Objetivo Final
1.  Refatorar o fragmento de **Catálogo** para consumir o endpoint consolidado `/api/bff/home`.
2.  Implementar a comunicação desacoplada entre os fragmentos usando eventos nativos do navegador.
3.  Garantir que o Carrinho reaja às adições sem conhecer nenhuma função interna do Catálogo.

---

## 🗺️ Passo 1: O Cenário "Frankenstein"
1. No seu Codespaces, navegue até a pasta do laboratório e instale as dependências:
   ```bash
   cd lab07-microfrontends
   pip install fastapi uvicorn httpx2
   ```
2. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```
3. Abra a URL no navegador. Você verá a "Loja Frankenstein". Note que o botão "Adicionar" não funciona e a rede (F12 > Network) está poluída com múltiplas chamadas.

---

## ✂️ Passo 2: Otimizando a Performance (BFF)
Abra o arquivo `static/catalogo.js`. O time de back-end já criou um endpoint de agregação. Vamos usá-lo.

**Altere a função `renderCatalogo` para usar o BFF:**

```javascript
async function renderCatalogo() {
    // TROQUE: /api/v1/catalogo por /api/bff/home
    const response = await fetch('/api/bff/home');
    const data = await response.json();
    
    const container = document.getElementById('vitrine-list');
    container.innerHTML = '';

    // ATENÇÃO: O BFF retorna 'vitrine' em vez de 'produtos'
    data.vitrine.forEach(p => {
        const div = document.createElement('div');
        div.className = 'product';
        div.innerHTML = `
            <span><strong>${p.nome}</strong> - R$ ${p.preco} <br>
            <span class="stock-tag">Status: ${p.estoque}</span></span>
            <button onclick="adicionarAoCarrinho('${p.nome}', ${p.preco})">Adicionar</button>
        `;
        container.appendChild(div);
    });
}
```

---

## 📢 Passo 3: Gritando no Front-end (CustomEvents)
Agora, vamos fazer o Catálogo "anunciar" a venda sem precisar saber quem é o Carrinho.

**Implemente o disparo do evento no `catalogo.js`:**

```javascript
function adicionarAoCarrinho(nome, preco) {
    console.log(`[CATALOGO] Disparando evento para: ${nome}`);
    
    // Criamos um evento customizado que qualquer um pode ouvir
    const evento = new CustomEvent('cart:add', { 
        detail: { nome, preco } 
    });
    
    window.dispatchEvent(evento);
}
```

---

## 👂 Passo 4: O Ouvinte Atento (Carrinho)
Agora, o time do Carrinho só precisa ficar "de orelha em pé".

**Abra o `static/carrinho.js` e adicione o listener:**

```javascript
// O Carrinho é independente. Ele apenas escuta o 'cart:add'
window.addEventListener('cart:add', (e) => {
    const { nome, preco } = e.detail;
    console.log(`[CARRINHO] Recebi notificação de adição: ${nome}`);
    
    cart.items.push({ nome, preco });
    cart.total += preco;
    updateCartUI();
});
```

---

## 🧪 Passo 5: Validação de Engenharia
1.  Recarregue a página. 
2.  Clique em "Adicionar". O carrinho deve atualizar instantaneamente.
3.  Rode os testes para garantir que você não quebrou o contrato da API:
    ```bash
    pytest test_lab07.py -v
    ```

---
*Dica de Ouro: Micro Frontends transformam o navegador em um "Bus de Eventos". Quando você usa CustomEvents, o Time A pode trocar React por Vue sem que o Time B (em Angular) sequer perceba.*
