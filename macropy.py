#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
  macropy.py 2.0.0
  
  Inspired on first implementation in C for gedit 2 by Sam K. Raju.
  This version for Gedit 3, by Eduardo Romero <eguaio@gmail.com>, Feb 13, 2012.
  Updated for Gedit 3.18, by Leif Martensson <liffem@gmail.com>, Apr 04, 2017.
 
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2, or (at your option)
  any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''

from gi.repository import GObject, Gedit, Gio, GLib

MACRO_SHORTCUT_PLAY = "F4"
MACRO_PLAY_ACCELERATOR = ["<Ctrl><Alt>m", MACRO_SHORTCUT_PLAY]

class macropy(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "Macro"
    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        # Menu item Play macro
        item = Gio.MenuItem.new("Playback recorded macro", "win.macro_play")
        item.set_attribute_value("accel", GLib.Variant("s", MACRO_SHORTCUT_PLAY))
        self.menu_ext.prepend_menu_item(item)
        self.app.set_accels_for_action("win.macro_play", MACRO_PLAY_ACCELERATOR)
        # Menu item Stop record macro
        item = Gio.MenuItem.new("Stop macro recording", "win.macro_record_stop")
        self.menu_ext.prepend_menu_item(item)
        # Menu item Start record macro
        item = Gio.MenuItem.new("Start macro recording", "win.macro_record_start")
        self.menu_ext.prepend_menu_item(item)

    def do_deactivate(self):
        self.app.set_accels_for_action("win.macro_record_start", [])
        self.app.set_accels_for_action("win.macro_record_stop", [])
        self.app.set_accels_for_action("win.macro_play", [])
        self.menu_ext = None

class MacroPyWin(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)
    macro_play = Gio.SimpleAction(name="macro_play")
    macro_record_stop = Gio.SimpleAction(name="macro_record_stop")
    macro_record_start = Gio.SimpleAction(name="macro_record_start")

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings.new("org.gnome.gedit.preferences.editor")

    def do_activate(self):
        self.macro_record_start.connect('activate', self.on_start_macro_recording)
        self.macro_record_stop.connect('activate', self.on_stop_macro_recording)
        self.macro_play.connect('activate', self.on_playback_macro)
        # Enable menu item Start record macro
        self.window.add_action(self.macro_record_start)

    def on_start_macro_recording(self, action, parameter):
        handlers = []
        handler_id = self.window.connect('key-press-event',
                                          self.on_key_press_event)
        handlers.append(handler_id)
        self.window.handlers = handlers
        self.macro = []
        # Disable menu item Play macro
        self.window.remove_action("macro_play")
        # Disable menu item Start record macro
        self.window.remove_action("macro_record_start")
        # Enable menu item Stop record macro
        self.window.add_action(self.macro_record_stop)

    def on_stop_macro_recording(self, action, parameter):
        handlers = self.window.handlers
        for handler_id in handlers:
            self.window.disconnect(handler_id)
        # Disable menu item Stop record macro
        self.window.remove_action("macro_record_stop")
        # Enable menu item Play macro
        self.window.add_action(self.macro_play)
        # Enable menu item Start record macro
        self.window.add_action(self.macro_record_start)

    def on_playback_macro(self, action, data=None):
        for e in self.macro:
            e.put()

    def on_key_press_event(self, window, event):
        self.macro.append(event.copy())

