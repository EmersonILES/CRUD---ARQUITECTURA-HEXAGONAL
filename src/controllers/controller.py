from decimal import Decimal, InvalidOperation
import re

from flask import Blueprint, redirect, render_template, request, url_for

from src.application.casos_uso import (
  actualizar_producto,
  crear_producto,
  eliminar_producto,
  existe_producto_duplicado,
  listar_imagenes,
  listar_productos,
  obtener_producto_por_id,
)
from src.domain.puertos import RepositorioImagenProducto, RepositorioProducto


def crear_blueprint_productos(
  repositorio_producto: RepositorioProducto,
  repositorio_imagen: RepositorioImagenProducto,
):
  productos_c = Blueprint(
    'productos_c', __name__, template_folder='../templates'
  )

  def validar_campos_producto(producto: str, marca: str, precio_texto: str):
    if not producto or not marca or not precio_texto:
      return False, "Todos los campos son obligatorios.", None

    if not re.fullmatch(r"[A-Za-z0-9\s\-]{2,80}", producto):
      return (
        False,
        "Producto solo permite letras, numeros, espacios y guiones (2-80).",
        None,
      )

    if not re.fullmatch(r"[A-Za-z0-9\s\-]{2,80}", marca):
      return (
        False,
        "Marca solo permite letras, numeros, espacios y guiones (2-80).",
        None,
      )

    try:
      precio = Decimal(precio_texto)
    except InvalidOperation:
      return False, "El precio debe ser un valor numerico.", None

    if precio <= 0:
      return False, "El precio debe ser mayor que 0.", None

    return True, "", precio

  @productos_c.route("/productos")
  def obtener_productos():
    data = listar_productos(repositorio_producto)
    return render_template(
      "productos.html",
      data=data,
      producto_editar=None,
      mensaje_error=None,
      form_data=None,
    )

  @productos_c.route("/productos/crear", methods=["POST"])
  def crear_nuevo_producto():
    producto = request.form.get("producto", "").strip()
    marca = request.form.get("marca", "").strip()
    precio = request.form.get("precio", "").strip()

    valido, mensaje_error, precio_valido = validar_campos_producto(
      producto,
      marca,
      precio,
    )

    if not valido:
      data = listar_productos(repositorio_producto)
      return render_template(
        "productos.html",
        data=data,
        producto_editar=None,
        mensaje_error=mensaje_error,
        form_data={"producto": producto, "marca": marca, "precio": precio},
      )

    if existe_producto_duplicado(repositorio_producto, producto, marca):
      data = listar_productos(repositorio_producto)
      return render_template(
        "productos.html",
        data=data,
        producto_editar=None,
        mensaje_error="Ya existe un producto con la misma marca.",
        form_data={"producto": producto, "marca": marca, "precio": precio},
      )

    crear_producto(repositorio_producto, producto, marca, precio_valido)

    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/productos/editar/<int:idproducto>", methods=["GET", "POST"])
  def editar_producto(idproducto):
    producto_existente = obtener_producto_por_id(repositorio_producto, idproducto)
    if not producto_existente:
      return redirect(url_for("productos_c.obtener_productos"))

    if request.method == "POST":
      producto = request.form.get("producto", "").strip()
      marca = request.form.get("marca", "").strip()
      precio = request.form.get("precio", "").strip()

      valido, mensaje_error, precio_valido = validar_campos_producto(
        producto,
        marca,
        precio,
      )

      if not valido:
        data = listar_productos(repositorio_producto)
        return render_template(
          "productos.html",
          data=data,
          producto_editar=producto_existente,
          mensaje_error=mensaje_error,
          form_data={"producto": producto, "marca": marca, "precio": precio},
        )

      if existe_producto_duplicado(
        repositorio_producto,
        producto,
        marca,
        idproducto,
      ):
        data = listar_productos(repositorio_producto)
        return render_template(
          "productos.html",
          data=data,
          producto_editar=producto_existente,
          mensaje_error="Ya existe un producto con la misma marca.",
          form_data={"producto": producto, "marca": marca, "precio": precio},
        )

      actualizar_producto(
        repositorio_producto,
        idproducto,
        producto,
        marca,
        precio_valido,
      )

      return redirect(url_for("productos_c.obtener_productos"))

    data = listar_productos(repositorio_producto)
    return render_template(
      "productos.html",
      data=data,
      producto_editar=producto_existente,
      mensaje_error=None,
      form_data=None,
    )

  @productos_c.route("/productos/eliminar/<int:idproducto>", methods=["POST"])
  def eliminar_un_producto(idproducto):
    eliminar_producto(repositorio_producto, idproducto)
    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/imagenes_productos")
  def obtener_imagenes():
    data2 = listar_imagenes(repositorio_imagen)
    return render_template("imagenes_productos.html", data2=data2)

  return productos_c






