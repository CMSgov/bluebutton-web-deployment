# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment:
    #  Standard documentation
    DOCUMENTATION = r"""
    options: {}
    notes:
      - This module is part of the hitachivantara.vspone_block collection.
    """
    GATEWAY_NOTE = r"""
    options: {}
    notes:
      - Connection type C(gateway) was removed starting from version 3.4.0. Please use an earlier version if you require this connection type.
    """
    DEPRECATED_NOTE = r"""
    options: {}
    notes:
      - This module is deprecated and will be removed in a future release.
    """
    CONNECTION_INFO = r"""
    options:
      connection_info:
        description: Information required to establish a connection to the storage system.
        type: dict
        required: true
        suboptions:
          address:
            description: IP address or hostname of the storage system.
            type: str
            required: true
          username:
            description: Username for authentication. This is a required field.
            type: str
            required: true
          password:
            description: Password for authentication. This is a required field.
            type: str
            required: true

    """
