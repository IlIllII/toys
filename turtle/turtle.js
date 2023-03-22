let canvas = document.getElementById('my-canvas');
let context = canvas.getContext('2d');
context.lineWidth = 1;
let angle = 3 * Math.PI / 2;
let sleepDuration = 100;
let color = "black"
let x = canvas.width / 2;
let y = canvas.height / 2;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function line(x1, y1, x2, y2, color) {
    await sleep(sleepDuration);
    context.strokeStyle = color;
    context.beginPath();
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.stroke();
    context.closePath();
    return;
}

function dot(centerX, centerY, radius, color) {
    context.beginPath();
    context.fillStyle = color;
    context.arc(centerX, centerY, radius, 0, 2 * Math.PI, true);
    context.fill();
};

function forward(distance) {
    let x2 = x + distance * Math.cos(angle);
    let y2 = y + distance * Math.sin(angle);
    line(x, y, x2, y2, color);
    x = x2;
    y = y2;
}

function turn(degrees) {
    angle += degrees * Math.PI / 180;
    angle = angle % (2 * Math.PI);
}

function turnRight(degrees) {
    turn(degrees);
}

function turnLeft(degrees) {
    turn(-degrees);
}