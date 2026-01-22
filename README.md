# NutriAgenda - Flet Version

Aplicación de gestión nutricional moderna hecha con Python y Flet.

## 🚀 Características

- ✅ Interfaz moderna y responsive (Web + Móvil)
- ✅ Autenticación con Firebase
- ✅ Dashboard para nutricionistas y clientes
- ✅ Gestión de clientes
- ✅ Agenda de citas
- ✅ Registro de mediciones corporales
- ✅ Compatible con Android APK

## 📦 Tecnologías

- **Frontend**: Flet (Python UI framework)
- **Backend**: Firebase (Auth, Firestore, Storage)
- **Lenguaje**: Python 3.9+

## 🛠️ Instalación

### Prerrequisitos

- Python 3.9 o superior
- Cuenta de Firebase
- (Opcional) Flutter SDK para compilar APK

### Pasos

1. **Clonar/Navegar al proyecto**
```bash
cd /home/raulsalazar/CascadeProjects/nutri-agenda-flet
```

2. **Crear entorno virtual (recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar Firebase**

Copia el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de Firebase:
```env
FIREBASE_API_KEY=tu_api_key
FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com
FIREBASE_PROJECT_ID=tu_proyecto_id
FIREBASE_STORAGE_BUCKET=tu_proyecto.appspot.com
# ... etc
```

**Importante**: También necesitas el archivo de credenciales de Firebase Admin:
- Ve a Firebase Console → Project Settings → Service Accounts
- Genera nueva clave privada (descarga JSON)
- Guarda como `firebase-admin-key.json` en la raíz del proyecto

5. **Ejecutar la aplicación**

```bash
# Modo desarrollo (navegador)
flet run main.py

# Modo web
flet run main.py --web

# Modo desktop
flet run main.py --desktop
```

## 📱 Probar en Navegador

Una vez ejecutado, Flet abrirá automáticamente tu navegador en `http://localhost:XXXX`.

Puedes probar la app directamente en el navegador antes de compilar la APK.

## 📦 Compilar APK para Android

### Prerrequisitos
- Flutter SDK instalado y configurado
- Android SDK instalado

### Pasos

1. **Instalar Flutter** (si no lo tienes)
```bash
# Descarga Flutter desde https://flutter.dev/docs/get-started/install
# O usa snap en Linux:
sudo snap install flutter --classic

# Verifica instalación
flutter doctor
```

2. **Configurar Android SDK**
```bash
flutter doctor --android-licenses
```

3. **Compilar APK**
```bash
flet build apk
```

La APK se generará en `build/apk/app-release.apk`

### Compilación personalizada
```bash
# APK específica
flet build apk --project="NutriAgenda" --description="Nutrición Profesional"

# Con icono personalizado
flet build apk --icon="assets/icon.png"
```

## 📂 Estructura del Proyecto

```
nutri-agenda-flet/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias Python
├── .env.example           # Template de configuración
│
├── services/              # Servicios backend
│   ├── firebase_config.py
│   ├── auth_service.py
│   ├── client_service.py
│   ├── appointment_service.py
│   └── measurement_service.py
│
├── ui/                    # Interfaz de usuario
│   └── screens/
│       ├── login_screen.py
│       ├── register_screen.py
│       ├── nutritionist_dashboard.py
│       └── client_dashboard.py
│
├── utils/                 # Utilidades
│   └── theme.py           # Tema y colores
│
└── assets/               # Recursos (imágenes, etc.)
```

## 🎯 Uso

### Crear Usuarios de Prueba

1. Ejecuta la app
2. Ve a "Registrarse"
3. Crea un usuario nutricionista y uno cliente

**Nutricionista:**
- Email: nutri@test.com
- Contraseña: test123
- Rol: Nutricionista

**Cliente:**
- Email: cliente@test.com
- Contraseña: test123
- Rol: Cliente

### Navegar la App

- **Nutricionistas**: Verán dashboard con estadísticas de clientes y citas
- **Clientes**: Verán sus próximas citas y últimas mediciones

## 🔥 Configuración de Firebase

### Firestore Collections

La app utiliza estas colecciones:

- `users/` - Usuarios (nutricionistas y clientes)
- `clients/` - Información de clientes
- `appointments/` - Citas programadas
- `measurements/` - Mediciones corporales

### Reglas de Seguridad

Copia estas reglas en Firebase Console → Firestore → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    match /clients/{clientId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update, delete: if resource.data.nutritionistId == request.auth.uid;
    }
    
    match /appointments/{appointmentId} {
      allow read, write: if request.auth != null;
    }
    
    match /measurements/{measurementId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 🐛 Troubleshooting

**Error: Firebase not initialized**
→ Verifica que el archivo `.env` y `firebase-admin-key.json` existen

**Error al compilar APK**
→ Ejecuta `flutter doctor` y resuelve los problemas

**La app no carga**
→ Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`

## 📝 Próximas Funcionalidades

- [ ] Gráficos de progreso con charts
- [ ] Galería de fotos de progreso
- [ ] Sistema de notificaciones
- [ ] Integración con Mercado Pago
- [ ] Modo offline

## 👥 Soporte

Para problemas o preguntas, contacta al desarrollador.

## 📄 Licencia

Proyecto privado y propietario.
