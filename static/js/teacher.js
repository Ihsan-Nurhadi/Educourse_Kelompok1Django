let products = {
    data: [
        {
            productName: "OSN Bidang Biologi 2024",
            category: "Biologi",
            price: "0",
            image: "sains.jpg",
        },
        {
            productName: "OSN Bidang Kimia 2024",
            category: "Kimia",
            price: "0",
            image: "sains.jpg",
        },
        {
            productName: "OSN Bidang Fisika 2024",
            category: "Fisika",
            price: "0",
            image: "sains.jpg",
        },
        {
            productName: "OSN Bidang Matematika 2024",
            category: "Matematika",
            price: "0",
            image: "math.jpg",
        },
        {
            productName: "OSN Bidang Bahasa Inggris 2024",
            category: "English",
            price: "0",
            image: "english.jpg",
        },
    ],
};

for (let i of products.data) {
    // create card
    let card = document.createElement("div");
    // Card should have category and shoul stay hidden initialy
    card.classList.add("card", i.category, "hide");
    // image  div
    let imgContainer = document.createElement("div");
    imgContainer.classList.add("image-container");
    // img tag
    let image = document.createElement("img");
    image.setAttribute("src", i.image);
    imgContainer.appendChild(image);
    card.appendChild(imgContainer);
    // container
    let container = document.createElement("div");
    container.classList.add("container");
    // product name
    let name = document.createElement("h5");
    name.classList.add("product-name");
    name.innerText = i.productName.toUpperCase();
    container.appendChild(name);
    // price
    let price = document.createElement("h6");
    price.innerText = "Rp. " + i.price
    container.appendChild(price);

    card.appendChild(container)
    document.getElementById("products").appendChild(card);
}

// parameter passed from button (parameter same as category)
function filterProduct(value) {
    // button class code
    let buttons = document.querySelectorAll(".button-value");
    buttons.forEach((button) => {
        // check if value equals innerText
        if (value.toUpperCase() == button.innerText.
        toUpperCase()) {
            button.classList.add("active");
        } else{
            button.classList.remove("active")
        }
    });

    let elements = document.querySelectorAll(".card");

    elements.forEach((element) => {

        if(value == "all"){
            element.classList.remove("hide");
        }
        else{
            if(element.classList.contains(value)){

                element.classList.remove("hide");
            }
            else{
                element.classList.add("hide");
            }
        }
    });
}

// initially display all products
window.onload = () =>{
    filterProduct("all");
}
