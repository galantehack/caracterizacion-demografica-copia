from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,  static_folder='static')   # importante para que tome los estilos en la carpeta static

# Configuración de la base de datos MySQL
db = mysql.connector.connect (
    host="localhost",
    user="root",
    password="",
    database="caracterizacion"
)
cursor = db.cursor()

app.secret_key ="miclave"


@app.route('/index')
def index():
   
    return render_template('index.html')
#LISTAR USUARIOS
# Ruta para mostrar los datos de usuario en una tabla HTML
@app.route('/sidebar_miembros')
def listar():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT reconocimiento, nombre, apellido, identidad, sexo, edad, escolaridad, id, direccion, sector FROM miembros")
    usuarios = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_miembros.html', miembros=usuarios)


@app.route("/Agmiembros",  methods=["GET", "POST"])
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
       return redirect(url_for("Agmiembros")) # redirije a la pagina index despues del proceso 
    else:
      return render_template("Agmiembros.html")
  
# ENCUESTA DE TERRITORIO   
@app.route("/territorio",  methods=["GET", "POST"])
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
def lista_territorio():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT a1, a2, a3, a4, a5_1, a5_2, a5_3, a5_4, a5_5, a5_6 , a6, id_encuesta FROM territorio")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_territorio.html', territorio=respuesta)  
  
  
  
  #ENCUESTA IDENTIDAD
@app.route("/identidad",  methods=["GET", "POST"])
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
def lista_identidad():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT b1, b2, 	b3, b4, b5, b6_1, b6_2, b6_3, b6_4, b6_5, b7, id_encuesta FROM identidad")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_identidad.html', identidad=respuesta)



# ENCUESTA DE DESARROLLO
@app.route("/desarrollo", methods=["GET", "POST"])
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
def lista_desarrollo():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT c1_1, c1_2, 	c1_3, c1_4, c1_5, c1_6, c1_7, c1_8, id_encuesta FROM desarrollo")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_desarrollo.html', desarrollo=respuesta)



  
 # encuesta vivienda 
@app.route("/vivienda", methods=["GET", "POST"])
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
def lista_vivienda():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT d1_1, d1_2, d1_3, d1_4, d2_1, d2_2, d2_3, d3_1, d3_2, d3_3, d3_4, d4_1, d4_2, d4_3, d4_4 , d4_5, d4_6, d4_7, d5_1, d5_2, d5_3, d5_4, d5_5, d5_6, d6_1, d6_2, d6_3, d6_4, d6_5, d6_6, d6_7, d7_1, d7_2, d7_3, d7_4, d7_5 , d7_6, d7_7, d7_8, id_encuesta FROM vivienda")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_vivienda.html', vivienda=respuesta)



    
    
  # encuesta saneamiento  
@app.route("/saneamiento", methods=["GET", "POST"])
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
def lista_saneamiento():
    # Ejecutar consulta SQL para obtener los datos de usuario
    cursor.execute("SELECT e1_1, e1_2, e1_3, e1_4, e1_5, e1_6, e1_7, e1_8, e2_1, e2_2, e2_3, e3_1, e3_2, e3_3, e4_1, e4_2, e4_3, e5_1, e5_2, e5_3, e5_4, e6_1, e6_2, e7_1, e7_2, e7_3, e7_4, e7_5, e8, e9_1, e9_2, e9_3, e10_1, e10_2, e10_3, e11_1, e11_2, e11_3, e11_4, e11_5, id_encuesta FROM saneamiento")
    respuesta = cursor.fetchall()

    # Renderizar la plantilla con los datos de usuario
    return render_template('sidebar_saneamiento.html', saneamiento=respuesta)  
  
    
#ruta sidebar
@app.route('/sidebar')
def sidebar():
   
    return render_template('sidebar.html')    
    
    
    
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
           if session ["id_rol"] ==1:
               return render_template('sidebar_territorio.html')
           if session ["id_rol"] ==2:
               return render_template('index.html')
           
        else:
   
           return render_template('login.html', mensaje="credenciales  incorrectas")  
    else:
        return render_template('login.html')    


#ruta registrar login
@app.route("/registrar", methods=["GET", "POST"])
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
def borrar(id_encuesta):
    cursor.execute("DELETE FROM territorio WHERE id_encuesta = %s" ,(id_encuesta,))
    db.commit() 
    return redirect(url_for('territorio'))

# confrmacion de borrado falta

    


  
# LLAMAR DATOS DE TERRITORIO PARA EDITAR 
@app.route("/editar_territorio/<int:id_encuesta>") #se acede a la ruta pasando el parametro id_encuesta
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
    
       
if __name__ == '__main__':
    app.run(debug=True)
