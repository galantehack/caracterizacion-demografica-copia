from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
import io
import base64
from functools import wraps
from flask_login import login_required


app = Flask(__name__,  static_folder='static')   # importante para que tome los estilos en la carpeta static
import matplotlib
matplotlib.use('Agg')
#la configuración app = Flask(__name__, static_folder='static') instancia de la aplicación Flask, asegura que Flask pueda servir archivos estáticos correctamente, y matplotlib.use('Agg') configura Matplotlib para generar gráficos de manera adecuada en un entorno sin interfaz gráfica.

# Configuración de la base de datos MySQL
db = mysql.connector.connect (
    host="localhost",
    user="root",
    password="",
    database="caracterizacion"
)
cursor = db.cursor()

app.secret_key ="miclave"

#funcion para crear el decorador para proteger las rutas 
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id_rol') != 1:
            
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function2(*args, **kwargs):
        if session.get('id_rol') != 2 and  session.get('id_rol') != 1:
            
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function2

#pagina de inicio encuestador
@app.route('/index')
@user_required
def index():
   
    return render_template('index.html')


@app.route('/')
@user_required
def index2():
   
    return render_template('login.html')
#LISTAR USUARIOS
# Ruta para mostrar los datos de usuario en una tabla HTML
@app.route('/sidebar_miembros')
@user_required
def listar():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT reconocimiento, nombre, apellido, identidad, sexo, edad, escolaridad,  direccion, sector, id_encuesta FROM miembros")
    usuarios = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_miembros.html', miembros=usuarios)


