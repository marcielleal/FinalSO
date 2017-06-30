#!/usr/bin/env python
#encoding:utf-8

import smtplib
from email.mime.text import MIMEText

from time import sleep
from threading import Thread

from random import randint

from os import environ
class Saida:
	def __init__(self):
		self.string=""
		self.newKey=0

saida=Saida()
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
		global saida		
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
			#saida.newKey+=1
			#saida.string="Nova chave enviada para o email "+self.to[0:5]+"*******"+self.to[self.to.find("@"):]
			sended="Enviado"
		except Exception as err:
			sended=err.__str__()+self.email+ " "+self.senha+ " "+self.assunto+ " "+ self.to+ " "+self.texto



def readInformation(generator):
	try:
		alogin=open(environ['HOME']+"/.emailInformation","r")
		email=alogin.readline()[:-1]
		pwd=alogin.readline()[:-1]
		to=alogin.readline()[:-1]
		alogin.close()
		sender=SendEmail(email,pwd,"Login Key",to,generator.expectedKey)
		sender.start()
		return True
	except:
		print "Poker face"
		return False


class GenerateKey(Thread):
	def __init__(self,time):
		Thread.__init__(self)
		self.end=False
		self.time=time
		self.expectedKey=""
	def run(self):
		while(not self.end):
			self.expectedKey=""
			#for i in range(6):
			self.expectedKey=self.expectedKey+str(randint(100000,999999))
			readInformation(self)
			for i in range(self.time):
				sleep(1)
				if(self.end):
					return None


def sair(retorno, generator):
	generator.end=True
	exit(retorno)

def erro(generator):
	print "Erro inesperado"
	sair(1,generator)

def handler(generator):
	try:
		asw=raw_input('\nVocê quer realmente sair?[S/n] ')
		if(asw=='S' or asw=='s'): sair(1,generator)
	except KeyboardInterrupt:
		return 0
	except Exception as e:
		print e.message
		erro(generator)

ok=False
tempo = 60
#while(not ok):
#	tempo=raw_input("Quanto tempo deseja que sua chave seja válida (em segundos)? ")
#	try:
#		int(tempo)
#		ok=True
#	except:
#		print "Tem certeza que digitou um número? "

generator=GenerateKey(int(tempo))
generator.start()
print("Sua chave será enviada em instantes para o email cadastrado")
sleep(1)

while(True):
	try:
		key=raw_input("Digite a chave: ")
		if(key==generator.expectedKey):
			print "Logado com sucesso!"
			sair(0,generator)
		else:
			print "Chave incorreta!"
	except KeyboardInterrupt:
		while (handler(generator)==0):
			pass
	except Exception as e:
		print e.message
		erro(generator)
