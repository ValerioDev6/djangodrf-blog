# Django REST API Blog

Una API REST construida con Django REST Framework para gestión de blog con funcionalidades completas.

## 🚀 Tecnologías

- **Django 5.2+** - Framework web Python
- **Django REST Framework** - API REST toolkit
- **PostgreSQL** - Base de datos relacional
- **Redis** - Cache y sesiones
- **Docker & Docker Compose** - Containerización
- **Uvicorn** - Servidor ASGI

## ⚡ Inicio Rápido

### 1. Clonar el proyecto
```bash
git clone <tu-repo-url>
cd django-api-blog
```

### 2. Configurar entorno
```bash
# Copiar variables de entorno
cp .env.example .env

# Editar con tus credenciales
nano .env
```

### 3. Levantar con Docker
```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser
```

## 🌐 Endpoints

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API** | http://localhost:8000 | Django REST API |
| **Admin** | http://localhost:8000/admin | Panel administrativo |
| **Docs** | http://localhost:8000/api/docs | Documentación API |

## 📊 Servicios

### Desarrollo
- **Django**: Puerto 8000
- **PostgreSQL**: Puerto 5432
- **Redis**: Puerto 6379
- **pgAdmin**: Puerto 8080 (opcional)

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Ejecutar comandos Django
docker-compose exec backend python manage.py <comando>

# Acceder al shell Django
docker-compose exec backend python manage.py shell

# Ejecutar tests
docker-compose exec backend python manage.py test

# Colectar archivos estáticos
docker-compose exec backend python manage.py collectstatic

# Crear migraciones
docker-compose exec backend python manage.py makemigrations

# Parar servicios
docker-compose down
```

## 📁 Estructura del Proyecto

```
django-api-blog/
├── core/                 # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── apps/                 # Aplicaciones Django
├── requirements.txt      # Dependencias Python
├── docker-compose.yml    # Orquestación Docker
├── Dockerfile           # Imagen Django
├── .env.example         # Variables de entorno template
└── manage.py           # CLI Django
```

## 🛠️ Configuración

### Variables de Entorno (.env)

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:pass@host:port/dbname
REDIS_URL=redis://host:port/db
```

## 📝 Desarrollo

### Instalar dependencias localmente
```bash
pip install -r requirements.txt
```

### Ejecutar sin Docker
```bash
python manage.py runserver
```

## 🔐 Producción

### Configuraciones importantes
- Cambiar `DEBUG=False`
- Configurar `ALLOWED_HOSTS`
- Usar variables de entorno seguras
- Configurar HTTPS
- Usar un servidor web (Nginx)

## 📦 Deploy

```bash
# Construir para producción
docker-compose -f docker-compose.prod.yml up --build

# Con variables de producción
docker-compose -f docker-compose.prod.yml --env-file .env.prod up
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@ValerioDev6](https://github.com/ValerioDev6)
