document.addEventListener('DOMContentLoaded', () => {
  // --- Bloc 1 : login ---
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevent page reload

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
          window.location.href = 'index.html';
        } else {
          const errorData = await response.json();
          alert('Login failed: ' + (errorData.message || response.statusText));
        }
      } catch (error) {
        alert('Network error: ' + error.message);
      }
    });
  }

  // --- Bloc 2 : display first name from cookie ---
  const token = getTokenFromCookie();

  if (token) {
    const userData = parseJwt(token);
    console.log('👤 User connected :', userData);

    const welcomeDiv = document.getElementById('welcome');
    console.log('🧪 welcomeDiv found:', welcomeDiv);

    if (welcomeDiv && userData && userData.sub && userData.sub.first_name) {
      welcomeDiv.textContent = `Welcome, ${userData.sub.first_name} !`;
    } else if (welcomeDiv && userData.sub && userData.sub.email) {
      welcomeDiv.textContent = `Welcome, ${userData.sub.email} !`;
    } else {
      welcomeDiv.textContent = `Welcome back!`;
    }
  }
});

// --- Useful functions ---
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) =>
      '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));

    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

function getTokenFromCookie() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'token') {
      return value;
    }
  }
  return null;
}
