const passwordList = document.getElementById('passwords');
const passwordForm = document.getElementById('password-form');
const generateButton = document.getElementById('generate');
const siteInput = document.getElementById('site');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

// Retrieve saved passwords from localStorage
function loadPasswords() {
  const passwords = JSON.parse(localStorage.getItem('passwords')) || [];
  passwordList.innerHTML = '';
  passwords.forEach(({ site, username, password }) => {
    const li = document.createElement('li');
    li.textContent = `Site: ${site}, Username: ${username}, Password: ${password}`;
    passwordList.appendChild(li);
  });
}

// Save a new password
function savePassword(event) {
  event.preventDefault();
  const site = siteInput.value;
  const username = usernameInput.value;
  const password = passwordInput.value;

  if (site && username && password) {
    const passwords = JSON.parse(localStorage.getItem('passwords')) || [];
    passwords.push({ site, username, password });
    localStorage.setItem('passwords', JSON.stringify(passwords));
    loadPasswords();
    passwordForm.reset();
  }
}

// Generate a random password
function generatePassword() {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()';
  let password = '';
  for (let i = 0; i < 12; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    password += characters[randomIndex];
  }
  passwordInput.value = password;
}

// Event Listeners
passwordForm.addEventListener('submit', savePassword);
generateButton.addEventListener('click', generatePassword);

// Load passwords on startup
loadPasswords();