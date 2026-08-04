// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];

function setCellClasses(inp, { isPrefilled = false, isIncorrect = false, isInvalid = false } = {}) {
  inp.className = 'sudoku-cell';
  if (isPrefilled) {
    inp.className += ' prefilled';
  }
  if (isIncorrect) {
    inp.className += ' incorrect';
  }
  if (isInvalid) {
    inp.className += ' invalid';
  }
}

function getBoardFromInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return { inputs, board };
}

function hasConflictingValue(board, row, col, value) {
  for (let j = 0; j < SIZE; j++) {
    if (j !== col && board[row][j] === value) {
      return true;
    }
  }
  for (let i = 0; i < SIZE; i++) {
    if (i !== row && board[i][col] === value) {
      return true;
    }
  }
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      const r = boxRow + i;
      const c = boxCol + j;
      if ((r !== row || c !== col) && board[r][c] === value) {
        return true;
      }
    }
  }
  return false;
}

function updateLiveValidation() {
  const { inputs, board } = getBoardFromInputs();
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) {
      setCellClasses(inp, { isPrefilled: true });
      continue;
    }
    const row = Number(inp.dataset.row);
    const col = Number(inp.dataset.col);
    const value = inp.value ? parseInt(inp.value, 10) : 0;
    const isInvalid = value !== 0 && hasConflictingValue(board, row, col, value);
    setCellClasses(inp, { isInvalid });
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        updateLiveValidation();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        setCellClasses(inp, { isPrefilled: true });
      } else {
        inp.value = '';
        inp.disabled = false;
        setCellClasses(inp);
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty-select').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const { inputs, board } = getBoardFromInputs();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) {
      setCellClasses(inp, { isPrefilled: true });
      continue;
    }
    setCellClasses(inp, { isIncorrect: incorrect.has(idx) });
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function showHint() {
  const { inputs, board } = getBoardFromInputs();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const idx = data.row * SIZE + data.col;
  const inp = inputs[idx];
  if (!inp || inp.disabled) {
    msg.style.color = '#d32f2f';
    msg.innerText = 'No available hint.';
    return;
  }
  inp.value = data.value;
  inp.disabled = true;
  setCellClasses(inp, { isPrefilled: true });
  msg.style.color = '#1976d2';
  msg.innerText = 'Hint applied.';
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-button').addEventListener('click', showHint);
  // initialize
  newGame();
});