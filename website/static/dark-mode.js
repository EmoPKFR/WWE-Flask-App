// Function to toggle dark mode styles
function toggleDarkMode() {
	const darkModeEnabled = document.getElementById('darkModeToggle').checked;
  
	// Store dark mode preference in local storage
	localStorage.setItem('darkModeEnabled', darkModeEnabled);
  
	// Toggle dark mode class on the body
	if (darkModeEnabled) {
	  document.body.classList.add('dark-mode');
	} else {
	  document.body.classList.remove('dark-mode');
	}
  
	// Check if this is the home page
	if (document.body.getAttribute('home-page') === 'home') {
	  // Change the background image when dark mode is enabled or disabled
	  const backgroundImage = darkModeEnabled
		? 'url("static/images/logo_images/wwe_background.jpg")'
		: 'url("static/images/logo_images/home_light_mode.jpg")';
  
	  document.body.style.backgroundImage = backgroundImage;
	}
  
	// Toggle text color for <p>, <h>, and <div> elements
	const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, div');
	textElements.forEach(element => {
	  if (darkModeEnabled) {
		element.style.color = '#fff'; // White text color
	  } else {
		element.style.color = ''; // Restore default text color
	  }
	});
  }
  
  // Toggle dark mode on checkbox change
  document.getElementById('darkModeToggle').addEventListener('change', toggleDarkMode);
  
  // Initialize dark mode based on local storage preference
  const savedDarkModePreference = localStorage.getItem('darkModeEnabled');
  if (savedDarkModePreference === 'true') {
	// Ensure the dark mode toggle is checked
	document.getElementById('darkModeToggle').checked = true;
  }
  
  // Trigger initial toggle to apply dark mode to the current route
  toggleDarkMode();