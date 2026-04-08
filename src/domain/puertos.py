from typing import Protocol


class RepositorioProducto(Protocol):

  def leer_productos(self):
    ...

  def obtener_producto_por_id(self, idproducto):
    ...

  def crear_producto(self, producto, marca, precio):
    ...

  def actualizar_producto(self, idproducto, producto, marca, precio):
    ...

  def eliminar_producto(self, idproducto):
    ...

  def existe_producto_duplicado(self, producto, marca, idproducto_excluir=None):
    ...


class RepositorioImagenProducto(Protocol):

  def leer_imagenes(self):
    ...
