const e = (() => {
    let qs = (c) => document.querySelector(c);
    let qsa = (c) => [...document.querySelectorAll(c)];
    return {
        profileImage: qs(".profile-picture"),
        navigationWrapper: qs(".navigation"),
        findBookInput: qs(".find-book"),
        booksToFind: qsa(".book-to-find")
    };
})();

const ToggleMenu = () => {
    e.navigationWrapper.classList.toggle("active");
};

const FindBookHandler = ({ target }) => {
    let value = target.value.toLowerCase();
    e.booksToFind.forEach((el) => {
        let parsedHTML = el.innerHTML.toLowerCase();
        parsedHTML.includes(value) ? el.classList.remove("hidden") : el.classList.add("hidden");
    });
};
if (window.location.pathname === "/loans/")
    e.findBookInput.addEventListener(
        "input",
        debounce((event) => FindBookHandler(event))
    );
e.profileImage.addEventListener("click", ToggleMenu);

function debounce(func, timeout = 500) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}
