<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password', [AuthController::class, 'resetPassword']);

//Falta agregar el resto sincronia con el otro modulo 
// Route::post('/login', [AuthController::class, 'login']);
// Route::post('/login', [AuthController::class, 'login']);
// Route::post('/login', [AuthController::class, 'login']);

// Rutas protegidas Requieren Token

Route::middleware('auth:sanctum')->put('/me', [AuthController::class, 'updateProfile']);
Route::middleware('auth:sanctum')->post('/logout', [AuthController::class, 'logout']);
Route::middleware('auth:sanctum')->get('/me', function (Request $request) {
    return $request->user();
});

Route::middleware(['auth:sanctum', 'admin'])->group(function () {
    // Aqui van las rutas exclusivas del admin
});