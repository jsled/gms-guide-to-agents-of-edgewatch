function beta_features(evt) {
    params = new URLSearchParams(window.location.search);
    for (const [key,value] of params) {
        if ('beta' === key && ('' == value || 'true' === value)) {
            beta_elts = document.getElementsByClassName('beta');
            for (const key in Array.from(beta_elts)) {
                const elt = beta_elts[key];
                elt.setAttribute('style', '');
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", beta_features);
