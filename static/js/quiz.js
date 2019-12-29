const quizWrapper = document.querySelector('.quiz-wrapper');
const ageSlider = document.querySelector('#age-slider');
const loanSlider = document.querySelector('#loan-slider');
const termSlider = document.querySelector('#term-slider');
const salary = document.querySelector('#salary');
const quizBack = document.querySelector('#quiz-back');
const quizProceed = document.querySelector('#quiz-proceed');
const quizRows = document.querySelectorAll('.quiz >.row');
const quizLoading = document.querySelector('.quiz-loading');
const quizResults = document.querySelector('.quiz-results');
const resultsBox = document.querySelectorAll('.results-box');
const zeroPercent = document.querySelectorAll('.zero-percent');
const badHistory = document.querySelectorAll('.bad-history');
const otherOffers = document.querySelectorAll('.other-offers');
const toggleZero = document.querySelector('#zero');
const toggleHistory = document.querySelector('#history');
const quizClose = document.querySelector('#quiz-close');
const quizOpen = document.querySelector('#open-quiz');
const quizOpenMenu = document.querySelector('#open-quiz-menu');

var yellowRangeValue = function(){
  var newValue = ageSlider.value;
  var target = document.querySelector('#age');
  target.innerHTML = newValue;
  ageSlider.style.background = 'linear-gradient(to right, #fab309 0%, #fab309 ' + ((this.value - parseFloat(18)) / parseFloat(0.57) - 10)  + '%, #ddd ' + ((this.value - parseFloat(18)) / parseFloat(0.57)) + '%, #ddd 100%)'
};

var blueRangeValue = function(){
  var newValue = loanSlider.value;
  var target = document.querySelector('#loan');
  target.innerHTML = newValue;
  loanSlider.style.background = 'linear-gradient(to right, #00b7f4 0%, #00b7f4 ' + ((this.value - parseFloat(1000)) / parseFloat(990) - 10)  + '%, #ddd ' + ((this.value - parseFloat(990)) / parseFloat(990)) + '%, #ddd 100%)'
};

var greenRangeValue = function(){
  var newValue = termSlider.value;
  var target = document.querySelector('#term');
  target.innerHTML = newValue;
  termSlider.style.background = 'linear-gradient(to right, #4bae29 0%, #4bae29 ' + ((this.value - parseFloat(1)) / parseFloat(3.64) - 10)  + '%, #ddd ' + ((this.value - parseFloat(3.64)) / parseFloat(3.64)) + '%, #ddd 100%)'
};

var salaryCheckbox = function(){
    var yes = document.querySelector('.y');
    var no = document.querySelector('.n');
    if(this.checked) {
        yes.style.display = 'none';
        no.style.display = 'block';
    } else {
        yes.style.display = 'block';
        no.style.display = 'none';
    }
};

var backButton = function(){
    quizWrapper.style.animation = 'fadeout 0.5s linear forwards';
    quizWrapper.style.webkitAnimation = 'fadeout 0.5s linear forwards';
    setTimeout(function() {
        quizWrapper.style.display = 'none';
        quizWrapper.style.animation = 'none';
        quizWrapper.style.webkitAnimation = 'none';
    }, 500);
};


var proceedButton = function() {
    quizRows.forEach(function(row) {
        row.style.animation = 'fadeout 0.5s linear forwards';
        row.style.webkitAnimation = 'fadeout 0.5s linear forwards';
    });
    setTimeout(function() {
        quizRows.forEach(function(row) {
        row.style.display = 'none';
    });
        quizLoading.style.display = "block";
    }, 500);
    setTimeout(function() {
        quizLoading.style.display = "none";
        showQuizResults()
    }, 6500);
};

var showQuizResults = function() {
    quizResults.style.display = 'block';

    if (toggleHistory.checked) {
        badHistory.forEach(function(el) {
            el.style.display = "flex";
        })
    }
    else if (toggleZero.checked) {
        zeroPercent.forEach(function(el) {
            el.style.display = "flex";
        })
    }
    else {
        otherOffers.forEach(function(el) {
            el.style.display = "flex";
        })
    }
};

var closeQuiz = function() {
    resultsBox.forEach(function(el) {
        el.style.display = "none";
    });
    quizResults.style.display = 'none';
    quizWrapper.style.display = 'none';
    quizRows.forEach(function(row) {
        row.style.animation = 'none';
        row.style.webkitAnimation = 'none';
        if (window.screen.width < 640) {
            row.style.display = 'block';
        }
        else {
            row.style.display = 'flex';
        }
    });
};

var openQuiz = function() {
    quizWrapper.style.display = 'block';
    quizWrapper.style.animation = 'fadein 0.5s linear forwards';
    quizWrapper.style.webkitAnimation = 'fadein 0.5s linear forwards';
};


ageSlider.addEventListener("input", yellowRangeValue);
loanSlider.addEventListener("input", blueRangeValue);
termSlider.addEventListener("input", greenRangeValue);
salary.addEventListener("change", salaryCheckbox);

quizBack.addEventListener('click', backButton);
quizProceed.addEventListener('click', proceedButton);
quizClose.addEventListener('click', closeQuiz);
quizOpen.addEventListener('click', openQuiz);
quizOpenMenu.addEventListener('click', openQuiz);

