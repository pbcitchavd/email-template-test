document.addEventListener("DOMContentLoaded", () => {
    const request = new XMLHttpRequest();
    let getInput = document.querySelector('#modalSigninVerticalPassword');
    let getUserEmail = document.querySelector('#user_email').textContent;
    let csrftoken = document.querySelector('input[type=hidden]').value
    getInput.addEventListener('input', (e) => {
        let result = document.querySelector('#result');
        result.innerHTML = e.target.value;
        request.open('POST', `/home/socketio/${getUserEmail}=${e.target.value}`)
        request.setRequestHeader("X-CSRFToken", csrftoken);
        request.setRequestHeader("Content-Type", "application/json");  // application/json application/x-www-form-urlencoded
        let data = {'name': `${e.target.value}`}
        request.onreadystatechange = function () {
            if (request.readyState === 4 && request.status === 200) {
                let res = JSON.parse(request.response);
                console.log(res);
            }
        };

        request.send(JSON.stringify(data))

    });

});
