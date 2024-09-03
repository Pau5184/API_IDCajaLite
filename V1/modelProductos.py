from pymongo import MongoClient
from bson import ObjectId
from bson.binary import Binary
import base64

class Conexion():
    def __init__(self, db_name):
        self.cliente = MongoClient("mongodb+srv://sipsasoluciones:sLHaml3BAWlERcoP@cluster0.idzpxoq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        # self.cliente = MongoClient("mongodb+srv://apbarajas658:32GeaC79hqdZNTbf@cluster0.6f3klmh.mongodb.net/")
        self.db = self.cliente[db_name]
        
    def registrarProducto(self, data):
        resp = {"estatus": "", "mensaje": ""}
        try:
            producto = self.db.Productos.find_one({"codigoBase": data["codigoBase"]})
            if producto:
                resp["estatus"] = "error"
                resp["mensaje"] = "Error. Este producto ya existe. Inténtelo de nuevo"
            else:
                image_binary = base64.b64decode(data['foto'])
                data['foto'] = Binary(image_binary)
                
                if data["unidadBase"]:
                    data["unidadBase"] = ObjectId(data["unidadBase"])
                
                if data["unidadCompra"]:
                    data["unidadCompra"] = ObjectId(data["unidadCompra"])
                
                self.db.Productos.insert_one(data)
                resp["estatus"] = "ok"
                resp["mensaje"] = "Producto registrado"
        except Exception as e:
            resp["estatus"] = "error"
            resp["mensaje"] = str(e)
        return resp
    
    def obtenerProductos(self):
        resp = {"estatus": "", "mensaje": ""}
        productos = self.db.Productos.find()
        listaProductos = []
        
        for s in productos:
            image_base64 = base64.b64encode(s['foto']).decode('utf-8')
            
            # Look up unidadBase in UnidadesMedida collection
            unidad_base_nombre = ""
            if s["unidadBase"]:
                unidad_base = self.db.UnidadesMedida.find_one({"_id": ObjectId(s["unidadBase"])})
                if unidad_base:
                    unidad_base_nombre = unidad_base.get("nombre")
            
            # Look up unidadCompra in UnidadesMedida collection
            unidad_compra_nombre = ""
            if s["unidadCompra"]:
                unidad_compra = self.db.UnidadesMedida.find_one({"_id": ObjectId(s["unidadCompra"])})
                if unidad_compra:
                    unidad_compra_nombre = unidad_compra.get("nombre")
            
            listaProductos.append({
                "codigoBase": s["codigoBase"],
                "nombre": s["nombre"],
                "existencia": s["existencia"],
                "precios": s["precios"],
                "unidadBase": unidad_base_nombre,
                "unidadCompra": unidad_compra_nombre,
                "costoCompra": s["costoCompra"],
                "fechaUltimaCompra": s["fechaUltimaCompra"],
                "foto": image_base64
            })
        
        if len(listaProductos) > 0:
            resp["estatus"] = "ok"
            resp["mensaje"] = "Lista de productos"
            resp["productos"] = listaProductos
        else:
            resp["estatus"] = "error"
            resp["mensaje"] = "No hay productos registrados"
        
        return resp
    
    def obtenerFotosProductos(self):
        resp={"estatus":"", "mensaje":""}
        productos = self.db.Productos.find()
        listaProductos = []
        for s in productos:
            image_base64 = base64.b64encode(s['foto']).decode('utf-8')
            listaProductos.append({"codigoBase":s["codigoBase"], "foto":image_base64})
        if len(listaProductos) > 0:
            resp["estatus"]="ok"
            resp["mensaje"]="Lista de fotos"
            resp["fotos"]=listaProductos
        else:
            resp["estatus"]="error"
            resp["mensaje"]="No hay productos registrados"
        return resp
    
    def obtenerProducto(self, codigoBase):
        resp = {"estatus": "", "mensaje": ""}
        producto = self.db.Productos.find_one({"codigoBase": codigoBase})
        
        if producto:
            image_base64 = base64.b64encode(producto['foto']).decode('utf-8')
            
            # Look up unidadBase in UnidadesMedida collection
            unidad_base_nombre = ""
            if producto["unidadBase"]:
                unidad_base = self.db.UnidadesMedida.find_one({"_id": ObjectId(producto["unidadBase"])})
                if unidad_base:
                    unidad_base_nombre = unidad_base.get("nombre")
            
            # Look up unidadCompra in UnidadesMedida collection
            unidad_compra_nombre = ""
            if producto["unidadCompra"]:
                unidad_compra = self.db.UnidadesMedida.find_one({"_id": ObjectId(producto["unidadCompra"])})
                if unidad_compra:
                    unidad_compra_nombre = unidad_compra.get("nombre")
            
            resp["estatus"] = "ok"
            resp["mensaje"] = "Producto encontrado"
            resp["producto"] = {
                "codigoBase": producto["codigoBase"],
                "nombre": producto["nombre"],
                "descripcion": producto["descripcion"],
                "unidadBase": unidad_base_nombre,
                "unidadCompra": unidad_compra_nombre,
                "factorConversion": producto["factorConversion"],
                "existencia": producto["existencia"],
                "proveedor": producto["proveedor"],
                "estatus": producto["estatus"],
                "minimoVender": producto["minimoVender"],
                "marca": producto["marca"],
                "linea": producto["linea"],
                "ancho": producto["ancho"],
                "alto": producto["alto"],
                "largo": producto["largo"],
                "volumen": producto["volumen"],
                "precios": producto["precios"],
                "costoCompra": producto["costoCompra"],
                "fechaUltimaCompra": producto["fechaUltimaCompra"],
                "foto": image_base64
            }
        else:
            resp["estatus"] = "error"
            resp["mensaje"] = "Producto no encontrado"
        
        return resp
    
    def editarProducto(self, data):
        resp = {"estatus":"","mensaje":""}
        try:
            producto=self.db.Productos.find_one({"codigoBase":data["codigoBase"]})
            if producto:
                if 'foto' in data:
                    image_binary = base64.b64decode(data['foto'])
                    data['foto'] = Binary(image_binary)

                # Look up unidadBase and unidadCompra in UnidadesMedida collection
                if 'unidadBase' in data and data["unidadBase"]:
                    try:
                        data["unidadBase"] = ObjectId(data["unidadBase"])
                    except Exception as e:
                        data["unidadBase"] = ""

                if 'unidadCompra' in data and data["unidadCompra"]:
                    try:
                        data["unidadCompra"] = ObjectId(data["unidadCompra"])
                    except Exception as e:
                        data["unidadCompra"] = ""
                
                self.db.Productos.update_one({"codigoBase":data["codigoBase"]},{"$set":data})
                resp["estatus"]="ok"
                resp["mensaje"]="Producto actualizado"
            else:
                resp["estatus"]="error"
                resp["mensaje"]="Producto no encontrado"
        except Exception as e:
            resp["estatus"]="error"
            resp["mensaje"]=str
        return resp
    
    def eliminarProducto(self, codigoBase):
        resp = {"estatus":"","mensaje":""}
        producto=self.db.Productos.find_one({"codigoBase":codigoBase})
        if producto:
            self.db.Productos.delete_one({"codigoBase":codigoBase})
            resp["estatus"]="ok"
            resp["mensaje"]="Producto eliminado"
        else:
            resp["estatus"]="error"
            resp["mensaje"]="Producto no encontrado"
        return resp
    
    def obtenerProductosVenta(self):
        resp={"estatus":"", "mensaje":""}
        productos = self.db.Productos.find()
        listaProductos = []
        for s in productos:
            # Check if the precios array is not empty
            if s['precios']:
                image_base64 = base64.b64encode(s['foto']).decode('utf-8')
                # Look up unidadBase in UnidadesMedida collection
                unidad_base_nombre = ""
                if s["unidadBase"]:
                    unidad_base = self.db.UnidadesMedida.find_one({"_id": ObjectId(s["unidadBase"])})
                    if unidad_base:
                        unidad_base_nombre = unidad_base.get("nombre")

                listaProductos.append({
                    "codigoBase":s["codigoBase"], 
                    "nombre":s["nombre"], 
                    "existencia":s["existencia"], 
                    "precio":s["precios"][0]["total"],  # Only include the total of the first precio
                    "unidadBase":unidad_base_nombre,
                    "foto":image_base64
                })
        if len(listaProductos) > 0:
            resp["estatus"]="ok"
            resp["mensaje"]="Lista de productos"
            resp["productos"]=listaProductos
        else:
            resp["estatus"]="error"
            resp["mensaje"]="No hay productos registrados"
        return resp