

document.getElementById('swap-button').addEventListener('click', function() {
    var startInput = document.querySelector('.start-station');
    var endInput = document.querySelector('.end-station');
    var tempValue = startInput.value;
    startInput.value = endInput.value;
    endInput.value = tempValue;
});