# Cómo Obtener Credenciales de Firebase 🔑

## 📋 ¿Qué son las Credenciales de Firebase?

Las credenciales de Firebase son un archivo JSON que le permite a tu aplicación comunicarse de forma segura con los servicios de Firebase (Firestore, Storage, Authentication, etc.).

Este archivo contiene:
- ID del proyecto
- Claves privadas de autenticación
- Configuración de acceso

**⚠️ IMPORTANTE: Este archivo es SECRETO. NUNCA lo compartas ni lo subas a GitHub público.**

---

## 🔥 Paso a Paso: Obtener el Archivo JSON

### 1. Acceder a Firebase Console

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Selecciona tu proyecto (o crea uno nuevo)

### 2. Ir a Configuración del Proyecto

1. Click en el ícono de **engranaje (⚙️)** en la parte superior izquierda
2. Selecciona **"Configuración del proyecto"**

### 3. Ir a Cuentas de Servicio

1. En la parte superior, busca la pestaña **"Cuentas de servicio"**
2. Click en esa pestaña

Verás algo así:

```
Firebase Admin SDK
Tu backend puede autenticarse como un usuario administrador de Firebase
mediante el SDK de Firebase Admin.
```

### 4. Generar Nueva Clave Privada

1. **Importante**: Verifica que esté seleccionado **"Firebase Admin SDK"** (no "Google Cloud")
2. Click en el botón **"Generar nueva clave privada"**
3. Te aparecerá un mensaje de advertencia:

```
⚠️ Mantén este archivo privado.
Este archivo contiene información confidencial, incluida la clave privada
cifrada de tu cuenta de servicio.
```

4. Click en **"Generar clave"**

### 5. Descargar el Archivo

1. Se descargará automáticamente un archivo `.json`
2. El nombre será algo como:
   ```
   nutriagenda-12345-firebase-adminsdk-abc123.json
   ```

### 6. Renombrar el Archivo

Para facilitar su uso:

```bash
# Renombra a:
firebase-admin-key.json
```

---

## 📂 ¿Qué Contiene este Archivo?

El archivo JSON se ve así:

```json
{
  "type": "service_account",
  "project_id": "nutriagenda-12345",
  "private_key_id": "abc123def456...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xxxxx@nutriagenda-12345.iam.gserviceaccount.com",
  "client_id": "1234567890",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

**Campos importantes:**
- `project_id`: ID de tu proyecto de Firebase
- `private_key`: Clave privada (SECRETO)
- `client_email`: Email de la cuenta de servicio

---

## 🔒 Cómo Usar las Credenciales

### Opción 1: Archivo Local (Desarrollo)

```bash
# Guarda el archivo en tu proyecto
/home/raulsalazar/CascadeProjects/nutri-agenda-flet/firebase-admin-key.json

# Asegúrate de que esté en .gitignore
echo "firebase-admin-key.json" >> .gitignore
```

En tu `.env`:
```env
FIREBASE_ADMIN_CREDENTIALS=./firebase-admin-key.json
DEMO_MODE=false
```

### Opción 2: Variables de Entorno (Cloud Run)

**NO subas el archivo a GitHub.**

En Cloud Run:
1. Crea un Secret con el contenido del archivo
2. Móntalo como variable de entorno

```bash
# En Cloud Run → Variables y Secrets
# Crear Secret:
Nombre: firebase-credentials
Valor: [Pegar TODO el contenido del JSON]

# Montar como variable:
FIREBASE_CREDENTIALS
```

Luego modifica `firebase_config.py`:

```python
import os
import json

# Leer desde variable de entorno
firebase_cred = os.getenv('FIREBASE_CREDENTIALS')
if firebase_cred:
    cred = credentials.Certificate(json.loads(firebase_cred))
else:
    # Leer desde archivo
    cred = credentials.Certificate('./firebase-admin-key.json')
```

---

## ✅ Verificar que Funciona

### Test en Local

```python
# test_firebase.py
from services.firebase_config import firebase

print("Testing Firebase connection...")
try:
    db = firebase.db
    print("✅ Firestore connected successfully!")
    
    # Test write
    test_ref = db.collection('test').document('test_doc')
    test_ref.set({'test': True})
    print("✅ Write test successful!")
    
    # Test read
    doc = test_ref.get()
    if doc.exists:
        print("✅ Read test successful!")
    
    # Cleanup
    test_ref.delete()
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

Ejecutar:
```bash
python test_firebase.py
```

---

## 🚨 Seguridad: Lo que NO Debes Hacer

❌ **NO** subas el archivo a GitHub público
❌ **NO** compartas el archivo por email/chat
❌ **NO** lo incluyas en screenshots
❌ **NO** lo copies a carpetas públicas

✅ **SÍ** usa `.gitignore`
✅ **SÍ** usa Secrets en Cloud Run
✅ **SÍ** guárdalo en un gestor de contraseñas
✅ **SÍ** genera una nueva clave si se filtra

---

## 🔄 Regenerar Credenciales

Si accidentalmente expones tus credenciales:

1. Ve a Firebase Console → Configuración → Cuentas de servicio
2. Encuentra la clave expuesta en la lista
3. Click en los 3 puntos (⋮)
4. Selecciona **"Eliminar clave"**
5. Genera una nueva clave siguiendo los pasos anteriores
6. Actualiza tu aplicación con la nueva clave

---

## 📱 Para Cloud Run

Cuando despliegues en Cloud Run:

1. **NO** incluyas el archivo en el repositorio
2. Crea un Secret en Google Cloud:
   ```bash
   gcloud secrets create firebase-credentials \
     --data-file=firebase-admin-key.json
   ```
3. Referencia el secret en Cloud Run:
   - Variables y secrets → Agregar secret
   - Selecciona `firebase-credentials`
   - Monta como variable de entorno

---

## 🎯 Resumen Rápido

```mermaid
graph LR
    A[Firebase Console] --> B[⚙️ Configuración]
    B --> C[Cuentas de servicio]
    C --> D[Generar clave privada]
    D --> E[Descargar JSON]
    E --> F1[Desarrollo Local]
    E --> F2[Cloud Run Secret]
    F1 --> G[firebase-admin-key.json]
    F2 --> H[Variable de entorno]
```

---

## 📞 ¿Problemas?

### Error: "Could not load the default credentials"

**Causa**: Firebase no encuentra las credenciales

**Solución**:
1. Verifica que el archivo existe en la ruta correcta
2. Verifica que el path en `.env` es correcto
3. Verifica que la variable de entorno está configurada

### Error: "Permission denied"

**Causa**: Las credenciales no tienen permisos

**Solución**:
1. Ve a Firebase Console → Configuración → Usuarios y permisos
2. Asegúrate de que la cuenta de servicio tenga rol de **"Editor"** o **"Propietario"**

### Error: "Invalid JSON"

**Causa**: El archivo JSON está corrupto

**Solución**:
1. Elimina el archivo actual
2. Genera una nueva clave privada desde Firebase Console

---

## ✅ Checklist

- [ ] Accedí a Firebase Console
- [ ] Seleccioné mi proyecto
- [ ] Fui a Configuración → Cuentas de servicio
- [ ] Generé nueva clave privada
- [ ] Descargué el archivo JSON
- [ ] Lo renombré a `firebase-admin-key.json`
- [ ] Lo agregué a `.gitignore`
- [ ] Verifiqué que funciona localmente
- [ ] (Para producción) Lo subí como Secret a Cloud Run

---

¡Listo! Ahora tu aplicación puede conectarse a Firebase de forma segura. 🎉
