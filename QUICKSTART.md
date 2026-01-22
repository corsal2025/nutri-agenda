# NutriAgenda Flet - Guía de Ejecución Rápida

## 🚀 Paso 1: Instalar Dependencias

```bash
cd /home/raulsalazar/CascadeProjects/nutri-agenda-flet

# Crear entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate

# Instalar todas las dependencias
pip install -r requirements.txt
```

## 🔥 Paso 2: Configurar Firebase (IMPORTANTE)

### Opción A: Usar Firebase Admin SDK (Recomendado)

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto
3. Ve a **Project Settings** → **Service Accounts**
4. Click en **Generate new private key**
5. Descarga el archivo JSON
6. Guárdalo como `firebase-admin-key.json` en la raíz del proyecto

### Opción B: Variables de entorno

1. Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales de Firebase

**NOTA**: Sin Firebase configurado, la app mostrará errores al intentar autenticar.

## 🌐 Paso 3: Ejecutar en Navegador

### Modo Web (Recomendado para pruebas)

```bash
flet run main.py --web
```

Esto abrirá automáticamente tu navegador en `http://localhost:8550` (o el puerto que asigne Flet).

### Modo Desktop

```bash
flet run main.py
```

Abrirá una ventana nativa de la aplicación.

### Ver en Dispositivo Móvil (misma red)

```bash
flet run main.py --web --port 8550
```

Luego abre en tu móvil: `http://TU_IP_LOCAL:8550`

## 📱 Paso 4: Compilar APK para Android

### Prerrequisitos

```bash
# Instalar Flutter (si no lo tienes)
sudo snap install flutter --classic

# Verificar instalación
flutter doctor

# Aceptar licencias de Android
flutter doctor --android-licenses
```

### Compilar

```bash
# APK básica
flet build apk

# APK con configuración personalizada
flet build apk \
  --project="NutriAgenda" \
  --description="Gestión Profesional de Nutrición" \
  --org="com.nutriagenda" \
  --version="1.0.0"
```

La APK se generará en: `build/apk/app-release.apk`

### Instalar en dispositivo Android

```bash
# Conecta tu dispositivo por USB
# Habilita "Depuración USB" en opciones de desarrollador

adb install build/apk/app-release.apk
```

## 🧪 Paso 5: Probar la Aplicación

### Crear Usuario de Prueba

1. Ejecuta la app
2. Click en **"Registrarse"**
3. Completa el formulario:
   - **Nombre**: Test Nutricionista
   - **Email**: nutri@test.com
   - **Teléfono**: +54 9 11 1234-5678
   - **Contraseña**: test123 (mínimo 6 caracteres)
   - **Rol**: Nutricionista

4. Click en **"Registrarse"**
5. Vuelve a login e inicia sesión

### Crear Cliente

Repite el proceso para crear un usuario cliente:
- Email: cliente@test.com
- Rol: Cliente

## 🎨 Interfaz

### Pantallas Implementadas

- ✅ **Login**: Autenticación con email/contraseña
- ✅ **Registro**: Crear cuenta con rol (nutricionista/cliente)
- ✅ **Dashboard Nutricionista**: 
  - Estadísticas (total clientes, citas hoy, próximas citas)
  - Acciones rápidas (agregar cliente, nueva cita, ver clientes)
- ✅ **Dashboard Cliente**:
  - Próxima cita programada
  - Última medición
  - Acciones (agendar cita, ver progreso)

### Responsive Design

La app está optimizada para:
- 📱 Móvil (320px+)
- 💻 Desktop (1024px+)
- 🌐 Web

## 🔧 Troubleshooting

### Error: "No module named 'flet'"

```bash
pip install flet
```

### Error: "Firebase not initialized"

Verifica que:
1. El archivo `firebase-admin-key.json` existe
2. O el archivo `.env` tiene las credenciales correctas

### Error al compilar APK

```bash
# Verifica que Flutter esté instalado
flutter doctor

# Si falta Android SDK:
flutter doctor --android-licenses
```

### La app no carga datos

- Verifica tu conexión a internet
- Revisa las reglas de Firebase Firestore
- Comprueba que el usuario esté autenticado

## 📊 Próximos Pasos

Después de probar la app, puedes:

1. **Implementar pantallas adicionales**:
   - Lista de clientes
   - Formulario de agregar cliente
   - Calendario de citas
   - Formulario de mediciones

2. **Agregar gráficos de progreso**:
```bash
pip install matplotlib
# o
pip install plotly
```

3. **Integrar Mercado Pago** para pagos

4. **Agregar notificaciones push**

## 📚 Recursos Adicionales

- [Documentación de Flet](https://flet.dev/docs/)
- [Firebase Python Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Flet Gallery - Ejemplos](https://flet.dev/gallery/)

---

¿Problemas? Revisa el archivo `README.md` principal o contacta al desarrollador.
