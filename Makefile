.PHONY: all
all:    rpi-conf

install:
	cp -f rpi-conf.boot.sh /etc/init.d/rpi-conf
	chmod +x /etc/init.d/rpi-conf
	cp -f config.py /etc/rpi_conf/config.py
	chmod +x /etc/rpi_conf/config.py
	cp -f list /etc/rpi_conf/list
	chmod +r /etc/rpi_conf/list
	update-rc.d rpi-conf start runlvl S
	/etc/init.d/rpi-conf start

uninstall:
	-/etc/init.d/rpi-conf stop
	rm /etc/rpi_conf/list
	rm /etc/rpi_conf/config.py
	rm -R /etc/rpi_conf
	rm /etc/init.d/rpi-conf
	update-rc.d rpi-conf remove
