// src/services/Auth.js

const API_URL = "http://localhost:3000";
const TOKEN_KEY = "token";
const USER_KEY = "user";

// Obtener token
export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

// Obtener usuario guardado
export function getUser() {
  try {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  } catch {
    clearAuth();
    return null;
  }
}

// Comprobar expiracion del JWT token
function isExpired(token) {
  try {
    const payload = JSON.parse(
      atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))
    );
    return typeof payload.exp === "number" && payload.exp * 1000 <= Date.now();
  } catch {
    return false;
  }
}

// Comprobar autenticacion
export function isAuthenticated() {
  const token = getToken();
  if (!token) return false;
  if (isExpired(token)) {
    clearAuth();
    return false;
  }
  return true;
}

// Guardado de sesion
export function saveAuth(data, fallbackEmail = "") {
  const token = data?.accessToken || data?.token;
  if (!token) throw new Error("El servidor no devolvió un token de acceso");

  localStorage.setItem(TOKEN_KEY, token);

  // Guarda el objeto usuario si viene en la respuesta, de lo contrario guarda la estructura básica
  const userInfo = data.user || { email: fallbackEmail };
  localStorage.setItem(USER_KEY, JSON.stringify(userInfo));

  if (fallbackEmail) localStorage.setItem("userEmail", fallbackEmail);
  return token;
}

// Limpieza de sesion (Cerrar sesión)
export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem("userEmail");
}

// Fetch autenticado con headers y Bearer Token
export async function authFetch(path, options = {}) {
  const token = getToken();
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (response.status === 401) {
    clearAuth();
    throw new Error("Sesión expirada. Inicia sesión nuevamente.");
  }
  return response;
}

// Iniciar sesión contra el endpoint /login de json-server-auth
export async function login(email, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.message || "Credenciales incorrectas");

  saveAuth(data, email);
  return data;
}

// Registrar usuario contra el endpoint /register
export async function register(userData) {
  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok)
    throw new Error(data.message || "No fue posible crear la cuenta");

  // NO guardamos la sesión automáticamente para requerir inicio de sesión manual
  return data;
}