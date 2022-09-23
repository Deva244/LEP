const countdown = document.getElementById('countdown-box')
const examDuration = document.getElementById('exam-duration')
console.log(examDuration.textContent)

const examDate = Date.parse(examDuration.textContent)
console.log(examDate)