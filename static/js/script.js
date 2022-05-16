const e = (() => {
    let qs = (c) => document.querySelector(c);
    let qsa = (c) => [...document.querySelectorAll(c)];
    return {
        profileImage: qs(".profile-picture"),
        navigationWrapper: qs(".navigation")
    };
})();

const ToggleMenu = () => {
    e.navigationWrapper.classList.toggle("active");
};

e.profileImage.addEventListener("click", ToggleMenu);
