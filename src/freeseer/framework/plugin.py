#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import ConfigParser
import logging
import os
import functools

import pygst
pygst.require("0.10")
import gst

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.IPlugin import IPlugin
from PyQt4 import QtCore, QtGui

class PluginManager(QtCore.QObject):
    '''
    @signal pluginActivated(plugin_name, plugin_category)
    Emitted when a plugin is activated.
    
    @signal pluginDectivated(plugin_name, plugin_category)
    Emitted when a plugin is deactivated.
    '''
    
    def __init__(self, configdir):
        QtCore.QObject.__init__(self)
        
        self.firstrun = False
        plugman = PluginManagerSingleton.get()
        
        self.configdir = configdir
        self.configfile = os.path.abspath("%s/plugin.conf" % self.configdir)
        
        self.config = ConfigParser.ConfigParser()
        self.load()
        self.plugmanc = ConfigurablePluginManager(self.config, self, plugman)
        
        # Get the path where the installed plugins are located on systems where
        # freeseer is installed.
        pluginpath = "%s/../plugins" % os.path.dirname(os.path.abspath(__file__))
        
        self.plugmanc.setPluginPlaces([pluginpath, 
                                       os.path.expanduser("~/.freeseer/plugins"), 
                                       "freeseer/plugins"])
        self.plugmanc.setCategoriesFilter({
            "AudioInput" : IAudioInput,
            "AudioMixer" : IAudioMixer,
            "VideoInput" : IVideoInput,
            "VideoMixer" : IVideoMixer,
            "Output" : IOutput})
        self.plugmanc.collectPlugins()
        
        # If config was corrupt or did not exist, reset default plugins.
        if self.firstrun == True:
            self.set_default_plugins()
            
        for plugin in self.plugmanc.getAllPlugins():
            plugin.plugin_object.set_plugman(self)
            
        logging.debug("Plugin manager initialized.")
        
    def __call__(self):
        pass
    
    def load(self):
        try:
            self.config.readfp(open(self.configfile))
        # Config file does not exist, create a default
        except IOError:
            logging.debug("First run scenario detected. Creating new configuration files.")
            self.firstrun = True # If config was corrupt or did not exist, reset defaults.
            self.save()
            return
        
    def set_default_plugins(self):
        """
        Default the passthrough mixers and ogg output plugins.
        """
        
        self.activate_plugin("Audio Passthrough", "AudioMixer")
        self.activate_plugin("Audio Test Source", "AudioInput")
        self.plugmanc.registerOptionFromPlugin("AudioMixer", "Audio Passthrough-0", "Audio Input", "Audio Test Source")
            
        self.activate_plugin("Video Passthrough", "VideoMixer")
        self.activate_plugin("Video Test Source", "VideoInput")
        self.plugmanc.registerOptionFromPlugin("VideoMixer", "Video Passthrough-0", "Video Input", "Video Test Source")
        self.activate_plugin("Ogg Output", "Output")
        logging.debug("Default plugins activated.")
        
    def _activate_default_metadata_plugins(self):
        self.activate_plugin("Filename Parser", IMetadataReader.CATEGORY)
        self.activate_plugin("GstDiscoverer Parser", IMetadataReader.CATEGORY)
        self.activate_plugin("os.stat Parser", IMetadataReader.CATEGORY)
        
    def save(self):
        with open(self.configfile, 'w') as configfile:
            self.config.write(configfile)
        
    def activate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.activatePluginByName(plugin_name, plugin_category, True)
        self.save()
        self.plugin_activated.emit(plugin_name, plugin_category)
        logging.debug("Plugin %s activated." % plugin_name)
        
    def deactivate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.deactivatePluginByName(plugin_name, plugin_category, True)
        self.save()
        self.plugin_deactivated.emit(plugin_name, plugin_category)
        logging.debug("Plugin %s deactivated." % plugin_name)
        
    # the arguments are plugin_name, plugin_category
    plugin_activated = QtCore.pyqtSignal(
            "QString", "QString", name="pluginActivated")
    plugin_deactivated = QtCore.pyqtSignal(
            "QString", "QString", name="pluginDectivated")
    

