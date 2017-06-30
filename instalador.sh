if [ -d "$HOME/.bash_login" ] ; then
	cp $HOME/.bash_login $HOME/cpbash_login
	cp validation.py $HOME/validation.py
fi
python instalador.py
python validation.py
if [ $? -eq 1 ]; then
	rm $HOME/.bash_login
	mv $HOME/.cpbash_login $HOME/.bash_login
   	rm $HOME/.emailInformation
   	rm validation.py
else
	echo "Email cadastrado com sucesso!"
fi
