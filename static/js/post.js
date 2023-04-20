const form = document.querySelector("form")

form.onsubmit = function(event) {
    event.preventDefault();
    var data = {}
    for (var i = 0, ii = form.length; i < ii; ++i) {
        var input = form[i];
        if (input.name == "house") {
            data[input.name] = parseInt(input.value);
            continue;
        }
        if (input.name != "") {
            data[input.name] = input.value;
        }
    }

    var post_request = {
        "shop" : data
    }

    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    // send the collected data as JSON
    xhr.send(JSON.stringify(post_request));

    xhr.onloadend = function () {
        window.location.replace("/shop/");
    };
    xhr.onerror = function () {
        window.location.replace("/shop/");
        alert("Ошибка запроса");
    }
} 

