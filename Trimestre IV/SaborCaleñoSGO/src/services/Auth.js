// src/services/Auth.js

/*
  Gestiona todo lo relacionado con autenticaciin (token, usuario, login, registro).
  Funciones:
    - 1.getToken(): Obtiene el token del localStorage
    - 2.getUser(): Obtiene el usuario del localStorage
    - 3.isAuthenticated(): Verifica si el usuario esta autenticado y el token no expiro
    - 4.saveAuth(): Guarda token y usuario en localStorage
    - 5.clearAuth(): Limpia todos los datos de autenticación
    - 6.authFetch(): Hace peticiones con el token en el header
    - 7.login(): Inicia sesion
    - 8.register(): Registra un nuevo usuario
*/

//Hooks
const API_URL = "http://localhost:3000";
const TOKEN_KEY = "token";
const USER_KEY = "user";

//#region Funciones

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function getUser() {
  try {
    const user = localStorage.getItem(USER_KEY); //Tenia una letrica (-) "Corregido"
    return user ? JSON.parse(user) : null;
  } catch {
    clearAuth();
    return null;
  }
}

function isExpired(token) {
  try {
    const payload = JSON.parse(
      atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")),
    );
    return typeof payload.exp === "number" && payload.exp * 1000 <= Date.now();
  } catch {
    return false;
  }
}

export function isAuthenticated() {
  const token = getToken();
  if (!token) return false;
  if (isExpired(token)) {
    clearAuth();
    return false;
  }
  return true; // Error estaba en false "Corregido"
}

export function saveAuth(data, fallbackEmail = "") {
  const token = data?.accessToken || data?.token;
  if (!token) throw new Error("El servidor no devolvio un token de acceso");

  localStorage.setItem(TOKEN_KEY, token);
  if (data.user) localStorage.setItem(USER_KEY, JSON.stringify(data.user));
  if (fallbackEmail) localStorage.setItem("userEmail", fallbackEmail);
  return token;
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem("userEmail");
}

export async function authFetch(path, options = {}) {
  const token = getToken();
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (response.status === 401) {
    clearAuth();
    throw new Error("Sesion expirada. Inicia sesion nuevamente.");
  }
  return response;
}

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

export async function register(userData) {
  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok)
    throw new Error(data.message || "No fue posible crear la cuenta");

  if (data.accessToken || data.token) saveAuth(data, userData.email);
  return data;
}

//#endregion
