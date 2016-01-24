#!/usr/bin/env python
"""
Copyright 2014 (c) by Inovonics Corporation, Inc. All Rights Reserved.

This is a Server Density Plugin to monitor the Redis servers
Daniel Williams <dwilliams@inovonics.com>
"""

import platform
assert platform.system() == 'Linux', 'I ought to run in Linux'

import os
from subprocess import Popen, PIPE

class Redis( object):
    def __init__( self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig
        self.host = self.rawConfig[ 'Redis'][ 'host']
        self.port = self.rawConfig[ 'Redis'][ 'port']

    def run( self):
        result = {}
        command = "redis-cli -h %s -p %s INFO" % ( self.host, self.port)
        process = Popen( command, shell=True, stdout=PIPE, preexec_fn=lambda: os.close( 0))
        stdout, dummy_stderr = process.communicate()
        for line in stdout.splitlines():
            if ':' in line:
                key, val = line.split( ':')
                if ',' in val:
                    for subline in val.split( ','):
                        subkey, subval = subline.split( '=')
                        compkey = "%s_%s" % ( key, subkey)
                        result[ compkey] = subval
                else:
                    result[ key] = val
        return result

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    plugin = Redis( None, logging, dict( Redis = dict( host = 'localhost', port = '6380')))
    print( plugin.run())

