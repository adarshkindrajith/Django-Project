document.addEventListener("DOMContentLoaded", function () {
    const updateTotals = (amount, totalWithShipping) => {
        document.getElementById("total-amount").textContent = `Rs.${amount}`;
        document.getElementById("total-with-shipping").textContent = `Rs.${totalWithShipping}`;
    };

    const showCartEmptyMessage = () => {
        const cartContainer = document.querySelector(".container .row");
        cartContainer.innerHTML = `
            <h1 class="text-center mb-5">Cart Empty</h1>
        `;
    };

    // Handle increment (plus button)
    document.querySelectorAll(".plus-cart").forEach(button => {
        button.addEventListener("click", function () {
            let prod_id = this.getAttribute("pid");
            fetch(`/plus-cart/?prod_id=${prod_id}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.quantity) {
                    this.previousElementSibling.textContent = data.quantity;

                    // Update totals
                    updateTotals(data.amount, data.total_amount);
                }
            })
            .catch(error => console.error("Error updating cart:", error));
        });
    });

    // Handle decrement (minus button)
    document.querySelectorAll(".minus-cart").forEach(button => {
        button.addEventListener("click", function () {
            let prod_id = this.getAttribute("pid");
            fetch(`/minus-cart/?prod_id=${prod_id}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.action === "updated") {
                    this.nextElementSibling.textContent = data.quantity;

                    // Update totals
                    updateTotals(data.amount, data.total_amount);
                } else if (data.action === "deleted") {
                    this.closest(".row").remove();

                    // Update totals
                    updateTotals(data.amount, data.total_amount);

                    if (data.cart_empty) {
                        showCartEmptyMessage();
                    }
                }
            })
            .catch(error => console.error("Error updating cart:", error));
        });
    });

    // Handle remove button
    document.querySelectorAll(".remove-cart").forEach(button => {
        button.addEventListener("click", function () {
            let prod_id = this.getAttribute("pid");
            fetch(`/remove-cart/?prod_id=${prod_id}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.action === "deleted") {
                    this.closest(".row").remove();

                    // Update totals
                    updateTotals(data.amount, data.total_amount);

                    if (data.cart_empty) {
                        showCartEmptyMessage();
                    }
                }
            })
            .catch(error => console.error("Error removing item:", error));
        });
    });
});