class IBackendPlugin(IPlugin):
    instance = 0
    name = None
    widget = None
    category = "Undefined"
    
    def __init__(self):
        IPlugin.__init__(self)
    
    def get_name(self):
        return self.name
    
    def get_config_name(self):
        return "%s-%s" % (self.name, self.instance)
    
    def load_config(self, plugman):
        pass
    
    def set_plugman(self, plugman):
        self.plugman = plugman
        
    def set_instance(self, instance=0):
        self.instance = instance
        
    def set_gui(self, gui):
        self.gui = gui
    
    def get_dialog(self):
        widget = self.get_widget()
        if widget is not None:
            self.gui.show_plugin_widget_dialog(widget)
            self.widget_load_config(self.plugman)
    
    def get_widget(self):
        """
        Implement this method to return the settings widget (Qt based).
        Used by Freeseer configtool 
        """
        return None
    
    def widget_load_config(self, plugman):
        """
        Implement this when using a plugin widget. This function should be used
        to load any required configurations for the plugin widget.
        """
        pass
    
    # CLI Functions
    
    """
    These 3 following methods must be implemented if it's expected from a plugin to be
    handled through CLI
    """    
    def get_properties(self):
        raise NotImplementedError("Plugins supported by CLI should implement this!")
    
    def get_property_value(self, property):
        raise NotImplementedError("Plugins supported by CLI should implement this!")
    
    def set_property_value(self, property, value):
        raise NotImplementedError("Plugins supported by CLI should implement this!")

class IAudioInput(IBackendPlugin):
    CATEGORY = "AudioInput"
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_audioinput_bin(self):
        raise NotImplementedError
    
class IAudioMixer(IBackendPlugin):
    CATEGORY = "AudioMixer"
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_audiomixer_bin(self):
        raise NotImplementedError
    
    def get_inputs(self):
        """
        Returns a list of inputs the that the audio mixer needs
        in order to initialize it's pipelines.
        
        This should be used so that the code that calls it can
        gather the required inputs before calling load_inputs().
        """
        raise NotImplementedError
    
    def load_inputs(self, player, mixer, inputs):
        """
        This method is responsible for loading the inputs needed
        by the mixer.
        """
        raise NotImplementedError
    
class IVideoInput(IBackendPlugin):
    CATEGORY = "VideoInput"
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_videoinput_bin(self):
        """
        Returns the Gstreamer Bin for the video input plugin.
        MUST be overridded when creating a video input plugin.
        """
        raise NotImplementedError
    
class IVideoMixer(IBackendPlugin):
    CATEGORY = "VideoMixer"
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_videomixer_bin(self):
        """
        Returns the Gstreamer Bin for the video mixer plugin.
        MUST be overridded when creating a video mixer plugin.
        """
        raise NotImplementedError
    
    def get_inputs(self):
        """
        Returns a list of inputs the that the video mixer needs
        in order to initialize it's pipelines.
        
        This should be used so that the code that calls it can
        gather the required inputs before calling load_inputs().
        """
        raise NotImplementedError
    
    def load_inputs(self, player, mixer, inputs):
        """
        This method is responsible for loading the inputs needed
        by the mixer.
        """
        raise NotImplementedError

class IOutput(IBackendPlugin):
    #
    # static variables
    #
    CATEGORY = "Output"
    
    # recordto
    FILE = 0
    STREAM = 1
    OTHER = 2
    
    # type
    AUDIO = 0
    VIDEO = 1
    BOTH = 2
    
    #
    # variables
    #
    recordto = None # recordto: FILE, STREAM, OTHER
    type = None # Types: AUDIO, VIDEO, BOTH
    extension = None
    location = None
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_recordto(self):
        return self.recordto
    
    def get_type(self):
        return self.type
    
    def get_output_bin(self, audio=True, video=True, metadata=None):
        """
        Returns the Gstreamer Bin for the output plugin.
        MUST be overridded when creating an output plugin.
        """
        raise NotImplementedError
    
    def get_extension(self):
        return self.extension
    
    def set_recording_location(self, location):
        self.location = location

    def set_metadata(self, data):
        """
        Set the metadata if supported by Output plugin. 
        """
        pass

#
# Removing Video Uploader code from Freeseer framework core
# Video Uploader should be redesigned as a separate tool not adding
# any additional requirements to main Freeseer UIs
#

