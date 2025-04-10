// Combined scripts.js + place.js + review.js

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

  function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
  }

  function checkAuthentication(token) {
    const addReviewSection = document.getElementById('add-review');
    if (!token && addReviewSection) {
      addReviewSection.style.display = 'none';
    } else if (addReviewSection) {
      addReviewSection.style.display = 'block';
    }
  }

  function checkAuthOrRedirect() {
    const token = getTokenFromCookie();
    if (!token) {
      window.location.href = 'index.html';
    }
    return token;
  }

  // --- Token and user data ---
  const token = getTokenFromCookie();
  const loginLink = document.getElementById('login-link');

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'inline-block';
  }

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

  const logoutButton = document.getElementById('logout-button');
  if (logoutButton) {
    if (token) {
      logoutButton.style.display = 'inline-block';
      logoutButton.addEventListener('click', () => {
        document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.href = 'login.html';
      });
    } else {
      logoutButton.style.display = 'none';
    }
  }

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
          console.log('✅ Token stored:', document.cookie);
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

  // --- Dynamic logic based on page ---
  const placeId = getPlaceIdFromURL();

  if (document.getElementById('places-list')) {
    fetchPlaces(token);
  }

  if (document.getElementById('place-details')) {
    if (!placeId) {
      alert('Place ID not found in URL');
      return;
    }
    checkAuthentication(token);
    fetchPlaceDetails(token, placeId);
  }

  if (document.getElementById('review-form') && window.location.pathname.includes('add_review')) {
    const token = checkAuthOrRedirect();
    const placeId = getPlaceIdFromURL();

    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;

      try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          window.location.href = `place.html?id=${placeId}`;
        } else {
          alert('Failed to submit review');
        }
      } catch (error) {
        console.error(error);
        alert('Network error');
      }
    });
  }

  // --- Place List functions ---
  async function fetchPlaces(token) {
    try {
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await fetch('http://localhost:5000/api/v1/places/', {
        headers: headers
      });

      if (!response.ok) throw new Error('Failed to fetch places');
      const places = await response.json();
      console.log('📦 Places loaded:', places);
      displayPlaces(places);
      setupFiltering();
    } catch (error) {
      console.error('Error loading places:', error);
    }
  }

  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
      console.error('❌ places-list element not found in the DOM!');
      return;
    }

    placesList.innerHTML = '';

    const noMessage = document.getElementById('no-places-message');
    if (places.length === 0 && noMessage) {
      noMessage.style.display = 'block';
    } else if (noMessage) {
      noMessage.style.display = 'none';
    }

    places.forEach(place => {
      console.log("🖼️", place.title, "→", place.image_url);
      const article = document.createElement('article');
      article.className = 'place-card';
      article.dataset.price = place.price;
      article.innerHTML = `
        <img src="${place.image_url || 'https://via.placeholder.com/600x400?text=No+Image'}" 
             alt="${place.title}" class="place-image">
        <h3>${place.title}</h3>
        <p>$${place.price} per night</p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      `;
      placesList.appendChild(article);
    });
  }

  function setupFiltering() {
    const filterSelect = document.getElementById('price-filter');
    const prices = [10, 50, 100, 'All'];
    prices.forEach(price => {
      const option = document.createElement('option');
      option.value = price;
      option.textContent = price === 'All' ? 'All' : `$${price}`;
      filterSelect.appendChild(option);
    });

    filterSelect.addEventListener('change', () => {
      const selected = filterSelect.value;
      const maxPrice = selected === 'All' ? Infinity : parseFloat(selected);
      document.querySelectorAll('.place-card').forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = price <= maxPrice ? 'block' : 'none';
      });
    });
  }

  // --- Place Details and Reviews ---
  async function fetchPlaceDetails(token, placeId) {
    try {
      const res = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : undefined
        }
      });

      if (!res.ok) throw new Error('Failed to fetch place details');
      const place = await res.json();
      displayPlaceDetails(place);
      fetchReviews(placeId);
    } catch (err) {
      console.error(err);
    }
  }

  function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = `
      <h2>${place.name}</h2>
      <img src="${place.image_url || 'https://via.placeholder.com/600x400?text=No+Image'}" 
           alt="${place.name}" class="place-image">
      <p class="place-info">Price: $${place.price} per night</p>
      <p class="place-info">${place.description}</p>
      <p class="place-info">Location: ${place.location}</p>
      <p class="place-info">Amenities: ${(place.amenities || []).map(a => a.name).join(', ')}</p>
    `;
  }

  async function fetchReviews(placeId) {
    try {
      const res = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews/`);
      if (!res.ok) throw new Error('Failed to fetch reviews');
      const reviews = await res.json();
      const reviewsContainer = document.getElementById('reviews');

      reviews.forEach(review => {
        const div = document.createElement('div');
        div.className = 'review-card';
        div.innerHTML = `<p>"${review.text}"</p><p>- ${review.author || 'User'}, Rating: ⭐${review.rating}</p>`;
        reviewsContainer.appendChild(div);
      });
    } catch (err) {
      console.error(err);
    }
  }
});
