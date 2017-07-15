#encoding:utf-8
from os import environ

bash=None
try:
	bash=open(environ['HOME']+"/.bash_login","a")
except:
	bash=open(environ['HOME']+"/.bash_login","w")

bash.write("""
python validation.py
if [ $? -eq 1 ]; then
    exit
fi
""")
bash.close()

a=open(environ['HOME']+"/.emailInformation","w")
a.write("email\n")
a.write("senha\n")
to=raw_input("Digite o email para receber suas chaves")
a.write(to+"\n")
a.close()
