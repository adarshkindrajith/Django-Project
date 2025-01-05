document.addEventListener("DOMContentLoaded", function () {
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
                    // Update quantity
                    this.previousElementSibling.textContent = data.quantity;

                    // Update totals
                    document.getElementById("total-amount").textContent = `Rs.${data.amount}`;
                    document.getElementById("total-with-shipping").textContent = `Rs.${data.total_amount}`;
                }
            });
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
                    // Update quantity
                    this.nextElementSibling.textContent = data.quantity;

                    // Update totals
                    document.getElementById("total-amount").textContent = `Rs.${data.amount}`;
                    document.getElementById("total-with-shipping").textContent = `Rs.${data.total_amount}`;
                } else if (data.action === "deleted") {
                    // Remove the item row if deleted
                    this.closest(".row").remove();

                    // Update totals
                    document.getElementById("total-amount").textContent = `Rs.${data.amount}`;
                    document.getElementById("total-with-shipping").textContent = `Rs.${data.total_amount}`;
                }
            });
        });
    });
});







document.addEventListener("DOMContentLoaded", function () {
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
                    // Remove the item row from the DOM
                    this.closest(".row").remove();

                    // Update totals
                    document.getElementById("total-amount").textContent = `Rs.${data.amount}`;
                    document.getElementById("total-with-shipping").textContent = `Rs.${data.total_amount}`;
                }
            });
        });
    });
});
    
