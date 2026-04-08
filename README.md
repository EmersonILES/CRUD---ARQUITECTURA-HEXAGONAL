# Proyecto CRUD con Arquitectura Hexagonal

## Descripcion
Este proyecto corresponde a una aplicacion web en Flask con arquitectura hexagonal, conectada a:
- MySQL para la gestion de productos.
- MongoDB para la visualizacion de imagenes de productos.

El proyecto base entregado por el docente solo realizaba lectura de datos. En esta entrega se completo el CRUD de productos y se agregaron validaciones de negocio y de datos.

## Arquitectura (Hexagonal)
La aplicacion esta organizada en capas:

- `src/domain/`: define puertos (contratos)
- `src/application/`: casos de uso
- `src/adapters/`: implementaciones concretas de persistencia
- `src/controllers/`: entrada HTTP (Flask)
- `src/templates/`: vistas HTML

Flujo general:
1. El controlador recibe la solicitud HTTP.
2. El caso de uso ejecuta la logica de aplicacion.
3. El repositorio (adaptador) accede a la base de datos.

## Que se implemento
### 1) CRUD completo para productos
Se agregaron operaciones:
- Create
- Read (ya existia)
- Update
- Delete

Rutas principales:
- `GET /productos` -> listar productos
- `POST /productos/crear` -> crear producto
- `GET /productos/editar/<idproducto>` -> cargar producto en modo edicion
- `POST /productos/editar/<idproducto>` -> actualizar producto
- `POST /productos/eliminar/<idproducto>` -> eliminar producto
- `GET /imagenes_productos` -> listar imagenes desde MongoDB

### 2) Validacion de duplicados
Se agrego validacion para evitar registros duplicados por combinacion:
- `producto + marca`

La validacion aplica en:
- creacion
- actualizacion (excluyendo el id actual)

### 3) Validacion de datos
Se agregaron validaciones en backend y frontend:

Backend:
- Campos obligatorios (`producto`, `marca`, `precio`)
- `producto` y `marca` con formato valido (2 a 80 caracteres, letras/numeros/espacios/guion)
- `precio` numerico y mayor que 0

Frontend:
- Input de `precio` como numerico (`type="number"`, `step="0.01"`, `min="0.01"`)
- Mensajes de error mostrados en el formulario

## Tecnologias
- Python
- Flask
- PyMySQL
- PyMongo
- Bootstrap 5

## Requisitos
- Python 3.x
- MySQL activo
- MongoDB activo
- Base de datos `mercancia` creada (scripts en `dbs/`)

## Instalacion y ejecucion
1. Crear y activar entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicacion:

```bash
flask run
```

4. Abrir en navegador:
- `http://127.0.0.1:5000/productos`
- `http://127.0.0.1:5000/imagenes_productos`

## Criterios del docente y estado
- Arquitectura hexagonal: Cumplido
- CRUD completo: Cumplido
- Validar duplicados: Cumplido
- Validar tipos de dato en formularios y backend: Cumplido
- Subir link de GitHub: Pendiente de publicacion

## Link del repositorio
Agrega aqui el enlace de GitHub una vez publiques el proyecto:

`https://github.com/tu-usuario/tu-repositorio`

## Autor
Estudiante: ____________________
Curso: Programacion Avanzada
Fecha: Abril 2026
