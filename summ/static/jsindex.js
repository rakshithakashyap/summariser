
//header fix
window.onscroll = function () {
    const docScrollTop = document.documentElement.scrollTop;

    if (window.innerWidth > 991) {
        if (docScrollTop > 100) {
            document.querySelector("header").classList.add("fixed")
        }
        else {
            document.querySelector("header").classList.remove("fixed")
        }
    }
}

//active to live bar during scroll
const mynavbar = document.querySelector(".mynavbar");
a = mynavbar.querySelectorAll("a");

a.forEach(function (element) {
    element.addEventListener("click", function () {
        for (let i = 0; i < a.length; i++) {
            a[i].classList.remove("active");
        }
        this.classList.add("active")
        document.querySelector(".mynavbar").classList.toggle("show");
    })
})

const hamburger = document.querySelector(".ham-burger");
hamburger.addEventListener("click", function () {
    document.querySelector(".mynavbar").classList.toggle("show");
})
