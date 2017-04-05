PLUGIN_DIR=~/.local/share/gedit/plugins/macropy

install:
	mkdir -p $(PLUGIN_DIR)
	cp macropy.py macropy.plugin $(PLUGIN_DIR)

uninstall:
	rm -rf $(PLUGIN_DIR)
