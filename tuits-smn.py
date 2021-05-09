# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:35:48 2021

@author: gaston
"""
###########################################
########Tuits del SMN Argentina############

#################LIBRERIAS#################
import pandas as pd
import tweepy

###########################################
##########ACCESO A API TUITER##############
consumer_key = 'xxxxxxxxxxxxx'
consumer_secret = 'xxxx'
access_token = 'xxxxxxx'
access_token_secret = 'xxxxx'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Creamos un handler con las 2 claves de cliente
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Pasamos los tokens de acceso
auth.set_access_token(access_token, access_token_secret)
# Guardamos la autorizacion a la API en una variable
api = tweepy.API(auth)
#testeo api
api.search(q='CFK')[0].text

###########################################
##########Dataframe con tuits###########
##Creo lista. La lleno con mi data elegida:
#mensaje, fecha de creación en hora twitter, likes, retuits, Media (dict).
tuits = []
for status in tweepy.Cursor(api.user_timeline, screen_name = 'SMN_Alertas', exclude_replies = True, include_rts = False, tweet_mode = 'extended', include_entities=True).items():
	tuits.append([status.full_text, status.created_at, status.favorite_count, status.retweet_count])
#transformo la lista en una dataframe
tuits = pd.DataFrame(tuits, columns=['Text', 'Created at', 'Likes', 'Retweets'])
#Elimino los saltos de linea de cada tuit 
tuits = tuits.replace('\n',' ', regex=True)
#exporto el crudo
tuits.to_csv("tuits-crudo.csv", index = True)

###########################################
########Limpieza de DataFrame###########
#columna Text es partida para obtener 'fecha', 'hora', 'evento' y 'link'.
#Dividir el dataset con el delimitador " "
#Al resultado del split lo ponemos en la primera columna [0] y segunda [1]
texto = tuits['Text'].str.split("Plazo ", n=1, expand=True)
tuits['xaviso']= texto[0]
tuits['xfecha']= texto[1]
nuevo = tuits['xfecha'].str.split(" ", n=1, expand=True)
tuits['Fecha']= nuevo[0]
tuits['xhora']= nuevo[1]
nuevo2 = tuits['xhora'].str.split(" ", n=1, expand=True)
tuits['Hora'] = nuevo2[0]
tuits['xvalidez'] = nuevo2[1]
nuevo3 = tuits['xvalidez'].str.split("emisión ", n=1, expand=True)
tuits['nada']= nuevo3[0]
tuits['xevento']= nuevo3[1]
nuevo4 = tuits['xevento'].str.split("https", n=1, expand=True) #no todos los eventos terminan en punto (.) por tanto se usa http
tuits['Evento']= nuevo4[0]
tuits['Link']= nuevo4[1] 
tuits['https'] = 'https' #creo columna con https como valor contacte
tuits['Link'] = tuits['https'] + tuits['Link']  #concateno columnas y obtengo link entero :D
#borro columnas que no me sirven
tuits.drop(columns =['Text', 'xaviso', 'xfecha', 'xhora', 'xvalidez', 'nada', 'xevento', 'https'], inplace = True)
#exporto el dataset final
tuits.to_csv("poner_fecha-tuits-smn.csv", index = True)

######################