let selectedHour = 0;
let selectedMinute = 0;

function setHour(hour) {
  selectedHour = hour;
  document.getElementById('hourValue').textContent = `${hour < 10 ? '0' : ''}${hour}시`;
  toggleHourLayer(); // 시간을 선택하면 리스트를 닫음
}

function setMinute(minute) {
  selectedMinute = minute;
  document.getElementById('minuteValue').textContent = `${minute < 10 ? '0' : ''}${minute}분`;
  toggleMinuteLayer(); // 분을 선택하면 리스트를 닫음
}

function changeHour(amount) {
  selectedHour = (selectedHour + amount) % 24;
  if (selectedHour < 0) {
    selectedHour += 24;
  }
  document.getElementById('hourValue').textContent = `${selectedHour < 10 ? '0' : ''}${selectedHour}시`;
}

function changeMinute(amount) {
  selectedMinute = (selectedMinute + amount) % 60;
  if (selectedMinute < 0) {
    selectedMinute += 60;
  }
  document.getElementById('minuteValue').textContent = `${selectedMinute < 10 ? '0' : ''}${selectedMinute}분`;
}

function toggleHourLayer() {
  const hourLayer = document.querySelector('.layer_timeset.hour');
  hourLayer.hidden = !hourLayer.hidden;
}

function toggleMinuteLayer() {
  const minuteLayer = document.querySelector('.layer_timeset.minute');
  minuteLayer.hidden = !minuteLayer.hidden;
}

function showSelectedTime() {
  const selectedHour = getHour();
  const selectedMinute = getMinute();

  // 선택한 시간과 분을 문자열로 조합하여 출력
  const selectedTime = `${selectedHour < 10 ? "0" : ""}${selectedHour}시 ${selectedMinute < 10 ? "0" : ""}${selectedMinute}분`;
  document.getElementById('selected-time').textContent = selectedTime;
}

function getHour() {
  return selectedHour;
}

function getMinute() {
  return selectedMinute;
}

function updateCurrentTime() {
  const currentTime = new Date();
  const hours = currentTime.getHours();
  const minutes = currentTime.getMinutes();

  let timeString = '';
  if (hours < 12) {
    timeString = '오전 ';
  } else {
    timeString = '오후 ';
    hours -= 12;
  }

  timeString += (hours < 10 ? '0' : '') + hours + ':';
  timeString += (minutes < 10 ? '0' : '') + minutes;

  document.getElementById('selected-time').textContent = timeString;
}

function setToCurrentTime() {
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  const currentMinute = currentTime.getMinutes();
  setHour(currentHour);
  setMinute(currentMinute);
  showSelectedTime();
  toggleMinuteLayer();
  toggleHourLayer();
}

// 1초마다 시간 업데이트 함수 호출하여 현재 시간을 업데이트합니다.
setInterval(updateCurrentTime, 30000);