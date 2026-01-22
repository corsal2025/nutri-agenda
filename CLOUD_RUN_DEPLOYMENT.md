# Google Cloud Run Deployment Guide

## 📋 Requisitos Previos

- [ ] Cuenta de Google Cloud Platform
- [ ] Cuenta de GitHub
- [ ] Cuenta de Firebase (mismo proyecto de Google Cloud)
- [ ] Código de NutriAgenda listo

---

## 🔥 Paso 1: Configurar Firebase

### 1.1 Crear Proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Click en **"Agregar proyecto"**
3. Nombre del proyecto: `nutriagenda-production` (o el que prefieras)
4. **Importante**: Habilita Google Analytics (opcional)
5. Click en **"Crear proyecto"**

### 1.2 Habilitar Firestore Database

1. En el menú izquierdo, busca **"Firestore Database"**
2. Click en **"Crear base de datos"**
3. Selecciona **"Modo de producción"** (más seguro)
4. Ubicación: Selecciona la más cercana a tus usuarios
   - `southamerica-east1` (São Paulo) para Sudamérica
5. Click en **"Habilitar"**

### 1.3 Configurar Reglas de Firestore

En la pestaña "Reglas", reemplaza con:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Usuarios - solo pueden leer/escribir su propia información
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Clientes - nutricionistas pueden gestionar sus clientes
    match /clients/{clientId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update, delete: if resource.data.nutritionistId == request.auth.uid;
    }
    
    // Citas - usuarios autenticados pueden gestionar
    match /appointments/{appointmentId} {
      allow read, write: if request.auth != null;
    }
    
    // Mediciones - usuarios autenticados pueden gestionar
    match /measurements/{measurementId} {
      allow read, write: if request.auth != null;
    }
    
    // Productos - todos pueden leer, solo autenticados pueden escribir
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Órdenes - usuarios autenticados pueden gestionar
    match /orders/{orderId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update: if resource.data.clientId == request.auth.uid;
    }
  }
}
```

Click en **"Publicar"**.

### 1.4 Habilitar Authentication

1. En el menú izquierdo, click en **"Authentication"**
2. Click en **"Comenzar"**
3. En la pestaña "Sign-in method":
   - Habilita **"Correo electrónico/contraseña"**
   - Click en **"Guardar"**

### 1.5 Habilitar Storage

1. En el menú izquierdo, click en **"Storage"**
2. Click en **"Comenzar"**
3. Selecciona **"Modo de producción"**
4. Misma ubicación que Firestore
5. Click en **"Listo"**

### 1.6 Obtener Credenciales de Firebase

**⚠️ IMPORTANTE: Este archivo es SECRETO. Nunca lo subas a GitHub público.**

1. En Firebase Console, ve a **⚙️ Configuración del proyecto**
2. Pestaña **"Cuentas de servicio"**
3. Click en **"Generar nueva clave privada"**
4. Se descargará un archivo `.json` (ejemplo: `nutriagenda-xxxxx.json`)
5. **Renómbralo a**: `firebase-admin-key.json`
6. **Guárdalo en un lugar seguro** (NO en el repositorio de GitHub)

---

## 🐙 Paso 2: Subir Código a GitHub

### 2.1 Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Click en **"+" → "New repository"**
3. Nombre: `nutriagenda-app`
4. Visibilidad: **Privado** (recomendado)
5. **NO** inicialices con README
6. Click en **"Create repository"**

### 2.2 Subir tu Código

```bash
cd /home/raulsalazar/CascadeProjects/nutri-agenda-flet

# Inicializar repositorio Git (si no existe)
git init

# Agregar remote de GitHub (cambiar por tu URL)
git remote add origin https://github.com/TU_USUARIO/nutriagenda-app.git

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - NutriAgenda Flet app"

