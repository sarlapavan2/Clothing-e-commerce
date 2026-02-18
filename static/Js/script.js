// hamburger Menu

const menuToggle = document.getElementById("menu-toggle");
const CloseBtn = document.getElementById("close-btn");
const overLay = document.getElementById("overlay");
const navMenu = document.getElementById("nav");

menuToggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
    overLay.classList.toggle("active");
});

CloseBtn.addEventListener("click", () => {
    navMenu.classList.remove("active");
    overLay.classList.remove("active");
});

// why should Choose Us

let count = document.querySelectorAll(".count"); // selects all the html elements with classname count- NodeList
let arr = Array.from(count); // NodeList - javascript array -map()

arr.map(function(item){
    let startnumber = 0;

    function counterup(){
        startnumber++;
        item.innerHTML = startnumber;

        if (startnumber == item.dataset.number){
        clearInterval(stopnumber);
        }
    }
    
    let stopnumber = setInterval(function()
    {
        counterup()
    }, 50)
})

// function validation 

function validationForm(){

    let isValid = true;  //isvalis submit form or not

    // clear previous error messages
    document.getElementById("name-error").textContent = "";
    document.getElementById("email-error").textContent = "";
    document.getElementById("phone-error").textContent = "";
    document.getElementById("courses-error").textContent = "";

    // Name Validation

    const name = document.getElementById("name").value;

    if (name == ''){
        document.getElementById("name-error").textContent = "Name is Required!";
        isValid = false;
    }

    // Email Validation

    const email = document.getElementById("email").value;
    const EmailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (email == ''){
        document.getElementById("email-error").textContent = "Email is Required!";
        isValid = false;
    }
    else if (!EmailPattern.test(email)) {
        document.getElementById("email-error").textContent = "Email is is in Invalid Format!";
        isValid = false;
    }

    // Phone Validation

    const phone = document.getElementById("phone").value;
    const PhonePattern = /^[6-9]\d{9}$/;

    if (phone == ''){
        document.getElementById("phone-error").textContent = "Phone is Required!";
        isValid = false;
    }
    else if (!PhonePattern.test(email)) {
        document.getElementById("phone-error").textContent = "Phone is is in Invalid Format!";
        isValid = false;
    }

    return isValid;
}

// API calling - axios

let tableBody = document.getElementById("tablebody"); // select the table body

axios.get("https://jsonplaceholder.typicode.com/todos/")
.then(function(response){
    const data = response.data
    if (data){
        data.forEach(function(item){
            tableBody.innerHTML +=  
            `<tr>
            <td>${item.userId}</td>
            <td>${item.id}</td>
            <td>${item.title}</td>
            <td>${item.completed}</td>
            </tr>
            `
        })
    }
})