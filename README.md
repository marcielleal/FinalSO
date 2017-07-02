## 2 factor Authentication Login Through mail service

#Packages:
GTK+3
python3
libpam-dev

#Instalation

Use instalation.sh with chmod +x for generating mail sender, than change your display manager 

Paste 
[Unit]
Description=My Display Manager
After=systemd-user-sessions.service

[Service]
ExecStart=/path/to/my/display-manager

[Install]
Alias=display-manager.service

in /usr/lib/systemd/system/ systemctl enable my-display-manager.service , hopefuly it will change your display manager

##Warning Sert your email sender First

