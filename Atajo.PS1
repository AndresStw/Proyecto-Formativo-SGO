# Detener la ejecución inmediatamente si ocurre un error en un comando de PowerShell
$ErrorActionPreference = "Stop"

# Función auxiliar para verificar que los ejecutables externos (python, pip, alembic, uvicorn) no fallen
function Ejecutar-Paso {
    param (
        [string]$Mensaje,
        [scriptblock]$Comando
    )
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host ">>> $Mensaje" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    
    & $Comando
    
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        Write-Host "`n[ERROR] Falló el paso: '$Mensaje' (Código de salida: $LASTEXITCODE)" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# 1. Crear el entorno virtual si aún no existe
if (-not (Test-Path ".\.venv")) {
    Ejecutar-Paso "Creando entorno virtual (.venv)..." { python -m venv .venv }
} else {
    Write-Host "`n[INFO] El entorno virtual .venv ya existe. Omitiendo creación..." -ForegroundColor Yellow
}

# 2. Activar el entorno virtual en la sesión actual
Write-Host "`n>>> Activando entorno virtual..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
Ejecutar-Paso "Instalando dependencias desde requirements.txt..." { pip install -r .\requirements.txt }

# 4. Ejecutar migraciones y verificar estado de Alembic
Ejecutar-Paso "Aplicando migraciones (alembic upgrade head)..." { alembic upgrade head }
Ejecutar-Paso "Verificando revisión actual (alembic current)..." { alembic current }
Ejecutar-Paso "Mostrando historial de migraciones (alembic history)..." { alembic history }

# 5. Ejecutar scripts de inicialización (seeds y super admin)
# Nota: Verifica si tu archivo se llama create_super_admin.py o es un módulo (-m)
Ejecutar-Paso "Creando Super Admin..." { python creat   e_super_admin.py }
Ejecutar-Paso "Ejecutando seed_pedidos..." { python -m scripts.seed_pedidos }
Ejecutar-Paso "Ejecutando seed_datos_pedidos..." { python -m scripts.seed_datos_pedidos }

# 6. Levantar el servidor de desarrollo
Write-Host "`n==========================================" -ForegroundColor Green
Write-Host ">>> Todo listo. Iniciando servidor Uvicorn..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Revisa si tu archivo principal es app/main.py (sería app.main:app) o app.py
uvicorn app.main:app --reload