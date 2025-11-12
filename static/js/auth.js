// Auth state management
let currentUser = null;

// Check authentication status on page load
document.addEventListener('DOMContentLoaded', async function() {
    await checkAuthStatus();
    updateNavigation();
});

// Check if user is logged in
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/check-session');
        const data = await response.json();
        
        if (data.logged_in) {
            currentUser = {
                id: data.user_id,
                username: data.username,
                role: data.role
            };
            
            // Also check localStorage for token
            const token = localStorage.getItem('access_token');
            if (token) {
                currentUser.token = token;
            }
        } else {
            currentUser = null;
            // Clear localStorage if session expired
            localStorage.removeItem('access_token');
            localStorage.removeItem('username');
            localStorage.removeItem('role');
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
        currentUser = null;
    }
}

// Update navigation based on auth status
function updateNavigation() {
    const navbarNav = document.querySelector('#navbarNav .navbar-nav');
    if (!navbarNav) return;
    
    // Remove existing auth items
    const existingAuthItems = navbarNav.querySelectorAll('.auth-nav-item');
    existingAuthItems.forEach(item => item.remove());
    
    if (currentUser) {
        // User is logged in
        const userDropdown = document.createElement('li');
        userDropdown.className = 'nav-item dropdown auth-nav-item';
        userDropdown.innerHTML = `
            <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                <i class="fas fa-user"></i> ${currentUser.username}
            </a>
            <ul class="dropdown-menu">
                ${currentUser.role === 'admin' ? `
                    <li><a class="dropdown-item" href="/admin/dashboard">
                        <i class="fas fa-tachometer-alt"></i> Admin Panel
                    </a></li>
                ` : ''}
                <li><a class="dropdown-item" href="#" onclick="handleLogout()">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </a></li>
            </ul>
        `;
        navbarNav.appendChild(userDropdown);
    } else {
        // User is not logged in
        const loginItem = document.createElement('li');
        loginItem.className = 'nav-item auth-nav-item';
        loginItem.innerHTML = `
            <a class="nav-link" href="/login">
                <i class="fas fa-sign-in-alt"></i> Login
            </a>
        `;
        navbarNav.appendChild(loginItem);
    }
}

// Handle logout
async function handleLogout() {
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST'
        });
        
        if (response.ok) {
            // Clear localStorage
            localStorage.removeItem('access_token');
            localStorage.removeItem('username');
            localStorage.removeItem('role');
            
            // Clear current user
            currentUser = null;
            
            // Show success message
            alert('Logged out successfully!');
            
            // Redirect to home
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('Error logging out. Please try again.');
    }
}

// Helper function to get auth headers for API requests
function getAuthHeaders() {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (currentUser && currentUser.token) {
        headers['Authorization'] = `Bearer ${currentUser.token}`;
    }
    
    return headers;
}

// Check if user is admin
function isAdmin() {
    return currentUser && currentUser.role === 'admin';
}

// Check if user is logged in
function isLoggedIn() {
    return currentUser !== null;
}

// Require login (redirect to login page if not logged in)
function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Require admin (redirect to home if not admin)
function requireAdmin() {
    if (!isAdmin()) {
        alert('Admin access required');
        window.location.href = '/';
        return false;
    }
    return true;
}