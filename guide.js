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

function build_sidebar(evt) {
    // document.getElementById('text-table-of-contents').setAttribute('sidebarjs','');
    console.log('FIXME: delete this ->', document.getElementById('table-of-contents'));
    // const sidebarjs = new SidebarJS.SidebarElement({position: 'right'})

    // enumerate h2-h3 elts, transform into <nav>
    
}

document.addEventListener("DOMContentLoaded", build_sidebar);
