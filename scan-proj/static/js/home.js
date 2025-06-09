


 
// function home() { window.open("file:///C:/Users/m/Desktop/scancle/home%20page.html  " , "_self") ; }
/*
function scrollWin() { window.open("/profile"   , "_self") ; }
  function fun() { window.location.href("/scan"   , "_self") ; }

  function logout() { window.open("login" , "_self") ; } 
  function fun2() { window.open("/scan"   , "_self") ; }
*/
// Scroll to the profile section
function scrollWin() {
  document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
}

// Scroll to the scan section
function fun() {
  document.getElementById('about').scrollIntoView({ behavior: 'smooth' });
}

// Scroll to the login section
function logout() { window.open("/login" , "_self") ; } 


// Scroll to the scan section (same as fun)
function fun2() {
  document.getElementById('pricing').scrollIntoView({ behavior: 'smooth' });
}


function scan() { window.open("/scan"   , "_self") ; }

document.querySelector('.hamburger').addEventListener('click', function () {

  document.querySelector('.nav-links').style.left='0';
  document.getElementById('overlay').style.display = 'block'; /* Semi-transparent black */

});

document.querySelector('.sidebar-close').addEventListener('click', function (e) {
  e.preventDefault();
  document.querySelector('.nav-links').style.left = '-100%';
  document.getElementById('overlay').style.display = 'none';

});

document.querySelectorAll('.nav-link').forEach(function (link) {
  link.addEventListener('click', function () {
    document.querySelector('.nav-links').style.left = '-100%';
    document.getElementById('overlay').style.display = 'none';
  });
})

document.getElementById('overlay').addEventListener('click', function () {
  document.querySelector('.nav-links').style.left = '-100%';
  document.getElementById('overlay').style.display = 'none';
});