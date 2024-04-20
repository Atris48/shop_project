var button2 = document.getElementById('password-button')
button2.style.display = 'none'

function check_password_input() {
    var button = document.getElementById('otp-button')
    var pass_inp = document.getElementById('password')
    if (button) {
        if (pass_inp.value.length > 0) {
            button.style.display = 'none'
            button2.style.display = 'block'
        } else {
            button.style.display = 'block'
            button2.style.display = 'none'
        }
    }

}