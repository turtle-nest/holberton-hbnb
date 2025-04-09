document.addEventListener('DOMContentLoaded', () => {
  // --- Utility functions ---
  function parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
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

  // --- Token and user data ---
  const token = getTokenFromCookie();

  // --- Display user's first name if connected ---
  const welcomeDiv = document.getElementById('welcome');
  if (token) {
    const userData = parseJwt(token);
    console.log('👤 User connected:', userData);

    if (welcomeDiv && userData && userData.sub && userData.sub.first_name) {
      welcomeDiv.textContent = `Welcome, ${userData.sub.first_name}!`;
    } else if (welcomeDiv && userData.sub && userData.sub.email) {
      welcomeDiv.textContent = `Welcome, ${userData.sub.email}!`;
    } else if (welcomeDiv) {
      welcomeDiv.textContent = `Welcome back!`;
    }
  }

  // --- Logout button logic ---
  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
    if (token) {
      logoutButton.style.display = 'inline-block';
      logoutButton.addEventListener('click', () => {
        // Clear the token cookie
        document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        // Redirect to login page
        window.location.href = 'login.html';
      });
    } else {
      logoutButton.style.display = 'none';
    }
  }

  // --- Login form submission ---
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

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
          // Store the token in a cookie
          document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
          console.log('✅ Token stored:', document.cookie);
          // Redirect to index
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
});
