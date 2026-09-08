#  Proyecto — Guía de instalación y uso para el equipo

##  Requisitos previos

- Tener [Node.js](https://nodejs.org/) instalado.
- Clonar el repositorio y ubicarte en la carpeta del proyecto.

##  Instalación de dependencias

Todas las dependencias del proyecto ya están definidas en `package.json`. Para instalarlas:

```bash
npm install
```

### Dependencias principales del proyecto

```
@fortawesome/fontawesome-free@7.3.1
@types/react-dom@19.2.5
@types/react@19.2.18
@vitejs/plugin-react@6.1.0
bootstrap@5.3.8
json-server-auth@2.1.0
json-server@0.17.4
oxlint@1.80.0
react-dom@19.2.8
react-router-dom@7.18.2
react@19.2.8
vite@8.2.2
```

### Verificar que ya estén instaladas

```bash
npm list --depth=0
```

## ▶ Ejecutar el proyecto

Se necesitan dos terminales abiertas en paralelo:

```bash
npm run server   # Levanta json-server (API con autenticación)
npm run dev      # Levanta el frontend con Vite
```

## 🔐 Probar la API con PowerShell

### 1. Registrar usuario

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/register" -ContentType "application/json" -Body '{"email":"usuario@test.com","password":"123456"}'
```

### 2. Iniciar sesión

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/login" -ContentType "application/json" -Body '{"email":"usuario@test.com","password":"123456"}'
```

Este paso devuelve un `token` que se usa en las siguientes peticiones protegidas.

### 3. Ver usuarios (requiere token)

```powershell
$token = "TU_TOKEN_AQUI"
Invoke-RestMethod -Method Get -Uri "http://localhost:3000/users" -Headers @{Authorization="Bearer $token"}
```

### 4. Ver productos (requiere token)

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:3000/productos" -Headers @{Authorization="Bearer $token"}
```

> ⚠️ **Nunca subas un token real al repositorio.** Usa siempre un placeholder como `TU_TOKEN_AQUI` en la documentación y en los ejemplos.

## ➕ Agregar datos desde la terminal

### Agregar un producto

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/productos" `
  -ContentType "application/json" `
  -Body '{
    "nombre": "Sancocho de Pescado",
    "descripcion": "Delicioso sancocho con pescado fresco y verduras.",
    "precio": 25000,
    "categoria": "platos"
  }'
```

### Agregar un usuario (registro)

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/register" `
  -ContentType "application/json" `
  -Body '{
    "email": "nuevo@usuario.com",
    "password": "123456"
  }'
```

### Agregar un pedido

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:3000/pedidos" `
  -ContentType "application/json" `
  -Body '{
    "usuario": "cliente@saborcaleno.com",
    "productos": [
      { "id": 1, "cantidad": 2 },
      { "id": 2, "cantidad": 1 }
    ],
    "total": 40000,
    "estado": "pendiente"
  }'
```

### Otro ejemplo de producto

```powershell
$body = '{
  "nombre": "Arroz Atollado",
  "descripcion": "Arroz con carnes y verduras típico del Valle",
  "precio": 28000,
  "categoria": "platos"
}'

Invoke-RestMethod -Method Post -Uri "http://localhost:3000/productos" -ContentType "application/json" -Body $body
```

### Verificar productos existentes

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:3000/productos"
```

## 🧩 Dependencias adicionales (opcional)

Si en algún momento necesitas agregar una dependencia que no está en el `package.json` (por ejemplo `axios`), instálala con:

```bash
npm install axios
```

## 🌐 Ejecutar el proyecto desde otra máquina en la red local

1. Consulta tu IP local:

```bash
ipconfig
```

2. Comparte esa IP con el compañero que se vaya a conectar (asegúrense de estar en la misma red).
