const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters = "01";
const matrix = letters.split("");

const font_size = 14;
const columns = canvas.width/font_size;

const drops = [];

for(let x = 0; x < columns; x++)
drops[x] = 1;

function draw(){

ctx.fillStyle = "rgba(2,6,23,0.05)";
ctx.fillRect(0,0,canvas.width,canvas.height);

ctx.fillStyle = "#22c55e";
ctx.font = font_size + "px monospace";

for(let i = 0; i < drops.length; i++){

const text = matrix[Math.floor(Math.random()*matrix.length)];

ctx.fillText(text,i*font_size,drops[i]*font_size);

if(drops[i]*font_size > canvas.height && Math.random() > 0.975)
drops[i] = 0;

drops[i]++;

}

}

setInterval(draw,35);