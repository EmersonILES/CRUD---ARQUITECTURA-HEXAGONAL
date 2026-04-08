from decimal import Decimal, InvalidOperation
import re

from flask import Blueprint, redirect, render_template, request, url_for

from src.application.casos_uso import (
  actualizar_producto,
  actualizar_imagen_producto,
  crear_producto,
  crear_imagen_producto,
  eliminar_producto,
  eliminar_imagen_producto,
  existe_producto_duplicado,
  listar_imagenes,
  listar_productos,
  obtener_imagen_producto,
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

  def validar_campos_imagen(descripcion: str, url: str):
    if not descripcion or not url:
      return False, "Descripcion y URL son obligatorios para la imagen."

    if len(descripcion) < 4 or len(descripcion) > 180:
      return False, "La descripcion debe tener entre 4 y 180 caracteres."

    if not re.fullmatch(r"https?://\S+", url):
      return False, "La URL debe iniciar con http:// o https://"

    return True, ""

  @productos_c.route("/productos")
  def obtener_productos():
    data = listar_productos(repositorio_producto)
    return render_template(
      "productos.html",
      data=data,
      producto_editar=None,
      imagen_editar=None,
      mensaje_error=None,
      form_data=None,
    )

  @productos_c.route("/productos/crear", methods=["POST"])
  def crear_nuevo_producto():
    producto = request.form.get("producto", "").strip()
    marca = request.form.get("marca", "").strip()
    precio = request.form.get("precio", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    url = request.form.get("url", "").strip()

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
        imagen_editar=None,
        mensaje_error=mensaje_error,
        form_data={
          "producto": producto,
          "marca": marca,
          "precio": precio,
          "descripcion": descripcion,
          "url": url,
        },
      )

    valido_imagen, mensaje_error_imagen = validar_campos_imagen(descripcion, url)
    if not valido_imagen:
      data = listar_productos(repositorio_producto)
      return render_template(
        "productos.html",
        data=data,
        producto_editar=None,
        imagen_editar=None,
        mensaje_error=mensaje_error_imagen,
        form_data={
          "producto": producto,
          "marca": marca,
          "precio": precio,
          "descripcion": descripcion,
          "url": url,
        },
      )

    if existe_producto_duplicado(repositorio_producto, producto, marca):
      data = listar_productos(repositorio_producto)
      return render_template(
        "productos.html",
        data=data,
        producto_editar=None,
        imagen_editar=None,
        mensaje_error="Ya existe un producto con la misma marca.",
        form_data={
          "producto": producto,
          "marca": marca,
          "precio": precio,
          "descripcion": descripcion,
          "url": url,
        },
      )

    id_creado = crear_producto(repositorio_producto, producto, marca, precio_valido)
    crear_imagen_producto(
      repositorio_imagen,
      id_creado,
      producto,
      descripcion,
      url,
    )

    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/productos/editar/<int:idproducto>", methods=["GET", "POST"])
  def editar_producto(idproducto):
    producto_existente = obtener_producto_por_id(repositorio_producto, idproducto)
    if not producto_existente:
      return redirect(url_for("productos_c.obtener_productos"))

    if request.method == "POST":
      producto_anterior = producto_existente["producto"]
      producto = request.form.get("producto", "").strip()
      marca = request.form.get("marca", "").strip()
      precio = request.form.get("precio", "").strip()
      descripcion = request.form.get("descripcion", "").strip()
      url = request.form.get("url", "").strip()

      valido, mensaje_error, precio_valido = validar_campos_producto(
        producto,
        marca,
        precio,
      )

      if not valido:
        data = listar_productos(repositorio_producto)
        imagen_existente = obtener_imagen_producto(
          repositorio_imagen,
          idproducto,
          producto_anterior,
        )
        return render_template(
          "productos.html",
          data=data,
          producto_editar=producto_existente,
          imagen_editar=imagen_existente,
          mensaje_error=mensaje_error,
          form_data={
            "producto": producto,
            "marca": marca,
            "precio": precio,
            "descripcion": descripcion,
            "url": url,
          },
        )

      valido_imagen, mensaje_error_imagen = validar_campos_imagen(descripcion, url)
      if not valido_imagen:
        data = listar_productos(repositorio_producto)
        imagen_existente = obtener_imagen_producto(
          repositorio_imagen,
          idproducto,
          producto_anterior,
        )
        return render_template(
          "productos.html",
          data=data,
          producto_editar=producto_existente,
          imagen_editar=imagen_existente,
          mensaje_error=mensaje_error_imagen,
          form_data={
            "producto": producto,
            "marca": marca,
            "precio": precio,
            "descripcion": descripcion,
            "url": url,
          },
        )

      if existe_producto_duplicado(
        repositorio_producto,
        producto,
        marca,
        idproducto,
      ):
        data = listar_productos(repositorio_producto)
        imagen_existente = obtener_imagen_producto(
          repositorio_imagen,
          idproducto,
          producto_anterior,
        )
        return render_template(
          "productos.html",
          data=data,
          producto_editar=producto_existente,
          imagen_editar=imagen_existente,
          mensaje_error="Ya existe un producto con la misma marca.",
          form_data={
            "producto": producto,
            "marca": marca,
            "precio": precio,
            "descripcion": descripcion,
            "url": url,
          },
        )

      actualizar_producto(
        repositorio_producto,
        idproducto,
        producto,
        marca,
        precio_valido,
      )
      actualizar_imagen_producto(
        repositorio_imagen,
        idproducto,
        producto,
        producto_anterior,
        descripcion,
        url,
      )

      return redirect(url_for("productos_c.obtener_productos"))

    data = listar_productos(repositorio_producto)
    imagen_existente = obtener_imagen_producto(
      repositorio_imagen,
      idproducto,
      producto_existente["producto"],
    )
    return render_template(
      "productos.html",
      data=data,
      producto_editar=producto_existente,
      imagen_editar=imagen_existente,
      mensaje_error=None,
      form_data=None,
    )

  @productos_c.route("/productos/eliminar/<int:idproducto>", methods=["POST"])
  def eliminar_un_producto(idproducto):
    producto_existente = obtener_producto_por_id(repositorio_producto, idproducto)
    if not producto_existente:
      return redirect(url_for("productos_c.obtener_productos"))

    eliminar_producto(repositorio_producto, idproducto)
    eliminar_imagen_producto(
      repositorio_imagen,
      idproducto,
      producto_existente["producto"],
    )
    return redirect(url_for("productos_c.obtener_productos"))

  @productos_c.route("/imagenes_productos")
  def obtener_imagenes():
    data2 = listar_imagenes(repositorio_imagen)
    return render_template("imagenes_productos.html", data2=data2)

  return productos_c






