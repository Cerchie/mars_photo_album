const faveBtn = document.getElementById("fave-btn");

toggle = () => {
    faveBtn.classList.toggle("bg-success");
}

faveBtn.addEventListener('click', function (evt) {
    evt.preventDefault;
    console.log('clicked');
});