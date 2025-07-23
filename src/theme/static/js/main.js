document.addEventListener("DOMContentLoaded", () => {
    const cartButton = document.getElementById("cart-button");
    const cartCount = document.getElementById("cart-count");
    let count = 0;

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", () => {
            count++;
            cartCount.textContent = count;
            alert("Produto adicionado ao carrinho!");
        });
    });

});