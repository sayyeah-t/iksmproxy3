APPNAME=iksmproxy3
CONFDIR=/etc/iksmproxy3
PYTHON=python3.7
INSTALLDIR=/opt
SERVICEFILEDIR=/usr/lib/systemd/system
BASECONFDIR=./etc/iksmproxy3
BASESERVICEFILEDIR=./etc/systemd/system
DEB_WORKDIR=package

all: package
install:
	sudo mkdir -p $(CONFDIR)
	if [ ! -e $(CONFDIR)/$(APPNAME).conf ]; then\
		sudo cp $(BASECONFDIR)/$(APPNAME).conf $(CONFDIR)/;\
		sudo cp $(BASECONFDIR)/print_cookie.py $(CONFDIR)/;\
		sudo cp $(BASESERVICEFILEDIR)/$(APPNAME).service $(SERVICEFILEDIR)/;\
		virtualenv -p $(PYTHON) ./tmp/$(APPNAME);\
		sudo ./tmp/$(APPNAME)/bin/python setup sdist;\
		sudo ./tmp/$(APPNAME)/bin/pip install dist/$(APPNAME)*;\
		sudo cp -r ./tmp/$(APPNAME) $(INSTALLDIR);\
		sudo rm -rf ./tmp;\
	fi
uninstall:
	sudo systemctl stop iksmproxy3
	sudo rm -f $(INSTALLDIR)/$(APPNAME)
	sudo rm -f $(CONFDIR)
	sudo rm -f $(SERVICEFILEDIR)/$(APPNAME).service
package:
	mkdir -p $(DEB_WORKDIR)$(INSTALLDIR)
	virtualenv -p $(PYTHON) $(DEB_WORKDIR)$(INSTALLDIR)/$(APPNAME)
	$(DEB_WORKDIR)$(INSTALLDIR)/$(APPNAME)/bin/python setup.py sdist
	$(DEB_WORKDIR)$(INSTALLDIR)/$(APPNAME)/bin/pip install dist/$(APPNAME)*
	mkdir -p $(DEB_WORKDIR)$(CONFDIR)
	cp $(BASECONFDIR)/$(APPNAME).conf $(DEB_WORKDIR)$(CONFDIR)/_$(APPNAME).conf
	cp $(BASECONFDIR)/print_cookie.py $(DEB_WORKDIR)$(CONFDIR)/
	mkdir -p $(DEB_WORKDIR)$(SERVICEFILEDIR)
	cp $(BASESERVICEFILEDIR)/$(APPNAME).service $(DEB_WORKDIR)$(SERVICEFILEDIR)
	cp -r DEBIAN $(DEB_WORKDIR)
	fakeroot dpkg-deb --build $(DEB_WORKDIR) .
	rm -rf $(DEB_WORKDIR)
	rm -rf ./dist
