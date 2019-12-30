const quizOpen = document.querySelector('#open-quiz');
const quizOpenMenu = document.querySelector('#open-quiz-menu');
const quizOpenStripe = document.querySelector('#quiz-open-stripe');

var navModal = document.getElementById("nav-mobile");
var navBtn = document.getElementById("nav-menu");
var navClose = document.getElementById("nav-close");

navBtn.onclick = function() {
  navModal.style.display = "block";};

navClose.onclick = function() {
  navModal.style.display = "none";};

window.onclick = function(event) {
  if (event.target === navModal) {
    navModal.style.display = "none";
  }
};

var openQuiz = function() {
    quizWrapper.style.display = 'block';
    quizWrapper.style.animation = 'fadein 0.5s linear forwards';
    quizWrapper.style.webkitAnimation = 'fadein 0.5s linear forwards';
};


quizOpen.addEventListener('click', openQuiz);
quizOpenMenu.addEventListener('click', openQuiz);
quizOpenStripe.addEventListener('click', openQuiz);