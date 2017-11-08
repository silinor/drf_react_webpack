require('es6-promise').polyfill();
require('isomorphic-fetch');

export function request(url, options) {
    return fetch(url, options)
        .then(function (response) {
            return response.json();
        })
}