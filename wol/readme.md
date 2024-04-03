Python web application with a simple interface where users can enter a secret string and then trigger a Wake-on-LAN command.

pip install wakeonlan

copy wol.service to /etc/systemd/system/ directory

sudo systemctl daemon-reload
sudo systemctl enable wol.service
sudo systemctl start wol.service
