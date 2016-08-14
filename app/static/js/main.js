/**
 * Created by tomi on 13/08/16.
 */

const httpRequest = new XMLHttpRequest();

const url_form = document.getElementById('url_form');
const full_url_input = document.getElementById('full_url_input');
const short_url_response_wrapper = document.getElementById('short_url_response_wrapper');
const short_url_response = document.getElementById('short_url_response');
const short_url_copy_target = document.getElementById('short_url_copy_target');
const copy_short_url_button = document.querySelector('#copy_short_url_button');


url_form.addEventListener("submit", function (e){
    e.preventDefault();
    shorten_url(full_url_input.value)
}, false);

copy_short_url_button.addEventListener('click', function(e) {
      short_url_copy_target.select();

      try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'Copied text successfully' : 'Failed to copy text';
        alert(msg)
      } catch(err) {
        console.log('Copy error');
      }
    }
);

function shorten_url(full_url) {
    http_post('/url', {'full_url': full_url}, function (response) {
        let json_response = JSON.parse(response);
        short_url_response.innerHTML = window.location.href + json_response.short_url;
        short_url_copy_target.value = window.location.href + json_response.short_url;
        short_url_response.href = window.location.href + json_response.short_url;
        short_url_response_wrapper.classList.remove("hidden");
        copy_short_url_button.classList.remove("hidden");
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
