PLUGIN_DIR=~/.local/share/gedit/plugins

install:
	mkdir -p $(PLUGIN_DIR)
	cp macropy.py macropy.plugin $(PLUGIN_DIR)

uninstall:
	rm -f $(PLUGIN_DIR)/macropy.py $(PLUGIN_DIR)/macropy.plugin