#class IMetadataReaderBase(QtCore.QObject):
#    def __init__(self):
#        QtCore.QObject.__init__(self)
#    
#    class header(object):
#        '''
#        defines the data that is being depicted by the metadata
#        @ivar name:Human readable name of the field
#        @ivar type:expected type (not used)
#        @ivar position:where the field should go in relation to the others
#                        (we sort by this value when populating the headers)
#        @ivar visible:if the field is currently visible (get from settings)
#        '''
#        # todo: load visibility from settings.
#        def __init__(self, name, typ=None, pos=0, visible=True):
#            self.name = name
#            self.type = typ
#            self.position = pos
#            self.visible = visible
#            
#    def retrieve_metadata(self, filepath):
#        raise NotImplementedError
#    
#    def retrieve_metadata_batch(self, filepath_list):
#        raise NotImplementedError
#    
#    def get_fields(self):
#        raise NotImplementedError
#            
#    field_visibility_changed = QtCore.pyqtSignal(
#            "QString", bool, name="fieldVisibilityChanged")
#
#strtobool = lambda s:bool(s) and s != str(False)
#class IMetadataReader(IBackendPlugin, IMetadataReaderBase):
#    ## abstract class members/methods
#    # this dict should be of type {string:header}
#    # Don't use externally! use get_fields() instead
#    fields_provided = {}
#    
#    def retrieve_metadata_internal(self, filepath):
#        raise NotImplementedError
#    
#    def retrieve_metadata_batch_begin(self):
#        '''
#        Optional abstract method
#        '''
#    
#    def retrieve_metadata_batch_end(self):
#        '''
#        Optional abstract method
#        '''
#    
#    ## concrete class members/methods
#    CATEGORY = "Metadata"
#    
#    def __init__(self):
#        IBackendPlugin.__init__(self)
#        IMetadataReaderBase.__init__(self)
#        self.checkboxes = {}
#        self.fields = self._get_fields()
#    
#    def retrieve_metadata(self, filepath):
#        '''
#        @return: Dict of field: data
#        '''
#        n = type(self).__name__
#        return dict((".".join((n,k)),v) for (k,v) in 
#                    self.retrieve_metadata_internal(filepath).iteritems())
#    
#    def retrieve_metadata_batch(self, filepath_list):
#        self.retrieve_metadata_batch_begin()
#        for filepath in filepath_list:
#            yield self.retrieve_metadata(filepath)
#        self.retrieve_metadata_batch_end()
#    
#    def load_config(self, plugman):
#        self.plugman = plugman
#        for key in self.fields_provided.iterkeys():
#            try:
#                self.set_visible(key, plugman.plugmanc.readOptionFromPlugin(
#                        self.CATEGORY, self.name, key))
#            except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
#                plugman.plugmanc.registerOptionFromPlugin(
#                        self.CATEGORY, self.name, key, 
#                        self.fields[self.localtoglobal(key)].visible)
##                self.set_visible(key, True)
#    
#    def set_visible(self, option_name, option_value):
#        self.plugman.plugmanc.registerOptionFromPlugin(
#                self.CATEGORY, self.name, option_name, str(option_value))
#        self.plugman.save()
#        self.fields[self.localtoglobal(option_name)].visible = strtobool(option_value)
#        # dispatch signal to notify any slots of changes
##        self.field_visibility_changed.emit(option_name, option_value)
#        self.field_visibility_changed.emit(
#                self.localtoglobal(option_name),
#                strtobool(option_value))
#        
##    globaltolocal = lambda field_id: field_id.split(".",1)[1]
#    globaltolocal = lambda self, field_id: field_id[len(type(self).__name__)+1:]
#    localtoglobal = lambda self, option_name: ".".join((type(self).__name__, option_name))
#    
#    def get_widget(self):
#        if self.widget is None:
#            self.widget = QtGui.QWidget()
#            
#            layout = QtGui.QVBoxLayout(self.widget)
#            self.widget.setLayout(layout)
#            
#            for key in self.fields_provided:
#                cbox = QtGui.QCheckBox(
#                        self.fields_provided[key].name, self.widget)
#                layout.addWidget(cbox)
#                cbox.toggled.connect(functools.partial(self.set_visible, key))
#                self.checkboxes[key] = cbox
#            
#        return self.widget
#    
#    def widget_load_config(self, plugman):
#        self.load_config(plugman)
#        for key in self.fields_provided:
#            checked = self.plugman.plugmanc.readOptionFromPlugin(
#                self.CATEGORY, self.name, key)
#            self.checkboxes[key].setChecked(strtobool(checked))
#    
#    @classmethod
#    def _get_fields(cls):
#        '''
#        ensures that the field dictionary is unique
#        @return: Dict of field: IMetadataReader.header
#        '''
#        return dict((".".join((cls.__name__,k)),v) for (k,v) in cls.fields_provided.iteritems())
#        #python 2.7+ only
##        return {".".join((cls.__name__,k)) : v for k in cls.fields_provided.iteritems()} 
#    def get_fields(self):
#        return self.fields

    # the following commented code precaches unique names for fields
#    ufields_provided = {}
#    @classmethod
#    def get_fields(cls):
#        '''
#        @return: Dict of field: header
#        '''
#        return cls.ufields_provided
#    
#    @staticmethod
#    def setup_ufields_on_subclasses(name, bases, attrs):
#        cls = type(name, bases, attrs)
#        
#        cls.ufields_provided = dict((".".join((name,k)),v) for (k,v) in cls.fields_provided)
#        #cls.ufields_provided = {".".join((name,k)) : v for k in cls.fields_provided} #python 2.7+ only
#    __metaclass__ = setup_ufields_on_subclasses
