#!/usr/bin/env python
"""
Copyright 2014 (c) by Inovonics Corporation, Inc. All Rights Reserved.

This is a Server Density Plugin to monitor the RabbitMQ cluster.
Daniel Williams <dwilliams@inovonics.com>
"""

import requests
import json

class RabbitMQ:
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig
        self.host = self.rawConfig[ 'RabbitMQ'][ 'host']
        self.port = self.rawConfig[ 'RabbitMQ'][ 'port']
        self.username = 'guest'
        self.password = 'guest'
    
    def run(self):
        results = {}
        url = "http://%s:%s/api/overview" % ( self.host, self.port)
        resp = requests.get( url, auth = ( self.username, self.password))
        rabbit_mq_reply = json.loads( resp.content)
        
        results[ 'msg_pub_rate'] = rabbit_mq_reply[ 'message_stats'][ 'publish_details'][ 'rate']
        results[ 'msg_ack_rate'] = rabbit_mq_reply[ 'message_stats'][ 'ack_details'][ 'rate']
        results[ 'msg_dlvg_rate'] = rabbit_mq_reply[ 'message_stats'][ 'deliver_get_details'][ 'rate']
        results[ 'msg_dlv_rate'] = rabbit_mq_reply[ 'message_stats'][ 'deliver_details'][ 'rate']
        
        results[ 'q_msg_rate'] = rabbit_mq_reply[ 'queue_totals'][ 'messages_details'][ 'rate']
        results[ 'q_msg_rdy_rate'] = rabbit_mq_reply[ 'queue_totals'][ 'messages_ready_details'][ 'rate']
        results[ 'q_msg_unack_rate'] = rabbit_mq_reply[ 'queue_totals'][ 'messages_unacknowledged_details'][ 'rate']
        
        results[ 'obj_consumers'] = rabbit_mq_reply[ 'object_totals'][ 'consumers']
        results[ 'obj_queues'] = rabbit_mq_reply[ 'object_totals'][ 'queues']
        results[ 'obj_exchanges'] = rabbit_mq_reply[ 'object_totals'][ 'exchanges']
        results[ 'obj_connections'] = rabbit_mq_reply[ 'object_totals'][ 'connections']
        results[ 'obj_channels'] = rabbit_mq_reply[ 'object_totals'][ 'channels']
        
        results[ 'num_listeners'] = len( rabbit_mq_reply[ 'listeners'])
        
        return results

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    plugin = RabbitMQ( None, logging, dict( RabbitMQ = dict( host = 'localhost', port = '15672')))
    print( plugin.run())

