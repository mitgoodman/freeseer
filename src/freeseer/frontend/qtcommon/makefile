ALL:
	@echo "Building Resource files."
	lrelease languages/freeseer.pro
	pyrcc4 -o resource_rc.py resource.qrc
	rm languages/*.qm
	@echo "Resource files created."
