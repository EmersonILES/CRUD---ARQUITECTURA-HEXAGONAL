from flask import Flask

from src.adapters.repositorios import ImagenProductoMongo, ProductoMysql
from src.controllers.controller import crear_blueprint_productos

app = Flask(__name__, template_folder="src/templates")

app.register_blueprint(
  crear_blueprint_productos(ProductoMysql(), ImagenProductoMongo())
)

if __name__ == "__main__":
  app.run(debug=True)




