# import main Flask class and request object
from flask import Flask, request , jsonify
import json
import os
from flask_apscheduler import APScheduler
from datetime import date
import smtplib
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

####################################################################
######################  CLASES  ####################################
####################################################################
class NUC:
    


    def __init__(self, name,ip,linea):
        self.Name = name
        self.IP = ip
        self.Linea = linea
        self.State = "NotWorking"
        self.Warnings = 0
        self.Notified = False
        self.Color = 'red'
        

    def ChangeState(self,state):
        self.State=state
    def ChangeWarnings(self,warnings):
        self.Warnings=warnings
    def ChangeNotified(self,notified):
        self.Notified=notified



####################################################################
####################  Funciones y Variables  #######################
####################################################################


#NucNames = ['ST0042','ST0043','ST0041','SSA0956','SSA2211','SSA2210','SSA2201','ST0023','ST0024','ST0025','ST0026','ST0010','ST0007','ST0008','ST0011','ST0019','ST0017','ST0020','ST0056','ST0058','ST0057','ST0045','ST0044','ST0040']

#NucIps = ['10.251.231.238','10.251.231.246','10.251.231.247','10.251.231.174','10.251.231.179','10.251.231.172','10.251.231.171','10.251.231.228','10.251.231.225','10.251.231.226','10.251.231.227','10.251.231.178','10.251.231.176','10.251.231.175','10.251.231.177','10.251.231.79','10.251.231.81','10.251.231.78','10.251.231.82','10.251.231.83','10.251.231.84','10.251.231.243','10.251.231.241','10.251.231.240']

NucNames = ['ST0043','ST0041','SSA0956','SSA2211','SSA2210','SSA2201','ST0023','ST0024','ST0025','ST0026','ST0010','ST0007','ST0008','ST0011','ST0019','ST0017','ST0020','ST0056','ST0058','ST0057','ST0045','ST0044','ST0040']

NucIps = ['10.251.231.246','10.251.231.247','10.251.231.174','10.251.231.179','10.251.231.172','10.251.231.171','10.251.231.228','10.251.231.225','10.251.231.226','10.251.231.227','10.251.231.178','10.251.231.176','10.251.231.175','10.251.231.177','10.251.231.79','10.251.231.81','10.251.231.78','10.251.231.82','10.251.231.83','10.251.231.84','10.251.231.243','10.251.231.241','10.251.231.240']


#NucNames = ['ST0056','ST0058','ST0057','ST0010','ST0007','ST0008','ST0011']

#NucIps = ['10.251.231.82','10.251.231.83','10.251.231.84','10.251.231.178','10.251.231.176','10.251.231.175','10.251.231.177']

NucLine = ['Celda Kapp','Celda Kapp','Celda Kapp','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1','Blando G1']

#NucNames = ['ST0056']

#NucIps = ['10.251.231.87']

ListOfNucs = []

def obj_dict(obj):
    return obj.__dict__

def CreateListOfNucs ():
    global NucNames
    global ListOfNucs
    global NucIps
    global NucLine
    i=0
    for name in NucNames:
        nuc = NUC(name,NucIps[i],NucLine[i])
        ListOfNucs.append(nuc)
        i=i+1

CreateListOfNucs()

def VerifyState ():
    global ListOfNucs
    for item in ListOfNucs:
        if(item.State == 'NotWorking' and item.Warnings == 5 and item.Notified == False):
                hostname = item.IP #example
                response = os.system("ping " + hostname)
                if response == 0:
                  Encendida=True
                  item.Color='yellow'
                else:
                  Encendida=False
                  item.Color='red'
                i = Enviar_Email(item,Encendida)
                print(item.Name)
                print(item.IP)
                if(i):
                    item.ChangeNotified(True)
        else:
            item.ChangeWarnings(item.Warnings + 1)
        if(item.State == 'Working'):
            item.ChangeNotified(False)
            item.Warnings = 0
            item.Color='green'
        item.State = "NotWorking"


def Enviar_Email(nuc,Encendida):
    # Iniciamos los parámetros del script
    remitente = 'Chronos@scania.com'
    destinatarios = ['santiagocuozzo2@gmail.com']
    asunto = 'Chronos Cerrado!!!!!!!'
    if(Encendida):
        cuerpo = 'La Nuc con Nombre ' + nuc.Name + ' con la direccion IP:'+ nuc.IP + ' esta sin chronos abierto'
    else:
        cuerpo = 'La Nuc con Nombre ' + nuc.Name + ' con la direccion IP:'+ nuc.IP + ' esta sin chronos abierto Y ADEMAS NO RESPONDE AL PING!!!!!!!'
    ##fecha=get_fecha()
    ##ruta_adjunto = 'C:/Users/pbertini/Desktop/Proyecto-Puente-Grua/'+Camion[2]+"-"+fecha+'.pdf'
    ##nombre_adjunto = Camion[2]+"-"+fecha+'.pdf'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    ##archivo_adjunto = open(ruta_adjunto, 'rb')
    
    # Creamos un objeto MIME base
    #adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    ##adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    #encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    #adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    #mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    try:



        #sesion_smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
        sesion_smtp = smtplib.SMTP('10.33.8.168', 25,'scania.com')
        # Ciframos la conexión
        #sesion_smtp.starttls()
        # Iniciamos sesión en el servidor
        #sesion_smtp.login('santiagocuozzo@hotmail.com','Elnote7explota')
        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()
        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        # Cerramos la conexión
        sesion_smtp.quit()




        print("se pudo enviar el email a la nuc "+ nuc.Name+' con la direccion IP:'+nuc.IP)
        return True
    except:
        print("no se pudo enviar el email a la nuc "+ nuc.Name+' con la direccion IP:'+nuc.IP)
        return False

####################################################################
####################  create the Flask app   #######################
####################################################################

app = Flask(__name__)
scheduler=APScheduler()
@app.route('/iamworking',methods=['POST'])
def iamworking():
    global ListOfNucs
    if request.method == 'POST':
        request_data = request.get_json()
        Machine = request_data['Machine']
        for item in ListOfNucs:
            if(item.Name == Machine):
                item.ChangeState("Working")
                item.Color = 'green'
                
        try:
            return jsonify(Status = "Recived")
        except:
            return

@app.route('/whoisworking',methods=['GET'])
def whoisworking():
    if request.method == 'GET':
        global ListOfNucs
        if request.method == 'GET':
            json_string = json.dumps(ListOfNucs, default=obj_dict)
            headers = {        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",}
            return json_string, 200,headers


if __name__ == '__main__':
    #scheduler.add_job(id = "Scheduled Task", func=VerifyState, trigger="interval", seconds=60)
    #scheduler.start()
    app.run(host='127.0.0.1',port=5000, use_reloader=False)

