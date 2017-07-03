#!/usr/bin/env python
#encoding:utf-8

import smtplib
from email.mime.text import MIMEText

from time import sleep
from threading import Thread

from random import randint

from os import environ
import sys

sended="Not send"

class SendEmail(Thread):
	def __init__(self, email, senha, assunto, to, texto):
		Thread.__init__(self)		
		self.email=email
		self.senha=senha
		self.assunto=assunto
		self.to=to
		self.texto=texto

	def run(self):
		global sended		
		local=self.email.find("@")
		if(local==-1): 
			sended="Email inválido"+self.email+ " "+self.assunto+ " "+ self.to+ " "+self.texto
		else: 
			local+=1

		server=self.email[local:]
		gmh=None

		if server.lower()=="hotmail.com":
			gmh = smtplib.SMTP("smtp.live.com", 587)
		elif server.lower()=="gmail.com":
			gmh = smtplib.SMTP("smtp.gmail.com", 587)
		elif server.lower()=="bol.com.br":
			gmh = smtplib.SMTP("smtps.bol.com.br", 587)
		elif server.lower()=="outlook.com":
			gmh = smtplib.SMTP("smtp-mail.outlook.com", 587)
		else:
			sended="Email invalido: "+self.email+ " "+self.assunto+ " "+ self.to+ " "+self.texto
			return

		try:
			gmh.starttls()
			gmh.login(self.email, self.senha)
			mail = MIMEText(self.texto)
			mail["To"] = self.to
			mail["Subject"] = self.assunto
			gmh.sendmail(self.email,self.to,mail.as_string())
			gmh.close()
			sended="Enviado"
		except Exception as err:
			sended=err.__str__()+self.email+ " "+self.senha+ " "+self.assunto+ " "+ self.to+ " "+self.texto



def readInformation(key):
	try:
		alogin=open(environ['HOME']+"/.emailInformation","r")
		email=alogin.readline()[:-1]
		pwd=alogin.readline()[:-1]
		to=alogin.readline()[:-1]
		alogin.close()
		sender=SendEmail(email,pwd,"Login Key",to,key)
		sender.start()
		return True
	except:
		print("Poker face")
		return False

readInformation(sys.argv[1])
print(sys.argv[1])