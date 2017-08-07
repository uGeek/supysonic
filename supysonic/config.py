# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# This file is part of Supysonic.
# Supysonic is a Python implementation of the Subsonic server API.
#
# Copyright (C) 2013-2017 Alban 'spl0k' Féron
#                    2017 Óscar García Amor
#
# Distributed under terms of the GNU AGPLv3 license.

from ConfigParser import ConfigParser, NoOptionError, NoSectionError

import mimetypes
import os
import tempfile

class Config(object):
    """
    Config object to work with config file
    """
    def __init__(self):
        # Seek for standard locations
        config_file = [
                'supysonic.conf',
                os.path.expanduser('~/.config/supysonic/supysonic.conf'),
                os.path.expanduser('~/.supysonic'),
                '/etc/supysonic'
                ]
        self.config = ConfigParser({ 'cache_dir': os.path.join(tempfile.gettempdir(), 'supysonic') })
        # Try read config file or raise error
        try:
            self.config.read(config_file)
        except Exception as e:
            err = 'Config file is corrupted.\n{0}'.format(e)
            raise SystemExit(err)

    def check(self):
        """
        Checks the config for mandatory fields
        """
        try:
            self.config.get('base', 'database_uri')
        except (NoSectionError, NoOptionError):
            raise SystemExit('No database URI set')
        return True

    def get(self, section, option):
        """
        Returns a config option value from config file

        :param section: section where the option is stored
        :param option: option name
        :return: a config option value
        :rtype: string
        """
        try:
            return self.config.get(section, option)
        except (NoSectionError, NoOptionError):
            return None

    def get_mime(self, extension):
        """
        Returns mimetype of an extension based on config file

        :param extension: extension string
        :return: mimetype
        :rtype: string
        """
        guessed_mime = mimetypes.guess_type('dummy.' + extension, False)[0]
        config_mime = self.get('mimetypes', extension)
        default_mime = 'application/octet-stream'
        return guessed_mime or config_mime or default_mime
