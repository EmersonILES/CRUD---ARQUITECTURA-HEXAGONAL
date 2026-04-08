from src.config.mongo_connection import get_mongo_connection
from src.config.mysql_connection import get_mysql_connection


class ProductoMysql:

  @staticmethod
  def leer_productos():
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM producto AS p")
        datos = cursor.fetchall()
      return datos
    finally:
      connection.close()

  @staticmethod
  def obtener_producto_por_id(idproducto):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          "SELECT * FROM producto WHERE idproducto = %s",
          (idproducto,),
        )
        return cursor.fetchone()
    finally:
      connection.close()

  @staticmethod
  def crear_producto(producto, marca, precio):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          "INSERT INTO producto (producto, marca, precio) VALUES (%s, %s, %s)",
          (producto, marca, precio),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
      connection.close()

  @staticmethod
  def actualizar_producto(idproducto, producto, marca, precio):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          """
          UPDATE producto
          SET producto = %s, marca = %s, precio = %s
          WHERE idproducto = %s
          """,
          (producto, marca, precio, idproducto),
        )
        connection.commit()
        return cursor.rowcount
    finally:
      connection.close()

  @staticmethod
  def eliminar_producto(idproducto):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        cursor.execute(
          "DELETE FROM producto WHERE idproducto = %s",
          (idproducto,),
        )
        connection.commit()
        return cursor.rowcount
    finally:
      connection.close()

  @staticmethod
  def existe_producto_duplicado(producto, marca, idproducto_excluir=None):
    connection = get_mysql_connection()
    try:
      with connection.cursor() as cursor:
        if idproducto_excluir is None:
          cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM producto
            WHERE LOWER(TRIM(producto)) = LOWER(TRIM(%s))
              AND LOWER(TRIM(marca)) = LOWER(TRIM(%s))
            """,
            (producto, marca),
          )
        else:
          cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM producto
            WHERE LOWER(TRIM(producto)) = LOWER(TRIM(%s))
              AND LOWER(TRIM(marca)) = LOWER(TRIM(%s))
              AND idproducto <> %s
            """,
            (producto, marca, idproducto_excluir),
          )

        result = cursor.fetchone()
        return result["total"] > 0
    finally:
      connection.close()


class ImagenProductoMongo:

  @staticmethod
  def leer_imagenes():
    db = get_mongo_connection()
    imagenes = list(db.producto.aggregate([
      {
        "$project": {
          "_id": 0
        }
      }
    ]))

    return imagenes
