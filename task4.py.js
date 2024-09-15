const choices = document.querySelectorAll('.choice');
const userScoreSpan = document.getElementById('user-score');
const computerScoreSpan = document.getElementById('computer-score');
const message = document.getElementById('message');
const resultImage = document.getElementById('result-image');

let userScore = 0;
let computerScore = 0;

choices.forEach(choice => {
  choice.addEventListener('click', (e) => {
    const userChoice = e.target.closest('button').id;
    const computerChoice = getComputerChoice();
    const winner = determineWinner(userChoice, computerChoice);

    displayResult(userChoice, computerChoice, winner);
  });
});

function getComputerChoice() {
  const choices = ['rock', 'paper', 'scissors'];
  const randomIndex = Math.floor(Math.random() * 3);
  return choices[randomIndex];
}

function determineWinner(user, computer) {
  if (user === computer) {
    return 'draw';
  }

  if ((user === 'rock' && computer === 'scissors') ||
      (user === 'paper' && computer === 'rock') ||
      (user === 'scissors' && computer === 'paper')) {
    return 'user';
  } else {
    return 'computer';
  }
}

function displayResult(userChoice, computerChoice, winner) {
  const images = {
    rock: 'images/rock.png',
    paper: 'images/paper.png',
    scissors: 'images/scissors.png'
  };

  let resultText;
  let resultImg;

  if (winner === 'user') {
    userScore++;
    resultText = `You Win! ${userChoice.charAt(0).toUpperCase() + userChoice.slice(1)} beats ${computerChoice}`;
    resultImg = images[userChoice];
  } else if (winner === 'computer') {
    computerScore++;
    resultText = `You Lose! ${computerChoice.charAt(0).toUpperCase() + computerChoice.slice(1)} beats ${userChoice}`;
    resultImg = images[computerChoice];
  } else {
    resultText = `It's a Draw! You both chose ${userChoice}`;
    resultImg = images[userChoice];
  }

  message.textContent = resultText;
  resultImage.src = resultImg;

  updateScore();
}

function updateScore() {
  userScoreSpan.textContent = userScore;
  computerScoreSpan.textContent = computerScore;
}