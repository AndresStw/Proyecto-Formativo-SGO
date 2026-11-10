<?php

namespace App\Http\Controllers;

use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;
use Illuminate\Auth\Events\PasswordReset;

class AuthController extends Controller
{
    // 1# Endpoint: POST /api/register ---------------- Registrar 
    public function register(Request $request)
    {
        $validated = $request->validate([
            'nombre' => 'required|string|max:100',
            'email' => 'required|email|unique:Usuario,email',
            'telefono' => 'required|string|max:15|unique:Usuario,telefono',
            'password' => 'required|string|min:6',
            'direccion' => 'nullable|string|max:255'
        ]);

        $partesNombre = explode(' ', $validated['nombre'], 2);
        $primerNombre = $partesNombre[0];
        $primerApellido = $partesNombre[1] ?? '-';

        $usuario = Usuario::create([
            'primerNombre' => $primerNombre,
            'primerApellido' => $primerApellido,
            'email' => $validated['email'],
            'telefono' => $validated['telefono'],
            'direccion' => $validated['direccion'] ?? null,
            'password_hash' => Hash::make($validated['password']),
            'rol' => 'cliente',
            'estado' => true
        ]);

        $token = $usuario->createToken('auth_token')->plainTextToken;

        return response()->json([
            'accessToken' => $token,
            'user' => $usuario
        ], 201);
    }

    // 2# Endpoint: POST /api/login ------ Logeo de usuario
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required'
        ]);

        $usuario = Usuario::where('email', $request->email)->first();

        if (!$usuario || !Hash::check($request->password, $usuario->password_hash)) {
            throw ValidationException::withMessages([
                'email' => ['Las credenciales son incorrectas.'],
            ]);
        }

        $token = $usuario->createToken('auth_token')->plainTextToken;

        return response()->json([
            'accessToken' => $token,
            'user' => $usuario
        ]);
    }

    // 3# EndPoint: POST /api/logout ------ Cerrar sesión
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(['message' => 'Sesión cerrada exitosamente']);
    }

    // 4# EndPoint: PUT /api/me ------ Actualizar datos
    public function updateProfile(Request $request)
    {
        $usuario = $request->user();

        $validated = $request->validate([
            'primerNombre' => 'sometimes|string|max:45',
            'telefono' => 'sometimes|string|max:15|unique:Usuario,telefono,' . $usuario->idUsuario . ',idUsuario',
            'direccion' => 'sometimes|string|max:255',
        ]);

        $usuario->update($validated);

        return response()->json([
            'message' => 'Perfil actualizado correctamente',
            'user' => $usuario
        ]);
    }

    // 5# EndPoint: POST /api/forgot-password ------ Solicitar enlace
    public function forgotPassword(Request $request)
    {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        if ($status === Password::RESET_LINK_SENT) {
            return response()->json(['message' => 'Enlace de recuperación enviado (Revisa storage/logs/laravel.log)']);
        }

        return response()->json(['message' => 'No se pudo enviar el enlace. Verifica el correo.'], 400);
    }

    // 6# EndPoint: POST /api/reset-password ------ Cambiar contraseña
    public function resetPassword(Request $request)
    {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|min:6|confirmed',
        ]);

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function ($user, $password) {
                $user->forceFill([
                    'password_hash' => Hash::make($password)
                ])->setRememberToken(Str::random(60));

                $user->save();
                event(new PasswordReset($user));
            }
        );

        if ($status === Password::PASSWORD_RESET) {
            return response()->json(['message' => '¡Contraseña restablecida con éxito!']);
        }

        return response()->json(['message' => 'El token es inválido o ha expirado.'], 400);
    }
}