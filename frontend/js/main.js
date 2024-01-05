const hideList = document.querySelectorAll(".hide-after-5");

hideList.forEach((el) => {
    setTimeout(() => {
        el.classList.remove("show");
    }, 5000);
});
