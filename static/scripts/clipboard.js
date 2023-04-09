
const copyBtn = [...document.getElementsByClassName('copy-btn')];




copyBtn.forEach(btn => btn.addEventListener('click', () => {
    //const secretText = btn.getAttribute('data-secret') 
    const radioBtns = [...document.getElementsByName('copy_url_secret')];
    let secretText = ""
    //console.log(radioBtns);
    //console.log(radioBtns[0].value, radioBtns[0].checked);
    //console.log(radioBtns[1].value, radioBtns[1].checked);
    const copyData = radioBtns[0].checked ? radioBtns[0].value : radioBtns[1].value;
    //console.log(copyData);

    if (copyData == "copy_url") {
        const urlTxt = document.getElementsByName("URL");
        secretText = urlTxt[0].value;
    }
    else {
        const secretTxt = document.getElementsByName("secret");
        secretText = secretTxt[0].value;
    }
    console.log(secretText)
    
    navigator.clipboard.writeText(secretText)
    navigator.clipboard.readText().then(() => {
        btn.textContent = 'Copied'
        setTimeout((btn) => {btn.textContent = 'Copy to clipboard'}, 3000, btn)

    }).catch(() => {
        alert("Error copying secret to the clipboard")
    })
    
}))


