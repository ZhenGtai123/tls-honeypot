'use strict';

const extcf7Metabox = document.getElementById("extcf7-metabox");
if(extcf7Metabox) {
    const clone = extcf7Metabox.cloneNode(true),
        cf7FormEditor = document.getElementById("contact-form-editor");
    cf7FormEditor.appendChild(clone);
    extcf7Metabox.style.display = 'block';
    extcf7Metabox.parentNode.removeChild(extcf7Metabox);
}

const htcf7extSidebarTabButton = document.querySelectorAll('.extcf7-metabox-sidebar-tab button');
htcf7extSidebarTabButton.forEach(function(button, index) {
    if (index === 0) {
        const toggle = button.dataset.toggle,
            target = document.getElementById(toggle);
        button.classList.add('active');
        target.style.display = "block";
    }
    button.addEventListener('click', function() {
        if(!this.classList.contains("active")) {
            const toggle = this.dataset.toggle,
                target = document.getElementById(toggle);
            this.closest('.extcf7-metabox-sidebar-tab').querySelectorAll('button').forEach(function(item) {
                item.classList.remove('active');
            })
            this.classList.add('active');
            target.closest('.extcf7-metabox-tab-content').querySelectorAll('.extcf7-metabox-tab-pane').forEach(function(item) {
                item.style.display = "none";
            })
            target.style.display = "block";
        }
    })
})

const htcf7extTabButton = document.querySelectorAll('.htcf7ext-tab-nav button');
htcf7extTabButton.forEach(function(button) {
    button.addEventListener('click', function() {
        if(!this.classList.contains("active")) {
            const toggle = this.dataset.toggle,
                target = document.getElementById(toggle);
            this.closest('.htcf7ext-tab-nav').querySelectorAll('button').forEach(function(item) {
                item.classList.remove('active');
            })
            this.classList.add('active');
            target.closest('.extcf7-tab-content').querySelectorAll('.extcf7-tab-pane').forEach(function(item) {
                item.style.display = "none";
            })
            target.style.display = "block";
        }
    })
})