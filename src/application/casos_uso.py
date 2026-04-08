from src.domain.puertos import RepositorioImagenProducto, RepositorioProducto


def listar_productos(repositorio: RepositorioProducto):
  return repositorio.leer_productos()


def obtener_producto_por_id(repositorio: RepositorioProducto, idproducto):
  return repositorio.obtener_producto_por_id(idproducto)


def crear_producto(repositorio: RepositorioProducto, producto, marca, precio):
  return repositorio.crear_producto(producto, marca, precio)


def actualizar_producto(
  repositorio: RepositorioProducto,
  idproducto,
  producto,
  marca,
  precio,
):
  return repositorio.actualizar_producto(idproducto, producto, marca, precio)


def eliminar_producto(repositorio: RepositorioProducto, idproducto):
  return repositorio.eliminar_producto(idproducto)


def existe_producto_duplicado(
  repositorio: RepositorioProducto,
  producto,
  marca,
  idproducto_excluir=None,
):
  return repositorio.existe_producto_duplicado(
    producto,
    marca,
    idproducto_excluir,
  )


def listar_imagenes(repositorio: RepositorioImagenProducto):
  return repositorio.leer_imagenes()


def obtener_imagen_producto(
  repositorio: RepositorioImagenProducto,
  idproducto,
  producto,
):
  return repositorio.obtener_imagen_producto(idproducto, producto)


def crear_imagen_producto(
  repositorio: RepositorioImagenProducto,
  idproducto,
  producto,
  descripcion,
  url,
):
  return repositorio.crear_imagen_producto(
    idproducto,
    producto,
    descripcion,
    url,
  )


def actualizar_imagen_producto(
  repositorio: RepositorioImagenProducto,
  idproducto,
  producto,
  producto_anterior,
  descripcion,
  url,
):
  return repositorio.actualizar_imagen_producto(
    idproducto,
    producto,
    producto_anterior,
    descripcion,
    url,
  )


def eliminar_imagen_producto(
  repositorio: RepositorioImagenProducto,
  idproducto,
  producto,
):
  return repositorio.eliminar_imagen_producto(idproducto, producto)