# Subir a GitHub
git push -u origin main
```

**⚠️ VERIFICAR**: Asegúrate de que `.gitignore` existe y contenga:
```
firebase-admin-key.json
.env
```

---

## ☁️ Paso 3: Desplegar en Google Cloud Run

### 3.1 Acceder a Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. **Importante**: Selecciona el **mismo proyecto** que Firebase
   - Arriba a la izquierda, verifica que diga el nombre de tu proyecto

### 3.2 Habilitar APIs necesarias

1. En el menú (☰), ve a **"APIs y servicios" → "Biblioteca"**
2. Busca y habilita:
   - **Cloud Run API**
   - **Cloud Build API**
   - **Container Registry API**

### 3.3 Configurar Cloud Run

1. En el menú (☰), ve a **"Cloud Run"**
2. Click en **"CREAR SERVICIO"**

#### Opción: Implementar desde GitHub

1. Selecciona **"Implementar continuamente a partir de un repositorio (GitHub)"**
2. Click en **"CONFIGURAR CON CLOUD BUILD"**
3. Click en **"Autenticar"** y conecta tu cuenta de GitHub
4. Selecciona tu repositorio: `TU_USUARIO/nutriagenda-app`
5. Rama: `main` o `master`
6. Tipo de compilación: **Dockerfile**
7. Ubicación del Dockerfile: `/Dockerfile`
8. Click en **"GUARDAR"**

#### Configuración del servicio

1. **Nombre del servicio**: `nutriagenda`
2. **Región**: Selecciona la más cercana
   - `southamerica-east1` (São Paulo) recomendado para Sudamérica
3. **CPU allocation**: Asignar CPU solo durante el procesamiento de solicitudes
4. **Autoscaling**:
   - Mínimo: `0` instancias (ahorro de costos)
   - Máximo: `10` instancias

#### Autenticación

**⚠️ MUY IMPORTANTE:**

Selecciona: **"Permitir invocaciones sin autenticar"**

✅ Esto permite que cualquiera acceda a tu app desde el navegador sin login de Google.

#### Variables de entorno

Click en **"CONTENEDOR, VARIABLES, SECRETS, CONEXIONES"**

En la pestaña **"Variables y secrets"**:

**Agregar variable de entorno:**
- `DEMO_MODE` = `false`

**Agregar secret (credenciales de Firebase):**

1. Click en **"HACER REFERENCIA A UN SECRET"**
2. Click en **"CREAR SECRET"**
   - Nombre: `firebase-credentials`
   - Valor: **Pega el contenido COMPLETO del archivo `firebase-admin-key.json`**
   - Click en **"CREAR SECRET"**
3. Montar como: **Variable de entorno**
   - Nombre de variable: `FIREBASE_CREDENTIALS`
4. Click en **"LISTO"**

#### Configuración final

1. Click en **"CREAR"**
2. Espera 2-5 minutos mientras se despliega

---

## 🎉 Paso 4: Acceder a tu Aplicación

### 4.1 Obtener URL

Una vez desplegado, verás:

```
✅ Servicio nutriagenda implementado correctamente
```

La URL será algo como:
```
https://nutriagenda-xxxxx-uc.a.run.app
```

### 4.2 Probar la Aplicación

1. Abre la URL en tu navegador
2. Deberías ver la pantalla de login de NutriAgenda
3. Registra un usuario de prueba
4. ¡Listo! 🎊

---

## 🔒 Paso 5: Configurar Dominio Personalizado (Opcional)

### 5.1 Mapear Dominio

1. En Cloud Run, selecciona tu servicio
2. Click en **"ADMINISTRAR DOMINIOS PERSONALIZADOS"**
3. Click en **"AGREGAR MAPEO"**
4. Ingresa tu dominio: `nutriagenda.tudominio.com`
5. Sigue las instrucciones para verificar el dominio

### 5.2 Configurar DNS

Agrega estos registros en tu proveedor de dominios:

```
Tipo: CNAME
Nombre: nutriagenda
Valor: ghs.googlehosted.com
```

---

## 💰 Costos Estimados

Cloud Run usa un modelo "pay-as-you-go":

**Capa gratuita (por mes):**
- 2 millones de solicitudes
- 360,000 GB-segundos de memoria
- 180,000 vCPU-segundos

**Para una app pequeña:**
- 100-500 usuarios/día: **GRATIS** 🎉
- 1,000+ usuarios/día: ~$5-20 USD/mes

**Consejo:** Con `Mínimo: 0` instancias, no pagas cuando nadie usa la app.

---

## 🔧 Troubleshooting

### Error: "Permission denied"

**Solución:** Verifica que los secrets estén correctamente configurados:
```bash
gcloud secrets list
```

### Error: "Port 8080 not listening"

**Solución:** Verifica que `main.py` use la variable de entorno `PORT`:
```python
port = int(os.environ.get("PORT", 8080))
```

### La app no carga

**Solución:** Ver logs en Cloud Run:
1. Selecciona tu servicio
2. Pestaña **"REGISTROS"**
3. Busca errores en rojo

### Firebase connection error

**Solución:** Verifica que el secret `firebase-credentials` esté bien configurado:
- Debe ser el contenido COMPLETO del archivo JSON
- Sin espacios extra al inicio/final

---

## 📱 Compartir con tu Amiga

Una vez desplegado, solo comparte la URL:

```
https://nutriagenda-xxxxx-uc.a.run.app
```

Ella podrá:
1. Abrir desde cualquier navegador
2. Agregar al inicio de su celular (PWA)
3. Usar como app normal

**Para agregar al inicio (Android/iOS):**
1. Abrir la URL en Chrome/Safari
2. Menú (⋮ o Share)
3. **"Agregar a pantalla de inicio"**
4. ¡Listo! Tendrá un icono como app nativa

---

## 🚀 Actualizaciones Automáticas

Con GitHub + Cloud Build configurado:

1. Haces cambios en tu código local
2. Subes a GitHub:
   ```bash
   git add .
   git commit -m "Mejoras en dashboard"
   git push
   ```
3. **Cloud Run despliega automáticamente** 🎉
4. En 2-3 minutos, la nueva versión está online

---

## ✅ Checklist Final

- [ ] Firebase proyecto creado
- [ ] Firestore habilitado con reglas
- [ ] Authentication habilitado
- [ ] Storage habilitado
- [ ] Credenciales JSON descargadas
- [ ] Código subido a GitHub (sin secrets)
- [ ] Cloud Run configurado
- [ ] Variables de entorno configuradas
- [ ] Secrets de Firebase agregados
- [ ] Servicio desplegado exitosamente
- [ ] URL funcionando
- [ ] Usuarios pueden registrarse

---

## 📚 Recursos

- [Firebase Console](https://console.firebase.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Flet Documentation](https://flet.dev/docs/)

---

¿Problemas? Revisa los logs en Cloud Run o contacta al desarrollador.
