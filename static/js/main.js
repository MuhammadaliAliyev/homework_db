"use strict";

function showNotification(message, type) {
    var notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? 'green' : 'red';
    notification.style.color = 'white'
    notification.style.display = 'block';

    setTimeout(() => {
        notification.style.display = 'none';
    }, 1000);
}

function checkAnswer() {
    var form = document.getElementById('testForm');
    var selectedOption = form.querySelector('input[name="answer"]:checked');
    var correctOption = form.querySelector('input[name="correct_option"]').value;

    if (selectedOption) {
        var selectedValue = selectedOption.value;
        
        if (selectedValue === correctOption) {
            showNotification("Correct","success")
            setTimeout(() => form.submit(), 500);
        } else {
            showNotification('Incorrect','error')
            clearRadioSelection();
        }
    } else {
        alert('Iltimos, biron bir javob tanlang.');
    }
    return false;
}

function clearRadioSelection() {
    console.log("radio buttonlarni tozalash");
    var radioButtons = document.querySelectorAll('input[name="answer"]');
    radioButtons.forEach(function(radio) {
        console.log("uuuuuu");
        radio.checked = false;
    });
}

function jumpToCategory(categoryId) {
    window.location.href = `#${categoryId}`;
}

// Get the button
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}