/**
 * Created by tomi on 13/08/16.
 */

const httpRequest = new XMLHttpRequest();

const url_form = document.getElementById('url_form');
const url_form_wrapper = document.getElementById('new_url_form_wrapper');
const full_url_input = document.getElementById('full_url_input');
const short_url_response_wrapper = document.getElementById('short_url_response_wrapper');
const short_url_response = document.getElementById('short_url_response');
const short_url_copy_target = document.getElementById('short_url_copy_target');
const copy_short_url_button = document.querySelector('#copy_short_url_button');


url_form.addEventListener("submit", function (e){
    e.preventDefault();
    shorten_url(full_url_input.value);
    url_form_wrapper.classList.add('hidden');
    setTimeout(function(){
        url_form_wrapper.classList.remove('hidden');
    }, 6000);
}, false);

copy_short_url_button.addEventListener('click', function(e) {
        short_url_copy_target.select();

        try {
            let successful = document.execCommand('copy');
            let msg = successful ? 'Copied text successfully' : 'Failed to copy text';
            if (successful) {
                document.getElementById('short_url_copy_modal__success').classList.remove('hidden')
            } else {
                document.getElementById('short_url_copy_modal__error').classList.remove('hidden')
            }
            $('#short_url_copy_success_modal').modal()
        } catch(err) {
            console.error('Error copying short url');
            console.error(err);
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
