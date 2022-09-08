import tkinter as tk
from tkinter import Button, Label
from playsound import playsound
import threading
import cv2
from mytools import miFecha



def alarma():
    cap = cv2.VideoCapture("direccion de la camara o video .mp4 / ip")

    #his   tamaño del historico
    # muestra de pixeles para capturar 
    # detectShadows detecta sombras o no 


    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc  = cv2.VideoWriter_fourcc(*'mp4v')
    name_video = "./grabaciones/Vid_{}.mp4".format(miFecha())

    grabador = cv2.VideoWriter(name_video, fourcc, 30, (w,h) )

    #mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

    #opencCL desactivar
    cv2.ocl.setUseOpenCL(False)

    audio_file = "./buu.mp3"
    while True:
        ret, cam = cap.read()
        ret, cam2 = cap.read()
        if not ret:
            break

        diff = cv2.absdiff(cam, cam2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20,255,cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contornos, _ =  cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #verificar los contornos en cam
        #cv2.drawContours(cam, contornos, -1, (0,0,255), 2)
        #dibujar rectangulo en los contornos
        for i in contornos:
            
            if cv2.contourArea(i) < 8918:
                continue

            if cv2.contourArea(i) >= 8918:
                #
                (x,y,w,h) = cv2.boundingRect(i)
                #dibujamos rectangulo en la imagen o video
                cv2.rectangle(cam, (x,y) , (x+w, y+h), (0,0,255),2)
                cv2.putText(cam, '{}'.format('Movimiento') , (x,y-5), 1,1.3, (0,0,255) , 1, cv2.LINE_AA)
                grabador.write(cam)
                
                    #winsound.PlaySound("bu.wav", winsound.SND_ASYNC)
            threading.Thread(target=playsound, args=(audio_file,False), daemon=True).start()
        #mostramos la camara, mascara y contornos
        #cv2.imshow('Contornos', contornos)

        #cv2.imshow("Diff", diff)
        # igual a diff en negro          cv2.imshow("Grises", gray)
        #cv2.imshow("Dilated", dilated)
        cv2.imshow("nuevi", cam)
        
        #igual a dilated menos rayado       cv2.imshow("Dibujo", thresh)
        #cv2.imshow('Sonido' , mascara)
        #verificar los contornos en cam
        #cv2.drawContours(cam, contornos, -1, (0,0,255), 2)

        #buscamos los contornos
        #con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

        k = cv2.waitKey(5)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()



def tk_pantalla_app():
    #hacer global una variable para usarla en todo el codigo
    global miPantalla
    miPantalla = tk.Tk()

    #tamaño
    
    miPantalla.geometry("500x250")

    miPantalla.title("Camara de seguridad YeAraya")
    Label(text ="Hola Yeisson", bg ="gray", width="300", height= "2", font= ("Verdana", 13)).pack()
#espacio
    Label( miPantalla, text="").pack()

    
#variable con el imput

#
#Hacer input de ip de camara , puerto


    Button(text="Iniciar con Alarma", height="2", width="30", command= alarma).pack()


    #creamos espacio
    
    Label( miPantalla, text="").pack()


#terminar programa

    miPantalla.mainloop()

tk_pantalla_app()