@app.route("/Agmiembros",  methods=["GET", "POST"])
@user_required
def Agmiembros():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       reconocimiento =  ','.join(request.form.getlist("reconocimiento"))
       nombre = request.form["nombre"]  # Esta línea de código extrae los datos ingresados por el usuario en el campo "nombre" del formulario HTML y los asigna a la variable nombre. Después de ejecutar esta línea, la variable nombre contendrá el valor ingresado por el usuario en el campo "nombre".
       apellido = request.form["apellido"]
       identidad = request.form["identidad"]
       sexo =request.form["sexo"] 
       edad =request.form["edad"] 
       escolaridad = request.form["escolaridad"]
       #id = request.form["id"]
       direccion = request.form["direccion"]
       sector = request.form["sector"]
       id_encuesta = request.form["id_encuesta"]
       cursor.execute("INSERT INTO miembros (reconocimiento, nombre, apellido, identidad, sexo, edad, escolaridad, direccion, sector, id_encuesta)  VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (reconocimiento, nombre, apellido, identidad, sexo, edad, escolaridad, direccion, sector, id_encuesta)) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("Agmiembros")) # redirije a la pagina despues del proceso 
    else:
      return render_template("Agmiembros.html")
  
# ENCUESTA DE TERRITORIO   
@app.route("/territorio",  methods=["GET", "POST"])
@user_required
def territorio():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       a1 =  ','.join(request.form.getlist("a1"))
       a2 =  ','.join(request.form.getlist("a2"))
       a3 =  ','.join(request.form.getlist("a3"))
       a4 =  ','.join(request.form.getlist("a4"))
       a5_1 =  ','.join(request.form.getlist("a5_1"))
       a5_2 =  ','.join(request.form.getlist("a5_2"))
       a5_3 =  ','.join(request.form.getlist("a5_3"))
       a5_4 =  ','.join(request.form.getlist("a5_4"))
       a5_5 =  ','.join(request.form.getlist("a5_5"))
       a5_6 =  ','.join(request.form.getlist("a5_6"))
       a6 =  ','.join(request.form.getlist("a6"))
       id_encuesta =  ','.join(request.form.getlist("id_encuesta"))

      
       cursor.execute("INSERT INTO territorio (a1, a2, a3, a4, a5_1, a5_2, a5_3, a5_4, a5_5, a5_6 , a6, id_encuesta )  VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (a1, a2, a3, a4, a5_1, a5_2, a5_3, a5_4, a5_5, a5_6 , a6, id_encuesta)) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       session['id_encuesta'] = id_encuesta   #mantiene la session del id para que se replique en los otros formularios
       return redirect(url_for("identidad")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("territorio.html")    
  
  
  #listar territorio
@app.route('/sidebar_territorio')
@user_required
def lista_territorio():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT a1, a2, a3, a4, a5_1, a5_2, a5_3, a5_4, a5_5, a5_6 , a6, id_encuesta FROM territorio")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_territorio.html', territorio=respuesta)  
  
  
  
  #ENCUESTA IDENTIDAD
@app.route("/identidad",  methods=["GET", "POST"])
@user_required
def identidad():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       b1 =  ','.join(request.form.getlist("b1"))
       b2 =  ','.join(request.form.getlist("b2"))
       b3 =  ','.join(request.form.getlist("b3"))
       b4 =  ','.join(request.form.getlist("b4"))
       b5 =  ','.join(request.form.getlist("b5"))
       b6_1 =  ','.join(request.form.getlist("b6_1"))
       b6_2 =  ','.join(request.form.getlist("b6_2"))
       b6_3 =  ','.join(request.form.getlist("b6_3"))
       b6_4 =  ','.join(request.form.getlist("b6_4"))
       b6_5 =  ','.join(request.form.getlist("b6_5"))
       b7 =  ','.join(request.form.getlist("b7"))
       id_encuesta = session.get('id_encuesta')#  sesion toma la session del id llave foranea desde llave primaria 
      


       cursor.execute("INSERT INTO identidad (b1, b2, b3, b4, b5, b6_1, b6_2, b6_3, b6_4, b6_5,  b7, id_encuesta )  VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (b1, b2, b3, b4, b5, b6_1, b6_2, b6_3, b6_4, b6_5,  b7, id_encuesta)) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("desarrollo")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("identidad.html")    
    
# listar identidad
@app.route('/sidebar_identidad')
@user_required
def lista_identidad():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT b1, b2, 	b3, b4, b5, b6_1, b6_2, b6_3, b6_4, b6_5, b7, id_encuesta FROM identidad")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_identidad.html', identidad=respuesta)



# ENCUESTA DE DESARROLLO
@app.route("/desarrollo", methods=["GET", "POST"])
@user_required
def desarrollo():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       c1_1 =  ','.join(request.form.getlist("c1_1"))
       c1_2 =  ','.join(request.form.getlist("c1_2"))
       c1_3 =  ','.join(request.form.getlist("c1_3"))
       c1_4 =  ','.join(request.form.getlist("c1_4"))
       c1_5 =  ','.join(request.form.getlist("c1_5"))
       c1_6 =  ','.join(request.form.getlist("c1_6"))
       c1_7 =  ','.join(request.form.getlist("c1_7"))
       c1_8 =  ','.join(request.form.getlist("c1_8"))
       id_encuesta = session.get('id_encuesta')
      


       cursor.execute("INSERT INTO desarrollo (c1_1, c1_2, c1_3, c1_4, c1_5, c1_6, c1_7, c1_8, id_encuesta )  VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s )", (c1_1, c1_2, c1_3, c1_4, c1_5, c1_6, c1_7, c1_8, id_encuesta )) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("vivienda")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("desarrollo.html")  
  
#LISTAR ENCUESTA DESARROLLO
@app.route('/sidebar_desarrollo')
@user_required
def lista_desarrollo():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT c1_1, c1_2, 	c1_3, c1_4, c1_5, c1_6, c1_7, c1_8, id_encuesta FROM desarrollo")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_desarrollo.html', desarrollo=respuesta)



  
 # encuesta vivienda 
@app.route("/vivienda", methods=["GET", "POST"])
@user_required
def vivienda():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       
       d1_1 =  ','.join(request.form.getlist("d1_1"))
       d1_2 =  ','.join(request.form.getlist("d1_2"))
       d1_3 =  ','.join(request.form.getlist("d1_3"))
       d1_4 =  ','.join(request.form.getlist("d1_4"))
       d2_1 =  ','.join(request.form.getlist("d2_1"))
       d2_2 =  ','.join(request.form.getlist("d2_2"))
       d2_3 = request.form["d2_3"]
       d3_1 =  ','.join(request.form.getlist("d3_1"))
       d3_2 =  ','.join(request.form.getlist("d3_2"))
       d3_3 =  ','.join(request.form.getlist("d3_3"))
       d3_4 =  ','.join(request.form.getlist("d3_4"))
       d4_1 =  ','.join(request.form.getlist("d4_1"))
       d4_2 =  ','.join(request.form.getlist("d4_2"))
       d4_3 =  ','.join(request.form.getlist("d4_3"))
       d4_4 =  ','.join(request.form.getlist("d4_4"))
       d4_5 =  ','.join(request.form.getlist("d4_5"))
       d4_6 = request.form["d4_6"]
       d4_7 =  ','.join(request.form.getlist("d4_7"))
       d5_1 =  ','.join(request.form.getlist("d5_1"))
       d5_2 =  ','.join(request.form.getlist("d5_2"))
       d5_3 =  ','.join(request.form.getlist("d5_3"))
       d5_4 =  ','.join(request.form.getlist("d5_4"))
       d5_5 =  ','.join(request.form.getlist("d5_5"))
       d5_6 = request.form["d5_6"]
       d6_1 =  ','.join(request.form.getlist("d6_1"))
       d6_2 =  ','.join(request.form.getlist("d6_2"))
       d6_3 =  ','.join(request.form.getlist("d6_3"))
       d6_4 =  ','.join(request.form.getlist("d6_4"))
       d6_5 =  ','.join(request.form.getlist("d6_5"))
       d6_6 = request.form["d6_6"]
       d6_7 =  ','.join(request.form.getlist("d6_7"))
       d7_1 =  ','.join(request.form.getlist("d7_1"))
       d7_2 =  ','.join(request.form.getlist("d7_2"))
       d7_3 =  ','.join(request.form.getlist("d7_3"))
       d7_4 =  ','.join(request.form.getlist("d7_4"))
       d7_5 =  ','.join(request.form.getlist("d7_5"))
       d7_6 =  ','.join(request.form.getlist("d7_6"))
       d7_7 =  ','.join(request.form.getlist("d7_7"))
       d7_8 =  ','.join(request.form.getlist("d7_8"))
       id_encuesta = session.get('id_encuesta')
 

       cursor.execute("INSERT INTO vivienda (d1_1, d1_2, d1_3, d1_4, d2_1, d2_2, d2_3, d3_1, d3_2, d3_3, d3_4, d4_1, d4_2, d4_3, d4_4 , d4_5, d4_6, d4_7, d5_1, d5_2, d5_3, d5_4, d5_5, d5_6, d6_1, d6_2, d6_3, d6_4, d6_5, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8, id_encuesta  ) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (d1_1, d1_2, d1_3, d1_4, d2_1, d2_2, d2_3, d3_1, d3_2, d3_3, d3_4, d4_1, d4_2, d4_3, d4_4 , d4_5, d4_6, d4_7, d5_1, d5_2, d5_3, d5_4, d5_5, d5_6, d6_1, d6_2, d6_3, d6_4, d6_5, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8, id_encuesta )) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("saneamiento")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("vivienda.html")


     #listar vivienda
@app.route('/sidebar_vivienda')
@user_required
def lista_vivienda():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT d1_1, d1_2, d1_3, d1_4, d2_1, d2_2, d2_3, d3_1, d3_2, d3_3, d3_4, d4_1, d4_2, d4_3, d4_4 , d4_5, d4_6, d4_7, d5_1, d5_2, d5_3, d5_4, d5_5, d5_6, d6_1, d6_2, d6_3, d6_4, d6_5, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8, id_encuesta FROM vivienda")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_vivienda.html', vivienda=respuesta)



    
    
  # encuesta saneamiento  
@app.route("/saneamiento", methods=["GET", "POST"])
@user_required
def saneamiento():
    if request.method == "POST":   #  permite al servidor distinguir entre las solicitudes en las que el usuario está enviando datos al servidor (POST) 
       
       e1_1 =  ','.join(request.form.getlist("e1_1"))
       e1_2 =  ','.join(request.form.getlist("e1_2"))
       e1_3 =  ','.join(request.form.getlist("e1_3"))
       e1_4 =  ','.join(request.form.getlist("e1_4"))
       e1_5 =  ','.join(request.form.getlist("e1_5"))
       e1_6 =  ','.join(request.form.getlist("e1_6"))
       e1_7 =  ','.join(request.form.getlist("e1_7"))
       e1_8 =  ','.join(request.form.getlist("e1_8"))
      
       e2_1 =  ','.join(request.form.getlist("e2_1"))
       e2_2 =  ','.join(request.form.getlist("e2_2"))
       e2_3 =  ','.join(request.form.getlist("e2_3"))
       e3_1 =  ','.join(request.form.getlist("e3_1"))
       e3_2 =  ','.join(request.form.getlist("e3_2"))
       e3_3 =  ','.join(request.form.getlist("e3_3"))
       e4_1 =  ','.join(request.form.getlist("e4_1"))
       e4_2 =  ','.join(request.form.getlist("e4_2"))
       e4_3 =  ','.join(request.form.getlist("e4_3"))
       
       e5_1 =  ','.join(request.form.getlist("e5_1"))
       e5_2 =  ','.join(request.form.getlist("e5_2"))
       e5_3 =  ','.join(request.form.getlist("e5_3"))
       e5_4 =  ','.join(request.form.getlist("e5_4"))
       e6_1 =  ','.join(request.form.getlist("e6_1"))
       e6_2 =  ','.join(request.form.getlist("e6_2"))
      
       e7_1 =  ','.join(request.form.getlist("e7_1"))
       e7_2 =  ','.join(request.form.getlist("e7_2"))
       e7_3 =  ','.join(request.form.getlist("e7_3"))
       e7_4 =  ','.join(request.form.getlist("e7_4"))
       e7_5 =  ','.join(request.form.getlist("e7_5"))
       
       e8 =  ','.join(request.form.getlist("e8"))
       e9_1 =  ','.join(request.form.getlist("e9_1"))
       e9_2 =  ','.join(request.form.getlist("e9_2"))
       e9_3 = request.form["e9_3"]
       e10_1 =  ','.join(request.form.getlist("e10_1"))
       e10_2 =  ','.join(request.form.getlist("e10_2"))
       e10_3 = request.form["e10_3"]
       e11_1 =  ','.join(request.form.getlist("e11_1"))
       e11_2 =  ','.join(request.form.getlist("e11_2"))
       e11_3 =  ','.join(request.form.getlist("e11_3"))
       e11_4 =  ','.join(request.form.getlist("e11_4"))
       e11_5 =  ','.join(request.form.getlist("e11_5"))
       id_encuesta = session.get('id_encuesta')
      


       cursor.execute("INSERT INTO saneamiento (e1_1, e1_2, e1_3, e1_4, e1_5, e1_6, e1_7, e1_8, e2_1, e2_2, e2_3, e3_1, e3_2, e3_3, e4_1, e4_2, e4_3, e5_1, e5_2, e5_3, e5_4, e6_1, e6_2, e7_1, e7_2, e7_3, e7_4, e7_5, e8, e9_1, e9_2, e9_3, e10_1, e10_2, e10_3, e11_1, e11_2, e11_3, e11_4, e11_5, id_encuesta  ) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  )", (e1_1, e1_2, e1_3, e1_4, e1_5, e1_6, e1_7, e1_8, e2_1, e2_2, e2_3, e3_1, e3_2, e3_3, e4_1, e4_2, e4_3, e5_1, e5_2, e5_3, e5_4, e6_1, e6_2, e7_1, e7_2, e7_3, e7_4, e7_5, e8,e9_1, e9_2, e9_3, e10_1, e10_2, e10_3, e11_1, e11_2, e11_3, e11_4, e11_5, id_encuesta  )) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("Agmiembros")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("saneamiento.html")
  
     #listar saneamiento
@app.route('/sidebar_saneamiento')
@user_required
def lista_saneamiento():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT e1_1, e1_2, e1_3, e1_4, e1_5, e1_6, e1_7, e1_8, e2_1, e2_2, e2_3, e3_1, e3_2, e3_3, e4_1, e4_2, e4_3, e5_1, e5_2, e5_3, e5_4, e6_1, e6_2, e7_1, e7_2, e7_3, e7_4, e7_5, e8, e9_1, e9_2, e9_3, e10_1, e10_2, e10_3, e11_1, e11_2, e11_3, e11_4, e11_5, id_encuesta FROM saneamiento")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_saneamiento.html', saneamiento=respuesta)  
  



    
#ruta loging - validacion de usuario
@app.route('/login', methods=["GET", "POST"])

def login():
    #validamos si usuario y contraseña enviados del formulario coinciden con lo de la base de datos 
    if request.method == "POST" and "usuario" in request.form and "contraseña" in request.form:
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        #cuando se llama usuario y contraseña se realñiza el desencriptado con check_password_hash(contraseña, contraseña)
        #contraseña con hash y la que se pone 
        
        cursor.execute("SELECT * FROM login WHERE usuario= %s AND contraseña = %s", (usuario, check_password_hash(contraseña, contraseña)))
        acceso = cursor.fetchone()
       
        if acceso :
           session["logeado"] = True
           session["id"] = acceso[4]
           session["id_rol"]= acceso[5]
           session["usuario"]= acceso[0]
           if session ["id_rol"] ==1:
               return render_template('sidebar_territorio.html')
           if session ["id_rol"] ==2:
               return render_template('index.html')
               
           
        else:
   
           return render_template('login.html', mensaje="credenciales  incorrectas")  
       
    else:
        return render_template('login.html')    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#ruta registrar login
@app.route("/registrar", methods=["GET", "POST"])
@admin_required

def registrar():
    if request.method == "POST": 
       usuario =  request.form["usuario"]
       correo =  request.form["correo"]
       cedula =  request.form["cedula"]
       contraseña =  request.form["contraseña"]  
       idrol =  request.form["idrol"] 
       hashed_password = generate_password_hash(contraseña)
      
       cursor.execute("INSERT INTO login (usuario, correo, cedula, contraseña, idrol )  VALUE (%s, %s, %s, %s, %s )", (usuario, correo, cedula, hashed_password, idrol )) 
       db.commit()  #se confirman todos los cambios pendientes realizados
       return redirect(url_for("registrar")) 
    else:
       return render_template('registrar.html')   
   



#ruta borrar
@app.route('/borrar/<int:id_encuesta>', methods=['GET'])
@user_required
def borrar(id_encuesta):
    cursor.execute("DELETE FROM territorio WHERE id_encuesta = %s" ,(id_encuesta,))
    db.commit() 
    return redirect(url_for('territorio'))

# confrmacion de borrado falta

    


  
# LLAMAR DATOS DE TERRITORIO PARA EDITAR 
@app.route("/editar_territorio/<int:id_encuesta>") #se acede a la ruta pasando el parametro id_encuesta
@user_required
def editar_territorio(id_encuesta):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM territorio WHERE id_encuesta = %s", (id_encuesta,))
        respuesta = cursor.fetchall()
        if respuesta:
            return render_template('editar_territorio.html', territorio=respuesta)
        else:
            return f'Error loading #{id_encuesta}'
    except Exception as e:
        print(e)
        return 'An error occurred'
    finally:
        cursor.close()
      
		
# ACCION QUE ACTUALIZA LOS DATOS DE TERRITORIO EDITAR
@app.route("/actualizar_territorio", methods=['GET', 'POST'])
@user_required
def actualizar_territorio():
    if request.method == 'POST':
        cursor = db.cursor()
        try:
            a1 = ','.join(request.form.getlist("a1"))
            a2 = ','.join(request.form.getlist("a2"))
            a3 = ','.join(request.form.getlist("a3"))
            a4 = ','.join(request.form.getlist("a4"))
            a5_1 = ','.join(request.form.getlist("a5_1"))
            a5_2 = ','.join(request.form.getlist("a5_2"))
            a5_3 = ','.join(request.form.getlist("a5_3"))
            a5_4 = ','.join(request.form.getlist("a5_4"))
            a5_5 = ','.join(request.form.getlist("a5_5"))
            a5_6 = ','.join(request.form.getlist("a5_6"))
            a6 = ','.join(request.form.getlist("a6"))
            id_encuesta = request.form.get("id_encuesta")

            sql = """
                UPDATE territorio
                SET a1 = %s, a2 = %s, a3 = %s, a4 = %s, a5_1 = %s, a5_2 = %s, a5_3 = %s, a5_4 = %s, a5_5 = %s, a5_6 = %s, a6 = %s
                WHERE id_encuesta = %s
            """
            data = (a1, a2, a3, a4, a5_1, a5_2, a5_3, a5_4, a5_5, a5_6, a6, id_encuesta)
            cursor.execute(sql, data)
            db.commit()  
            return redirect('/sidebar_territorio')
        except Exception as e:
            print(e)
            return 'Error while updating user'
        finally:
            cursor.close()
    else:
        return 'Invalid request method'

# LLAMAR DATOS A EDITAR DE IDENTIDAD 
@app.route("/editar_identidad/<int:id_encuesta>")
@user_required
def editar_identidad(id_encuesta):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM identidad WHERE id_encuesta = %s", (id_encuesta,))
            respuesta = cursor.fetchall()
            if respuesta:
                return render_template('editar_identidad.html', identidad=respuesta)
            else:
                return f'Error loading #{id_encuesta}', 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'An error occurred', 500

        
# ACTUALIZAR IDENTIDAD 
@app.route("/actualizar_identidad", methods=['GET', 'POST'])
@user_required
def actualizar_identidad():
    if request.method == 'POST':
        try:
            # Recuperar datos del formulario
            b1 = ','.join(request.form.getlist("b1"))
            b2 = ','.join(request.form.getlist("b2"))
            b3 = ','.join(request.form.getlist("b3"))
            b4 = ','.join(request.form.getlist("b4"))
            b5 = ','.join(request.form.getlist("b5"))
            b6_1 = ','.join(request.form.getlist("b6_1"))
            b6_2 = ','.join(request.form.getlist("b6_2"))
            b6_3 = ','.join(request.form.getlist("b6_3"))
            b6_4 = ','.join(request.form.getlist("b6_4"))
            b6_5 = ','.join(request.form.getlist("b6_5"))
            b7 = ','.join(request.form.getlist("b7"))
            id_encuesta = request.form.get("id_encuesta") #en la actualizacion no se mantiene el sesion ya que modificaria el ultimo registro agregado

            # Verificar que id_encuesta sea un entero válido
            if not id_encuesta or not str(id_encuesta).isdigit():
                return 'Invalid id_encuesta', 400

            id_encuesta = int(id_encuesta)  #se convierte a entero el id_encuesta

            sql = """
                UPDATE identidad
                SET b1=%s, b2=%s, b3=%s, b4=%s, b5=%s, b6_1=%s, b6_2=%s, b6_3=%s, b6_4=%s, b6_5=%s, b7=%s
                WHERE id_encuesta = %s
            """
            data = (b1, b2, b3, b4, b5, b6_1, b6_2, b6_3, b6_4, b6_5, b7, id_encuesta)

            # Ejecutar la consulta de actualización
            with db.cursor() as cursor:
                cursor.execute(sql, data)
                db.commit()

            return redirect('/sidebar_identidad')
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            return 'Database error', 500
        except Exception as e:
            print(f"Error while updating user: {e}")
            return 'Error while updating user', 500
    else:
        return 'Invalid request method', 405

# # LLAMAR DATOS A EDITAR DE DESARROLLO 
@app.route("/editar_desarrollo/<int:id_encuesta>")
@user_required
def editar_desarrollo(id_encuesta):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM desarrollo WHERE id_encuesta = %s", (id_encuesta,))
            respuesta = cursor.fetchall()
            if respuesta:
                return render_template('editar_desarrollo.html', desarrollo=respuesta)
            else:
                return f'Error loading #{id_encuesta}', 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'An error occurred', 500

        
# ACTUALIZAR DESARROLLO 
@app.route("/actualizar_desarrollo", methods=['GET', 'POST'])
@user_required
def actualizar_desarrollo():
    if request.method == 'POST':
        try:
            # Recuperar datos del formulario
            c1_1 =  ','.join(request.form.getlist("c1_1"))
            c1_2 =  ','.join(request.form.getlist("c1_2"))
            c1_3 =  ','.join(request.form.getlist("c1_3"))
            c1_4 =  ','.join(request.form.getlist("c1_4"))
            c1_5 =  ','.join(request.form.getlist("c1_5"))
            c1_6 =  ','.join(request.form.getlist("c1_6"))
            c1_7 =  ','.join(request.form.getlist("c1_7"))
            c1_8 =  ','.join(request.form.getlist("c1_8"))
            id_encuesta = request.form.get("id_encuesta")

            # Verificar que id_encuesta sea un entero válido
            if not id_encuesta or not str(id_encuesta).isdigit():
                return 'Invalid id_encuesta', 400

            id_encuesta = int(id_encuesta)

            sql = """
                UPDATE desarrollo
                SET c1_1=%s, c1_2=%s, c1_3=%s, c1_4=%s, c1_5=%s, c1_6=%s, c1_7=%s, c1_8=%s
                WHERE id_encuesta = %s
            """
            data = (c1_1, c1_2, c1_3, c1_4, c1_5, c1_6, c1_7, c1_8, id_encuesta)

            # Ejecutar la consulta de actualización
            with db.cursor() as cursor:
                cursor.execute(sql, data)
                db.commit()

            return redirect('/sidebar_desarrollo')
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            return 'Database error', 500
        except Exception as e:
            print(f"Error while updating user: {e}")
            return 'Error while updating user', 500
    else:
        return 'Invalid request method', 405
    
    
# # LLAMAR DATOS A EDITAR DE VIVIENDA 
@app.route("/editar_vivienda/<int:id_encuesta>")
@user_required
def editar_vivienda(id_encuesta):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM vivienda WHERE id_encuesta = %s", (id_encuesta,))
            respuesta = cursor.fetchall()
            if respuesta:
                return render_template('editar_vivienda.html', vivienda=respuesta)
            else:
                return f'Error loading #{id_encuesta}', 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'An error occurred', 500

        
# ACTUALIZAR VIVIENDA 
@app.route("/actualizar_vivienda", methods=['GET', 'POST'])
@user_required
def actualizar_vivienda():
    if request.method == 'POST':
        try:
            # Recuperar datos del formulario
            d1_1 =  ','.join(request.form.getlist("d1_1"))
            d1_2 =  ','.join(request.form.getlist("d1_2"))
            d1_3 =  ','.join(request.form.getlist("d1_3"))
            d1_4 =  ','.join(request.form.getlist("d1_4"))
            d2_1 =  ','.join(request.form.getlist("d2_1"))
            d2_2 =  ','.join(request.form.getlist("d2_2"))
            d2_3 = request.form["d2_3"]
            d3_1 =  ','.join(request.form.getlist("d3_1"))
            d3_2 =  ','.join(request.form.getlist("d3_2"))
            d3_3 =  ','.join(request.form.getlist("d3_3"))
            d3_4 =  ','.join(request.form.getlist("d3_4"))
            d4_1 =  ','.join(request.form.getlist("d4_1"))
            d4_2 =  ','.join(request.form.getlist("d4_2"))
            d4_3 =  ','.join(request.form.getlist("d4_3"))
            d4_4 =  ','.join(request.form.getlist("d4_4"))
            d4_5 =  ','.join(request.form.getlist("d4_5"))
            d4_6 = request.form["d4_6"]
            d4_7 =  ','.join(request.form.getlist("d4_7"))
            d5_1 =  ','.join(request.form.getlist("d5_1"))
            d5_2 =  ','.join(request.form.getlist("d5_2"))
            d5_3 =  ','.join(request.form.getlist("d5_3"))
            d5_4 =  ','.join(request.form.getlist("d5_4"))
            d5_5 =  ','.join(request.form.getlist("d5_5"))
            d5_6 = request.form["d5_6"]
            d6_1 =  ','.join(request.form.getlist("d6_1"))
            d6_2 =  ','.join(request.form.getlist("d6_2"))
            d6_3 =  ','.join(request.form.getlist("d6_3"))
            d6_4 =  ','.join(request.form.getlist("d6_4"))
            d6_5 =  ','.join(request.form.getlist("d6_5"))
            d6_6 = request.form["d6_6"]
            d6_7 =  ','.join(request.form.getlist("d6_7"))
            d7_1 =  ','.join(request.form.getlist("d7_1"))
            d7_2 =  ','.join(request.form.getlist("d7_2"))
            d7_3 =  ','.join(request.form.getlist("d7_3"))
            d7_4 =  ','.join(request.form.getlist("d7_4"))
            d7_5 =  ','.join(request.form.getlist("d7_5"))
            d7_6 =  ','.join(request.form.getlist("d7_6"))
            d7_7 =  ','.join(request.form.getlist("d7_7"))
            d7_8 =  ','.join(request.form.getlist("d7_8"))
            id_encuesta = request.form.get("id_encuesta")

            # Verificar que id_encuesta sea un entero válido
            if not id_encuesta or not str(id_encuesta).isdigit():
                return 'Invalid id_encuesta', 400

            id_encuesta = int(id_encuesta)

            sql = """
                UPDATE vivienda
                SET d1_1= %s, d1_2= %s, d1_3= %s, d1_4= %s, d2_1= %s, d2_2= %s, d2_3= %s, d3_1= %s, d3_2= %s, d3_3= %s, d3_4= %s, d4_1= %s, d4_2= %s, d4_3= %s, d4_4= %s , d4_5= %s, d4_6= %s, d4_7= %s, d5_1= %s, d5_2= %s, d5_3= %s, d5_4= %s, d5_5= %s, d5_6= %s, d6_1= %s, d6_2= %s, d6_3= %s, d6_4= %s, d6_5= %s, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8
                WHERE id_encuesta = %s
            """
            data = (d1_1, d1_2, d1_3, d1_4, d2_1, d2_2, d2_3, d3_1, d3_2, d3_3, d3_4, d4_1, d4_2, d4_3, d4_4 , d4_5, d4_6, d4_7, d5_1, d5_2, d5_3, d5_4, d5_5, d5_6, d6_1, d6_2, d6_3, d6_4, d6_5, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8, id_encuesta)

            # Ejecutar la consulta de actualización
            with db.cursor() as cursor:
                cursor.execute(sql, data)
                db.commit()

            return redirect('/sidebar_vivienda')
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            return 'Database error', 500
        except Exception as e:
            print(f"Error while updating user: {e}")
            return 'Error while updating user', 500
    else:
        return 'Invalid request method', 405    
    
# # LLAMAR DATOS A EDITAR DE SANEAMIENTO 
@app.route("/editar_saneamiento/<int:id_encuesta>")
@user_required
def editar_saneamiento(id_encuesta):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM saneamiento WHERE id_encuesta = %s", (id_encuesta,))
            respuesta = cursor.fetchall()
            if respuesta:
                return render_template('editar_saneamiento.html', saneamiento=respuesta)
            else:
                return f'Error loading #{id_encuesta}', 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'An error occurred', 500



# ACTUALIZAR SANEAMIENTO 
@app.route("/actualizar_saneamiento", methods=['GET', 'POST'])
@user_required
def actualizar_saneamiento():
    if request.method == 'POST':
        try:
            # Recuperar datos del formulario
            e1_1 =  ','.join(request.form.getlist("e1_1"))
            e1_2 =  ','.join(request.form.getlist("e1_2"))
            e1_3 =  ','.join(request.form.getlist("e1_3"))
            e1_4 =  ','.join(request.form.getlist("e1_4"))
            e1_5 =  ','.join(request.form.getlist("e1_5"))
            e1_6 =  ','.join(request.form.getlist("e1_6"))
            e1_7 =  ','.join(request.form.getlist("e1_7"))
            e1_8 =  ','.join(request.form.getlist("e1_8"))
            e2_1 =  ','.join(request.form.getlist("e2_1"))
            e2_2 =  ','.join(request.form.getlist("e2_2"))
            e2_3 =  ','.join(request.form.getlist("e2_3"))
            e3_1 =  ','.join(request.form.getlist("e3_1"))
            e3_2 =  ','.join(request.form.getlist("e3_2"))
            e3_3 =  ','.join(request.form.getlist("e3_3"))
            e4_1 =  ','.join(request.form.getlist("e4_1"))
            e4_2 =  ','.join(request.form.getlist("e4_2"))
            e4_3 =  ','.join(request.form.getlist("e4_3"))            
            e5_1 =  ','.join(request.form.getlist("e5_1"))
            e5_2 =  ','.join(request.form.getlist("e5_2"))
            e5_3 =  ','.join(request.form.getlist("e5_3"))
            e5_4 =  ','.join(request.form.getlist("e5_4"))
            e6_1 =  ','.join(request.form.getlist("e6_1"))
            e6_2 =  ','.join(request.form.getlist("e6_2"))
      
            e7_1 =  ','.join(request.form.getlist("e7_1"))
            e7_2 =  ','.join(request.form.getlist("e7_2"))
            e7_3 =  ','.join(request.form.getlist("e7_3"))
            e7_4 =  ','.join(request.form.getlist("e7_4"))
            e7_5 =  ','.join(request.form.getlist("e7_5"))
       
            e8 =  ','.join(request.form.getlist("e8"))
            e9_1 =  ','.join(request.form.getlist("e9_1"))
            e9_2 =  ','.join(request.form.getlist("e9_2"))
            e9_3 = request.form["e9_3"]
            e10_1 =  ','.join(request.form.getlist("e10_1"))
            e10_2 =  ','.join(request.form.getlist("e10_2"))
            e10_3 = request.form["e10_3"]
            e11_1 =  ','.join(request.form.getlist("e11_1"))
            e11_2 =  ','.join(request.form.getlist("e11_2"))
            e11_3 =  ','.join(request.form.getlist("e11_3"))
            e11_4 =  ','.join(request.form.getlist("e11_4"))
            e11_5 =  ','.join(request.form.getlist("e11_5"))
            id_encuesta = request.form.get("id_encuesta")

            # Verificar que id_encuesta sea un entero válido
            if not id_encuesta or not str(id_encuesta).isdigit():
                return 'Invalid id_encuesta', 400

            id_encuesta = int(id_encuesta)

            sql = """
                UPDATE saneamiento
                SET e1_1 = %s, e1_2= %s, e1_3= %s, e1_4= %s, e1_5= %s, e1_6= %s, e1_7= %s, e1_8= %s, e2_1= %s, e2_2= %s, e2_3= %s, e3_1= %s, e3_2= %s, e3_3= %s, e4_1= %s, e4_2= %s, e4_3= %s, e5_1= %s, e5_2= %s, e5_3= %s, e5_4= %s, e6_1= %s, e6_2= %s, e7_1= %s, e7_2= %s, e7_3= %s, e7_4= %s, e7_5= %s, e8= %s, e9_1= %s, e9_2= %s, e9_3= %s, e10_1= %s, e10_2= %s, e10_3= %s, e11_1= %s, e11_2= %s, e11_3= %s, e11_4= %s, e11_5= %s
                WHERE id_encuesta = %s
            """
            data = (e1_1, e1_2, e1_3, e1_4, e1_5, e1_6, e1_7, e1_8, e2_1, e2_2, e2_3, e3_1, e3_2, e3_3, e4_1, e4_2, e4_3, e5_1, e5_2, e5_3, e5_4, e6_1, e6_2, e7_1, e7_2, e7_3, e7_4, e7_5, e8, e9_1, e9_2, e9_3, e10_1, e10_2, e10_3, e11_1, e11_2, e11_3, e11_4, e11_5, id_encuesta)

            # Ejecutar la consulta de actualización
            with db.cursor() as cursor:
                cursor.execute(sql, data)
                db.commit()

            return redirect('/sidebar_saneamiento')
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            return 'Database error', 500
        except Exception as e:
            print(f"Error while updating user: {e}")
            return 'Error while updating user', 500
    else:
        return 'Invalid request method', 405   
    
# dashboar   grafico   


@app.route('/dashboard')
@admin_required
def dashboard_1():
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM miembros ")
    total_usuarios = cursor.fetchone()[0]
    
   
    cursor.execute("SELECT COUNT(*) FROM miembros WHERE sexo = 'masculino'")
    cantidad_hombres = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM miembros WHERE sexo = 'femenino'")
    cantidad_mujeres = cursor.fetchone()[0]
    
    #grafico por sexo
    cursor.execute("SELECT sexo, COUNT(*) FROM miembros GROUP BY sexo")
    gender_data = cursor.fetchall()
    
    labels = []
    counts = []
    for row in gender_data:
        if row[0] == 'masculino':
            labels.append('Masculino')
        elif row[0] == 'femenino':
            labels.append('Femenino')
        counts.append(row[1])
    
    # Crear gráfica de torta por sexo
    plt.figure(figsize=(4, 4))
    plt.pie(counts, labels=labels, autopct=lambda p: f'{p:.1f}%\n({int(p*sum(counts)/100)})', colors=['blue', 'pink'])
    plt.title("Población por género")
    
    # Guardar gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    
    # Codificar gráfica en base64
    grafica_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
   
    # Consulta para la distribución por reconocimiento
    cursor.execute("SELECT reconocimiento, COUNT(*) FROM miembros GROUP BY reconocimiento")
    reconocimiento_data = cursor.fetchall()
    
    labels2 = []
    counts2 = []
    for row in reconocimiento_data:
        if row[0] == 'si':
            labels2.append('Sí')
        elif row[0] == 'no':
            labels2.append('No')
        counts2.append(row[1])
    
    # Crear gráfica de torta por reconocimiento
    plt.figure(figsize=(4, 4))
    plt.pie(counts2, labels=labels2, autopct=lambda p: f'{p:.1f}%\n({int(p*sum(counts2)/100)})', colors=['green', 'red'])
    plt.title("Distribución por autoreconocimiento")
    
    # Guardar gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    
    # Codificar gráfica en base64
    grafica_base64_2 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    
     # Consulta para la distribución por escolaridad
    cursor.execute("SELECT escolaridad, COUNT(*) FROM miembros GROUP BY escolaridad")
    escolaridad_data = cursor.fetchall()
    
    labels3 = []
    counts3 = []
    for row in escolaridad_data:
        if row[0] == 'Primaria':
            labels3.append('Primaria')
        elif row[0] == 'Secundaria':
            labels3.append('Secundaria')
        elif row[0] == 'Técnica':
            labels3.append('Técnica')
        elif row[0] == 'Tecnologica':
            labels3.append('Tecnologica')
        elif row[0] == 'Universitaria':
            labels3.append('Universitaria')
        counts3.append(row[1])
    
    # Crear gráfica de torta por escolaridad
    plt.figure(figsize=(4, 4))
    plt.pie(counts3, labels=labels3, autopct=lambda p: f'{p:.1f}%\n({int(p*sum(counts3)/100)})', colors=['Yellow', 'Beige', 'Fuchsia', 'orange', 'purple'])
    plt.title("Distribución por escolaridad")
    
    # Guardar gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    # Codificar gráfica en base64
    grafica_base64_3 = base64.b64encode(buf.getvalue()).decode('utf-8')
   
    #edades y sexo masculino
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 0 AND 14 AND sexo = 'masculino'")
    sexo_edad1 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 15 AND 19 AND sexo = 'masculino'")
    sexo_edad2 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 20 AND 29 AND sexo = 'masculino'")
    sexo_edad3 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 30 AND 39 AND sexo = 'masculino'")
    sexo_edad4 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 40 AND 49 AND sexo = 'masculino'")
    sexo_edad5 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 50 AND 59 AND sexo = 'masculino'")
    sexo_edad6 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 60 AND 74 AND sexo = 'masculino'")
    sexo_edad7 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 75 AND 200 AND sexo = 'masculino'")
    sexo_edad8 = cursor.fetchone()[0]
    
    
   # creamos la grafica por edad y sexo
    x = ["HOMBRES 0-14 años", "HOMBRES 15-19 años", "HOMBRES 20-29 años", "HOMBRES 30-39 años", "HOMBRES 40-49 años", "HOMBRES 50-59 años", "HOMBRES 60-74 años", "HOMBRES 75 años y más"]
    y = [sexo_edad1, sexo_edad2, sexo_edad3, sexo_edad4, sexo_edad5, sexo_edad6, sexo_edad7, sexo_edad8]
    
    

    fig, ax = plt.subplots(figsize=(12, 4))  # Ajustar el tamaño de la figura

# Crear el gráfico de barras
    bars = ax.bar(x=x, height=y)

# Establecer el título del gráfico
    ax.set_title("Gráficos por género masculino y edades")
   
    

# Rotar las etiquetas del eje x para que se vean mejor
    ax.set_xticklabels(x, rotation=10, ha="right", fontsize=6)

# Añadir etiquetas de cantidad encima de cada barra
    for bar in bars:
       yval = bar.get_height()
       ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom')
    
    
     # Guardar gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    # Codificar gráfica en base64
    grafica_base64_4 = base64.b64encode(buf.getvalue()).decode('utf-8')

    
    
    # consulta edad y sexo femenino
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 0 AND 14 AND sexo = 'femenino'")
    sexo_edad9 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 15 AND 19 AND sexo = 'femenino'")
    sexo_edad10 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 20 AND 29 AND sexo = 'femenino'")
    sexo_edad11 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 30 AND 39 AND sexo = 'femenino'")
    sexo_edad12 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 40 AND 49 AND sexo = 'femenino'")
    sexo_edad13 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 50 AND 59 AND sexo = 'femenino'")
    sexo_edad14 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 60 AND 74 AND sexo = 'femenino'")
    sexo_edad15 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*)  FROM  miembros WHERE edad BETWEEN 75 AND 200 AND sexo = 'femenino'")
    sexo_edad16 = cursor.fetchone()[0]
    cursor.close()
     # creamos la grafica por edad y sexo
    x = ["MUJERES 0-14 años", "MUJERES 15-19 años", "MUJERES 20-29 años", "MUJERES 30-39 años", "MUJERES 40-49 años", "MUJERES 50-59 años", "MUJERES 60-74 años", "MUJERES 75 años y más"]
    y = [sexo_edad9, sexo_edad10, sexo_edad11, sexo_edad12, sexo_edad13, sexo_edad14, sexo_edad15, sexo_edad16]
    
    fig, ax = plt.subplots(figsize=(12, 4))  # Ajustar el tamaño de la figura

# Crear el gráfico de barras
    bars = ax.bar(x=x, height=y, color="pink")

# Establecer el título del gráfico
    ax.set_title("Gráficos por género femenino y edades")
    # Ajustar el rango del eje y
    

# Rotar las etiquetas del eje x para que se vean mejor
    ax.set_xticklabels(x, rotation=10, ha="right", fontsize=6)

# Añadir etiquetas de cantidad encima de cada barra
    for bar in bars:
       yval = bar.get_height()
       ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom')
    
    
     # Guardar gráfica en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    # Codificar gráfica en base64
    grafica_base64_5 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template("dashboard.html", miembros=total_usuarios, cantidad_hombres=cantidad_hombres, cantidad_mujeres=cantidad_mujeres, grafica_base64=grafica_base64, grafica_base642=grafica_base64_2, grafica_base64_3=grafica_base64_3, sexo_edad1=sexo_edad1, grafica_base64_4=grafica_base64_4, grafica_base64_5=grafica_base64_5 )
 
if __name__ == '__main__':
    app.run(debug=True)
