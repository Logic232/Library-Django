const e = (() => {
    let qs = (c) => document.querySelector(c);
    let qsa = (c) => [...document.querySelectorAll(c)];
    return {
        profileImage: qs(".profile-picture"),
        navigationWrapper: qs(".navigation"),
        findBookInput: qs(".find-book"),
        booksToFind: qsa(".book-to-find"),
        booksList: qsa(".book-image"),
        bookYearInput: qs("[name=book_year]")
    };
})();

const ChangeMaxNumberValue = (() => {
    if (!e.bookYearInput) return;
    e.bookYearInput.setAttribute("max", "2022");
    e.bookYearInput.setAttribute("maxLength", "4");
})();
const CheckImage = (image) => {
    const newImage = new Image();
    // const request = new XMLHttpRequest();
    // request.open("GET", image.src, true);
    // request.send();
    // request.onload = () => {
    //     console.log(request.status);
    //     if (request.status !== 200) {
    //         image.src = "https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png";
    //         image.classList.add("border");
    //     }
    // };
    // request.onerror = (err) => {
    //     console.error(err);
    // };
    newImage.src = image.src;
    newImage.onerror = () => {
        image.src = "https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png";
    };
};
const DetectIfImagesAreValid = (() => {
    if (e.booksList.length === 0) return;
    e.booksList.map((book) => CheckImage(book));
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
if (e.findBookInput)
    e.findBookInput.addEventListener(
        "input",
        debounce((event) => FindBookHandler(event))
    );
e.profileImage.addEventListener("click", ToggleMenu);

function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}
