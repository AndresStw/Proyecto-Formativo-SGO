# 📚 Proyecto Formativo SGO - Rama: Prefacht (Staging/Pruebas)

## Descripción General

Este README documenta la rama **`Prefacht`** del proyecto formativo **Proyecto-Formativo-SGO**, que funciona como rama de **pruebas y validación** antes de integrar cambios a la rama principal (`main`). Esta rama contiene todas las mejoras, desarrollos y correcciones que han sido probadas y están listas para producción.

**Rama:** `Prefacht` (Staging/Pruebas)  
**Repositorio:** [AndresStw/Proyecto-Formativo-SGO](https://github.com/AndresStw/Proyecto-Formativo-SGO)  
**Última Actualización:** 20 de Agosto de 2026  
**Estado:** ✅ Activa - Rama de Pruebas en Producción

---

## 📋 Propósito de la Rama Prefacht

La rama **Prefacht** actúa como entorno de **staging/pruebas** con los siguientes objetivos:

### 🎯 Objetivos Principales

1. **Validar Cambios** - Probar todas las características antes de integrarlas a `main`
2. **Control de Calidad** - Asegurar estabilidad y funcionalidad del sistema
3. **Integración Continua** - Consolidar aportes de múltiples desarrolladores
4. **Documentación Actualizada** - Mantener registros detallados de versiones
5. **Preparar Producción** - Preparar código listo para deployment

### 🔄 Flujo de Trabajo

```
feature/* branches
    ↓
[Desarrollo Individual]
    ↓
Pull Request → Prefacht
    ↓
[Pruebas y Validación]
    ↓
✅ Aprobado → main
    ↓
📦 Producción
```

---

## 📊 Últimas Actualizaciones (Agosto 2026)

| Fecha | Responsable | Commit | Cambio |
|-------|-------------|--------|--------|
| 20/08/2026 | AndresStw | a149d55 | Revise README for project overview and organization |
| 20/08/2026 | AndresStw | 6541308 | Add useful queries for Sabor Caleño SGO |
| 20/08/2026 | AndresStw | 8bddc1c | feat: initialize React project with Vite, add global styles, and include SVG assets |
| 04/08/2026 | AndresStw | f39c373 | Add README for feature/customer-experience-v4 |
| 04/08/2026 | AndresStw | 999823f | Delete README_FEATURE_BRANCH.md |

---

## 📁 Estructura del Proyecto

```
Última Actualización: 20 de Agosto de 2026 - Estructura Completa

└── 📁Proyecto-Formativo-SGO
    └── 📁.idea (IDE configuration)
        ├── .gitignore
        ├── misc.xml
        ├── modules.xml
        ├── vcs.xml
        └── workspace.xml
    
    └── 📁Trimestre I (Requisitos & Análisis)
        ├── 📁BPMN
        │   └── BPMN.pdf
        ├── 📁featurecustomer-experience-v4
        │   ├── Links formularios.docx
        │   ├── Modulo 4 app movil y web_Kevin Landazuri.pdf
        │   ├── Wireframe de sitio web.json
        │   └── Recolección de datos (Formularios de Google)
        ├── 📁Formato De Costos
        ├── 📁Formato SRS
        ├── 📁Proyecto versiones
        ├── 📁Recoleccion de datos
        └── 📁RF y RNF
    
    └── 📁Trimestre II (Análisis & Desarrollo)
        ├── cuadro cotizaciones.xlsx
        ├── FORMATO DE INFORME DE COSTOS Y ANÁLISIS DE PROVEEDORES.docx
        ├── GC-F-004FormatoPlantillaPresentacionPowerPointV10.pptx.pdf
        └── Sabor Caleño proyecto Fase II .pdf
    
    └── 📁Trimestre III (Prototipo - HTML/CSS/JS)
        └── 📁Prototipo
            ├── 📁Admin (Páginas de administración)
            ├── 📁Assets (CSS, Imágenes, JavaScript)
            ├── 📁Pages (Páginas de cliente)
            ├── Estructura.md
            └── index.html
        ├── Diagramas de procesos
        ├── MER (Modelo Entidad-Relación)
        └── Normalizacion.xlsx
    
    └── 📁Trimestre IV (Backend & React)
        ├── 📁DB SQL
        │   ├── README.md
        │   ├── schema.sql (Definición de tablas)
        │   ├── seed.sql (Datos de ejemplo)
        │   └── SQL-README.md
        ├── 📁SaborCaleñoSGO (Proyecto React + Vite)
        │   ├── 📁public
        │   ├── 📁src
        │   │   ├── 📁assets
        │   │   ├── App.jsx
        │   │   ├── index.css
        │   │   └── main.jsx
        │   ├── package.json
        │   ├── vite.config.js
        │   └── README.md
        └── schema.sql (Base de datos)
    
    └── README.md (Este archivo)
```

---

## 🎯 Contenido por Trimestres

### Trimestre I: Requisitos y Planificación
- **RF/RNF** - Requisitos Funcionales y No Funcionales
- **BPMN v1** - Diagramas de procesos de negocio
- **Presentaciones v1-v3** - Evolución del proyecto
- **Formato SRS** - Especificación de requisitos
- **Análisis de Proveedores**

### Trimestre II: Análisis y Presupuestos
- **Cotizaciones** - Análisis de costos (Excel/Word)
- **Formato de Costos** - Estructura económica
- **Presentación Fase II** - Avances del proyecto
- **Documentación Actualizada**

### Trimestre III: Prototipo (HTML/CSS/JS)
- **Páginas Web** - Interfaz cliente
- **Panel Administrativo** - Gestión de sistema
- **Assets** - Estilos, imágenes y validaciones
- **Diagramas ER/MER** - Modelo de datos
- **Normalización** - Análisis de base de datos

### Trimestre IV: Backend y Frontend Moderno ⭐ NUEVO
- **Base de Datos SQL** - Schema y datos de prueba
- **Proyecto React + Vite** - Frontend moderno
- **Configuración de Desarrollo** - Herramientas optimizadas
- **Queries SQL** - Consultas para validación

---

## 🔑 Archivos Clave

### Configuración y Entorno

| Archivo | Descripción | Ubicación |
|---------|-------------|-----------|
| `.gitignore` | Archivos ignorados por Git | Raíz |
| `package.json` | Dependencias del proyecto React | Trimestre IV/SaborCaleñoSGO |
| `vite.config.js` | Configuración de Vite | Trimestre IV/SaborCaleñoSGO |

### Base de Datos

| Archivo | Descripción | Ubicación |
|---------|-------------|-----------|
| `schema.sql` | Definición de tablas y relaciones | Trimestre IV/DB SQL |
| `seed.sql` | Datos de ejemplo para pruebas | Trimestre IV/DB SQL |
| `queries.sql` | Consultas útiles para validación | Trimestre IV/DB SQL |

### Documentación Estratégica

| Archivo | Descripción |
|---------|-------------|
| Formato SRS | Especificación de Requisitos de Software |
| Requisitos (RF/RNF) | Requisitos Funcionales y No Funcionales |
| BPMN | Diagramas de procesos de negocio |

### Frontend y UX

| Archivo | Descripción |
|---------|-------------|
| Wireframes | Diseño de interfaz de usuario |
| Prototipo HTML/CSS/JS | Versión inicial de la aplicación |
| React App (Trimestre IV) | Aplicación frontend moderna |

---

## 🚀 Cómo Trabajar con Esta Rama

### Clonar la Rama
```bash
git clone -b Prefacht https://github.com/AndresStw/Proyecto-Formativo-SGO.git
cd Proyecto-Formativo-SGO
```

### Instalar Dependencias (Trimestre IV - React)
```bash
cd "Trimestre IV/SaborCaleñoSGO"
npm install
npm run dev
```

### Configurar Base de Datos
```bash
cd "../DB SQL"
# Importar schema.sql en tu gestor de bases de datos (PostgreSQL)
psql -U usuario -d nombre_bd -f schema.sql
psql -U usuario -d nombre_bd -f seed.sql
```

### Navegar por el Contenido
```bash
# Documentación Trimestre I
cd "Trimestre I"
ls -la

# Prototipo Trimestre III
cd "../Trimestre III/Prototipo"
open index.html

# Backend Trimestre IV
cd "../../Trimestre IV/DB SQL"
cat schema.sql
```

---

## ✨ Características Implementadas

### ✅ Completado
- [x] Documentación completa de requisitos (RF/RNF)
- [x] Diagramas BPMN de procesos
- [x] Especificación SRS detallada
- [x] Análisis de costos y proveedores
- [x] Prototipo funcional (HTML/CSS/JS)
- [x] Modelo de datos (ER/MER)
- [x] Base de datos SQL con schema
- [x] Datos de ejemplo (seed data)
- [x] Proyecto React con Vite
- [x] Estilos globales y responsive
- [x] Queries SQL para validación

### 🔄 En Desarrollo/Pruebas
- [ ] Componentes React completos
- [ ] API REST backend
- [ ] Autenticación y autorización
- [ ] Integración frontend-backend
- [ ] Tests unitarios e integración
- [ ] Documentación API

### 📋 Pendiente para Producción
- [ ] Deployment en servidor
- [ ] Configuración de CI/CD
- [ ] Monitoreo y logging
- [ ] Optimización de performance
- [ ] Seguridad (HTTPS, CORS, validación)

---

## 👥 Contribuyentes

Este proyecto es resultado del trabajo colaborativo de:

- **AndresStw** - Coordinación general, actualizaciones principales y React setup
- **davidvillanuevapotosi** - Cotizaciones y análisis presupuestarios
- **brandonxrojas** - Diagramas BPMN y análisis de procesos
- **sclavijo291-dot** - Documentación y especificaciones SRS
- **Kevin Landazuri** - Desarrollo de módulos de aplicación móvil/web

---

## 🔐 Checklist Antes de Merge a Main

Antes de hacer merge de `Prefacht` a `main`, validar:

- [ ] Todos los tests pasan ✓
- [ ] Documentación actualizada
- [ ] No hay conflictos de merge
- [ ] Código revisado por mínimo 2 personas
- [ ] Base de datos migra correctamente
- [ ] Frontend renderiza sin errores
- [ ] Configuración de variables de entorno correcta
- [ ] Performance aceptable
- [ ] Seguridad validada

---

## 📝 Control de Versiones

| Versión | Fecha | Cambios Principales |
|---------|-------|-------------------|
| 1.3 | 20/08/2026 | React + Vite, Queries SQL, README actualizado |
| 1.2 | 04/08/2026 | Feature customer-experience-v4 consolidada |
| 1.1 | 06/04/2026 | BPMN v3, reorganización estructura |
| 1.0 | 04/04/2026 | Trimestres I y II documentados |

---

## 📖 Documentación Complementaria

- **[Trimestre I/Formato SRS](Trimestre%20I/Formato%20SRS/FormatoSRS%20Proyecto%20formativo.docx)** - Especificación técnica completa
- **[Trimestre III/Prototipo](Trimestre%20III/Prototipo/Estructura.md)** - Guía de estructura
- **[Trimestre IV/DB SQL/README.md](Trimestre%20IV/DB%20SQL/README.md)** - Documentación de base de datos
- **[Trimestre IV/SaborCaleñoSGO/README.md](Trimestre%20IV/SaborCaleñoSGO/README.md)** - Setup del proyecto React

---

## ⚙️ Requisitos para Trabajar con Esta Rama

### Software Requerido
- Git 2.0 o superior
- Node.js 16+ (para Trimestre IV)
- npm o yarn
- PostgreSQL 12+ (para base de datos)
- Visual Studio Code (recomendado)

### Herramientas Opcionales
- Postman (pruebas de API)
- DBeaver (gestor de base de datos)
- Draw.io (editar diagramas BPMN)
- Figma (diseño UI/UX)

### Dependencias del Proyecto
```bash
# Ver en Trimestre IV/SaborCaleñoSGO/package.json
- react 18.x
- vite 4.x
- (más por definir)
```

---

## 🔄 Ciclo de Vida: Prefacht

```
Semana 1-2: Desarrollo en feature/*
    ↓
Semana 3: PR a Prefacht
    ↓
Semana 4: Testing & QA
    ↓
Semana 5: Bugfixes y ajustes
    ↓
Semana 6: Code Review & Aprobación
    ↓
Semana 7: Merge a main
    ↓
Semana 8: Deploy a Producción
```

---

## 🚨 Notas Importantes

### ✋ NO Hacer en Prefacht
- ❌ Modificar datos de producción
- ❌ Hacer push directo sin review
- ❌ Ignorar tests fallidos
- ❌ Incluir credenciales o secrets
- ❌ Cambios directos a main

### ✅ SÍ Hacer en Prefacht
- ✅ Crear PRs desde feature branches
- ✅ Ejecutar tests locales primero
- ✅ Documentar cambios
- ✅ Pedir review a mínimo 2 personas
- ✅ Usar commits descriptivos

---

## 📞 Proceso de Soporte

Para problemas, preguntas o sugerencias en esta rama:

1. **Revisar documentación** en carpetas correspondientes
2. **Buscar en issues existentes** - [GitHub Issues](https://github.com/AndresStw/Proyecto-Formativo-SGO/issues)
3. **Crear nuevo issue** si no existe (con etiqueta `prefacht` o `bug`/`enhancement`)
4. **Contactar contributors** vía GitHub
5. **Escalar a main project lead** si es crítico

---

## 🎓 Contexto Académico

**Tipo:** Proyecto Formativo  
**Institución:** Programa de Formación Profesional  
**Período:** Enero 2026 - Diciembre 2026  
**Duración:** 4 Trimestres  
**Producto:** Sistema de Gestión Organizacional (SGO) - Sabor Caleño  

Este proyecto fue desarrollado como ejercicio práctico de ingeniería de software, cubriendo desde requisitos hasta implementación full-stack.

---

## 📊 Estadísticas de la Rama

- **Commits en Prefacht:** 40+
- **Archivos:** 100+
- **Tamaño:** ~500MB (incluyendo assets)
- **Últimas pruebas:** ✅ Exitosas (20/08/2026)
- **Cobertura de tests:** En desarrollo

---

## 🔐 Seguridad y Privacidad

- ✅ Repositorio público
- ✅ No hay información sensible
- ✅ Todos los cambios registrados en Git
- ✅ Control de acceso por permisos
- ✅ Requerimiento: PR review antes de merge
- ✅ Protección de rama principal (`main`)

---

## 📦 Próximo Paso: Deploy a Main

Cuando Prefacht esté lista:

```bash
# 1. Asegurar todos los tests pasan
npm run test

# 2. Build para producción
npm run build

# 3. Crear PR: Prefacht → main
# (mediante GitHub UI)

# 4. Después de aprobación
git checkout main
git pull origin main
git merge Prefacht
git push origin main
```

---

## 📄 Licencia

Este proyecto es parte de un programa formativo académico.  
Todos los derechos reservados al equipo de desarrollo.

---

**Última revisión:** 20 de Agosto de 2026  
**Versión README:** 2.0 (Rama Prefacht)  
**Estado:** ✅ Activa - Preparada para Testing  
**Próximo Merge:** Pendiente QA Final  

---

*Para clonar esta rama:*
```bash
git clone -b Prefacht https://github.com/AndresStw/Proyecto-Formativo-SGO.git
```

*Para más información, visita:* [GitHub Repository](https://github.com/AndresStw/Proyecto-Formativo-SGO)
