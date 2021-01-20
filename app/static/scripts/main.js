window.onresize = function(){
    addMediaQuery()
}

function savePostTitle(){
    const x = document.getElementById('post-title').value;
    if(x == ''){
        return false;
    }
    else{
        localStorage.setItem('title', x);
    }
}

function checkStorageForTitle(){
    if(localStorage.getItem('title') != null){
        document.getElementById('title').value=localStorage.getItem('title');
        localStorage.removeItem('title');
    }
}

function changeNavPosition(){
    if(document.querySelector('.logged-in-nav') !== null){
        document.getElementById('front-nav').style.top = '60px';
        document.querySelector('.home-content').style.marginTop = '100px';
    }
}

function addMediaQuery(){
    const x = document.getElementsByClassName('home-content')[0];
    if(document.querySelector('.logged-in-nav') == null){
        if(window.matchMedia('(max-width:1200px)').matches){
            x.style.position = 'relative';
            x.style.top = '100px';
        }
        else{
            x.style.top = '0';
        }
    }
}

function openNav(){
    document.getElementsByClassName('mobile-links')[0].classList.add('menu-in');
    document.getElementsByClassName('fa-bars')[0].style.display = 'none';
    document.getElementsByClassName('fa-times')[0].style.display = 'block';
}

function closeNav(){
    document.getElementsByClassName('mobile-links')[0].classList.remove('menu-in');
    document.getElementsByClassName('mobile-links')[0].classList.remove('menu-out');
    document.getElementsByClassName('fa-bars')[0].style.display = 'block';
    document.getElementsByClassName('fa-times')[0].style.display = 'none';
}

function showNewsletterForm(){
    document.getElementsByClassName('mail-chimp-form')[0].style.display = 'block';
    document.getElementById('email-sub-btn').onclick = hideNewsletterForm;
}

function hideNewsletterForm(){
    document.getElementsByClassName('mail-chimp-form')[0].style.display = 'none';
    document.getElementById('email-sub-btn').onclick = showNewsletterForm;
}

function previewPostValues(){
    if(localStorage.getItem('title')){
        document.getElementsByClassName('view-post-title')[0].innerHTML = localStorage.getItem('title');
        document.getElementById('preview-category').innerHTML = localStorage.getItem('category');
        document.getElementsByClassName('post-content-wrapper')[0].innerHTML = localStorage.getItem('content');
        localStorage.removeItem('title');
    }
}

function confirmDelete(id){
    console.log(id);
    const x = confirm("Are you sure you wish to delete this post?")
    if(x == true){
        window.location.replace(`/dashboard/delete/${id}`)
    }
}