
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
    let copyTxt;
    if (copyData == "copy_url") {
        copyTxt = document.getElementsByName("URL");
        copyTxt[0].select();
        copyTxt[0].setSelectionRange(0, 99999);
        
    }
    else {
        copyTxt = document.getElementsByName("secret");
        copyTxt[0].select();
        copyTxt[0].setSelectionRange(0, 99999);
    }
    console.log(copyTxt[0].value)
    
    navigator.clipboard.writeText(copyTxt[0].value)
    navigator.clipboard.readText().then(() => {
        btn.textContent = 'Copied'
        setTimeout((btn) => {btn.textContent = 'Copy to clipboard'}, 3000, btn)

    }).catch(() => {
        alert("Error copying secret to the clipboard")
    })
    
}))


