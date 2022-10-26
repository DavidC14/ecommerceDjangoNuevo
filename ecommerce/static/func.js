const sumar = document.getElementById('sumar')
const restar = document.getElementById('restar')
const cant = document.getElementById('cant')
total = 0
console.log(1)

sumar.addEventListener('click', (e)=>{
    e.preventDefault()
    total += 1
    cant.innerHTML = total

})

restar.addEventListener('click', (e)=>{
    e.preventDefault()
    total -= 1
    cant.innerHTML = total

})

