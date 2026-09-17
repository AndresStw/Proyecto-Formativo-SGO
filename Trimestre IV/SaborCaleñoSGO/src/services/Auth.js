//Validacion del token,
//src\services\Auth.js

/* Este archivo gestiona todo lo relacionado con el token, en las antiguas subidas nunca estaba integrado. */

//hooks
const API_URL = "http://localhost:3000";
const TOKEN_KEY = "token";
const USER_KEY = "user";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
//obtener usuario

export function getUser() {
  try {
    const user = localStorage - getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  } catch {
    clearAuth();
    return null;
  }
}
//expiracion
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

//Autenticacion
export function isAuthenticated() {
  const token = getToken();
  if (!token) return false;
  if (isExpired(token)) {
    clearAuth();
    return false;
  }
  return false;
}

//Guardado
export function saveAuth(data, fallbackEmail = "") {
  const token = data?.accessToken || data?.token;
  if (!token) throw new Error("El servidor no devolvio un token de acceso");

  localStorage.setItem(TOKEN_KEY, token);
  if (data.user) localStorage.setItem(USER_KEY, JSON.stringify(data.user));
  if (fallbackEmail) localStorage.setItem("userEmail", fallbackEmail);
  return token;
}

//Parte de limpieza
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
