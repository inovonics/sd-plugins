#!/usr/bin/env python

import requests
import csv

class HAproxy:
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig
        self.host = self.rawConfig[ 'HAproxy'][ 'host']
        self.port = self.rawConfig[ 'HAproxy'][ 'port']
        self.enable = self.rawConfig[ 'HAproxy'][ 'enable']
    
    def run(self):
        if( self.enable == 'True'):
            results = {}
            url = "http://%s:%s/;csv" % ( self.host, self.port)
            resp = requests.get( url)
            haproxy_reply = csv.DictReader( resp.content.splitlines())
            
            for row in haproxy_reply:
                results[ "%s_%s_rate" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'rate']
                results[ "%s_%s_rate_max" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'rate_max']
                results[ "%s_%s_scur" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'scur']
                results[ "%s_%s_smax" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'smax']
                results[ "%s_%s_stot" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'stot']
                results[ "%s_%s_qcur" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'qcur']
                results[ "%s_%s_qmax" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'qmax']
                results[ "%s_%s_bin" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'bin']
                results[ "%s_%s_bout" % ( row[ '# pxname'], row[ 'svname'])] = row[ 'bout']
            return results
        else:
            return {}

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    plugin = HAproxy( None, logging, dict( HAproxy = dict( host = 'localhost', port = '8080')))
    print( plugin.run())

