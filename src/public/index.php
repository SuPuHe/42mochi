<?php
// src/public/index.php
// This is the front controller. All requests are routed here.
require_once __DIR__ . '/../core/Autoload.php';
require_once __DIR__ . '/../core/Router.php';
// require_once __DIR__ . '/../App/controllers/HomeController.php';

// use core\Router;
// Instantiate the home controller and call a method
// $homeController = new HomeController();
// $homeController->index();

session_start();
$router = new Router;

$uri = $_SERVER['REQUEST_URI'];

// Define routes that do NOT require auth (like AuthController routes for login & callback)
$publicRoutes = [
    '/auth',          // login redirect to OAuth
    '/auth/callback', // OAuth callback URL
];

// Normalize URI for matching (remove query strings)
$uriPath = parse_url($uri, PHP_URL_PATH);

// If user is NOT logged in and tries to access protected route => redirect to /auth
if (!isset($_SESSION['access_token']) && !in_array(strtolower($uriPath), $publicRoutes)) {
    // Save the originally requested URL to redirect back after login
    $_SESSION['end_url'] = $uri;
    
    // Redirect to your AuthController index to start OAuth flow
    header('Location: /auth');
    exit;
}
define('WHERE_AM_I', $router->where_am_i($uri));
$router->dispatch($uri);