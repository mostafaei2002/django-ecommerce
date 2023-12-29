const navTabs = document.querySelector(".nav-tabs");
const tabBtns = document.querySelectorAll(".nav-tabs .nav-link");
const tabIDs = ["tab-description", "tab-reviews"];

navTabs.addEventListener("click", (e) => {
    const targetTabBtn = e.target.closest(".nav-link");
    console.log(targetTabBtn);
    tabBtns.forEach((tab) => tab.classList.remove("active"));

    targetTabBtn.classList.add("active");
    const targetTabID = targetTabBtn.dataset.target;
    console.log(targetTabID);

    tabIDs.forEach((tabID) => {
        const tab = document.getElementById(tabID);
        tab.classList.add("d-none");
    });

    const targetTab = document.getElementById(targetTabID);
    targetTab.classList.remove("d-none");
});
