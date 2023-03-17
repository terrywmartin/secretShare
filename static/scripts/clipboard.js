
const copyBtn = [...document.getElementsByClassName('copy-btn')]


copyBtn.forEach(btn => btn.addEventListener('click', () => {
    const secretText = btn.getAttribute('data-secret') 
    navigator.clipboard.writeText(secretText)
    navigator.clipboard.readText().then(() => {
        btn.textContent = 'Copied'
        setTimeout((btn) => {btn.textContent = 'Copy to clipboard'}, 3000, btn)

    }).catch(() => {
        alert("Error copying secret to the clipboard")
    })
    
}))


