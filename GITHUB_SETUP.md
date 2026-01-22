# Subir Código a GitHub - Guía Paso a Paso

## 📋 Requisitos

- Cuenta de GitHub ([crear aquí](https://github.com/join))
- Git instalado en tu sistema
- Código de NutriAgenda listo

---

## 🚀 Opción 1: Subir desde la Terminal (Recomendado)

### 1. Ir a tu Proyecto

```bash
cd /home/raulsalazar/CascadeProjects/nutri-agenda-flet
```

### 2. Inicializar Git (si no está inicializado)

```bash
git init
```

### 3. Configurar Git (solo primera vez)

```bash
# Tu nombre
git config --global user.name "Tu Nombre"

# Tu email (el mismo de GitHub)
git config --global user.email "tu@email.com"
```

### 4. Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Click en el **"+" arriba** a la derecha
3. Selecciona **"New repository"**
4. Configuración:
   - **Repository name**: `nutriagenda-app`
   - **Description**: `Aplicación de gestión nutricional con Flet y Firebase`
   - **Visibilidad**: 
     - ✅ **Private** (recomendado - solo tú lo ves)
     - ⚠️ Public (todos pueden verlo)
   - **NO** marques "Initialize with README"
5. Click en **"Create repository"**

### 5. Conectar tu Código Local con GitHub

GitHub te mostrará instrucciones. Copia el comando que dice:

```bash
git remote add origin https://github.com/TU_USUARIO/nutriagenda-app.git
```

O usa SSH (más seguro):

```bash
git remote add origin git@github.com:TU_USUARIO/nutriagenda-app.git
```

### 6. Agregar Archivos al Repositorio

```bash
# Ver qué archivos se subirán
git status

# Agregar todos los archivos
git add .

# Verificar que firebase-admin-key.json NO esté en la lista
git status

# Si aparece, asegúrate de tenerlo en .gitignore
echo "firebase-admin-key.json" >> .gitignore
git add .gitignore
```

### 7. Hacer Commit

```bash
git commit -m "Initial commit - NutriAgenda Flet application"
```

### 8. Subir a GitHub

```bash
# Verificar rama
git branch

# Si no existe 'main', créala
git branch -M main

# Subir todo
git push -u origin main
```

Si usa HTTPS, te pedirá:
- **Username**: Tu usuario de GitHub
- **Password**: Tu **Personal Access Token** (NO tu contraseña de GitHub)

#### Crear Personal Access Token

1. GitHub → Settings (tu perfil) → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Nombre: `nutriagenda-deploy`
5. Permisos:
   - ✅ `repo` (todos)
   - ✅ `workflow`
6. Generate token
7. **COPIA EL TOKEN** (solo se muestra una vez)
8. Úsalo como "password" cuando Git te lo pida

### 9. Verificar en GitHub

1. Refresca tu repositorio en GitHub
2. Deberías ver todos tus archivos
3. **Verifica que NO esté**:
   - `firebase-admin-key.json`
   - `.env` (si tiene datos sensibles)
   - `venv/` o `node_modules/`

---

## 🔄 Actualizaciones Futuras

Cuando hagas cambios:

```bash
# Ver qué cambió
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Agregué formulario de clientes"

# Subir a GitHub
git push
```

---

## 🌐 Opción 2: GitHub Desktop (Interfaz Gráfica)

### 1. Descargar GitHub Desktop

1. Ve a [desktop.github.com](https://desktop.github.com/)
2. Descarga para tu sistema operativo
3. Instala y abre la aplicación
4. Inicia sesión con tu cuenta de GitHub

### 2. Agregar tu Proyecto

1. En GitHub Desktop:
   - File → Add local repository
   - Choose: `/home/raulsalazar/CascadeProjects/nutri-agenda-flet`
2. Si no está inicializado, click en "Create repository"

### 3. Hacer Commit

1. Verás todos los archivos en la lista
2. **Importante**: Verifica que `firebase-admin-key.json` NO esté
3. Escribe mensaje: "Initial commit - NutriAgenda"
4. Click en "Commit to main"

### 4. Publicar en GitHub

1. Click en "Publish repository"
2. Nombre: `nutriagenda-app`
3. Marca "Keep this code private" si quieres que sea privado
4. Click en "Publish repository"

---

## 🔒 Seguridad: Archivos que NO Debes Subir

Asegúrate de que `.gitignore` contenga:

```gitignore
# Secrets y credenciales
firebase-admin-key.json
.env

# Python
__pycache__/
*.py[cod]
venv/
env/

# Flet
build/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

### Verificar .gitignore

```bash
# Ver contenido
cat .gitignore

# Si no existe, créalo
cat > .gitignore << 'EOF'
firebase-admin-key.json
.env
__pycache__/
*.py[cod]
venv/
build/
.vscode/
.idea/
.DS_Store
*.log
EOF
```

---

## 🐛 Problemas Comunes

### Error: "git: command not found"

**Solución**: Instala Git

```bash
# Ubuntu/Debian
sudo apt-get install git

# Verificar instalación
git --version
```

### Error: "Permission denied (publickey)"

**Causa**: Intentas usar SSH sin configurar claves

**Solución 1** (más fácil): Usa HTTPS en lugar de SSH

```bash
git remote set-url origin https://github.com/TU_USUARIO/nutriagenda-app.git
```

**Solución 2**: Configura SSH keys

```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu@email.com"

# Copiar clave pública
cat ~/.ssh/id_ed25519.pub

# Agregar en GitHub → Settings → SSH keys
```

### Error: "fatal: repository not found"

**Causa**: La URL del repositorio es incorrecta

**Solución**:

```bash
# Ver URL actual
git remote -v

# Cambiar URL
git remote set-url origin https://github.com/TU_USUARIO_CORRECTO/nutriagenda-app.git
```

### Error: "rejected - non-fast-forward"

**Causa**: El repositorio remoto tiene cambios que tu local no tiene

**Solución**:

```bash
# Traer cambios del remoto
git pull origin main --rebase

# Luego subir
git push
```

---

## 🎯 Checklist Final

Antes de continuar a Cloud Run, verifica:

- [ ] Código subido a GitHub exitosamente
- [ ] `firebase-admin-key.json` NO está en GitHub
- [ ] `.env` NO está en GitHub (o está en `.gitignore`)
- [ ] `.gitignore` está configurado correctamente
- [ ] Puedes ver el código en GitHub.com
- [ ] El repositorio es privado (recomendado)
- [ ] Tienes las credenciales de GitHub guardadas

---

## 📚 Comandos Git Útiles

```bash
# Ver estado
git status

# Ver historial
git log --oneline

# Ver diferencias
git diff

# Deshacer cambios no commiteados
git checkout -- archivo.py

# Ver ramas
git branch

# Cambiar de rama
git checkout nombre-rama

# Crear rama nueva
git checkout -b nueva-funcionalidad

# Fusionar rama
git merge nombre-rama
```

---

## ✅ Siguiente Paso

Una vez que tu código esté en GitHub, continúa con:

👉 [CLOUD_RUN_DEPLOYMENT.md](file:///home/raulsalazar/CascadeProjects/nutri-agenda-flet/CLOUD_RUN_DEPLOYMENT.md)

---

¿Problemas con GitHub? [Contacta soporte de GitHub](https://support.github.com/)
