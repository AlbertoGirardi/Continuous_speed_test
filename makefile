#restarts the service and pulls git changes

r:  
	git pull
	sudo systemctl daemon-reload
	sudo systemctl restart css.service

start:
	git pull
	sudo systemctl daemon-reload
	sudo systemctl enable css.service
	sudo systemctl start css.service
