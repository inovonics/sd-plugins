#!/usr/bin/env python

import platform
assert platform.system() == 'Linux', 'I ought to run in Linux'

import os
from subprocess import Popen, PIPE

class TWCProxy( object):
    def __init__( self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig
        self.redisHost = self.rawConfig[ 'TWCProxy'][ 'redis-host']
        self.redisPort = self.rawConfig[ 'TWCProxy'][ 'redis-port']
        self.enable = self.rawConfig[ 'TWCProxy'][ 'enable']

    def run( self):
        if( self.enable == 'True'):
            result = { 'numDevices': 0, 'numClients': 0}
            command = "redis-cli -h %s -p %s KEYS '*'" % ( self.redisHost, self.redisPort)
            process = Popen( command, shell=True, stdout=PIPE, preexec_fn=lambda: os.close( 0))
            stdout, dummy_stderr = process.communicate()
            # This should return a line for each key that exists.
            # If the set is empty, an empty line is returned, so we'll need to check for that
            lines = stdout.splitlines()
            if len( lines) == 1 and lines[ 0] == '':
                result[ 'numDevices'] = 0
                result[ 'numClients'] = 0
            else:
                for line in lines:
                    if 'device' in line:
                        result[ 'numDevices'] = result[ 'numDevices'] + 1
                    elif 'client' in line:
                        result[ 'numClients'] = result[ 'numClients'] + 1
            return result
        else:
            return {}

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    plugin = TWCProxy( None, logging, dict( Redis = dict( host = 'localhost', port = '6380')))
    print( plugin.run())
