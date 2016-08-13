/**
 * Created by tomi on 13/08/16.
 */

const httpRequest = new XMLHttpRequest();

const url_form = document.getElementById('url_form');
const full_url_input = document.getElementById('full_url_input');
const short_url_response = document.getElementById('short_url_response');

url_form.addEventListener("submit", function (e){
    e.preventDefault();
    shorten_url(full_url_input.value)
}, false);

function shorten_url(full_url) {
    http_post('/url', {'full_url': full_url}, function (response) {
        let json_response = JSON.parse(response);
        short_url_response.innerHTML = json_response.short_url
    })
}

function http_post(url, params, callback) {
    if (!httpRequest) {
      alert('Error: Cannot use xmlhttp request');
      return false;
    }
    const encoded_params = Object.keys(params).map(function(key) {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key])
    }).join('&');

    httpRequest.onreadystatechange= function() {
        if (httpRequest.readyState == 4) {
            callback(httpRequest.responseText);
        }
    };
    httpRequest.open("POST", url, true);
    httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    httpRequest.send(encoded_params);
}
