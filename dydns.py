#!/usr/bin/env python

import os
import argparse
import configparser
import logging
import requests
import sys
import time

logger = logging.getLogger('dyndns')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def getMyIP():

    try:

        ip =  requests.get('https://api.ipify.org').text

        return ip

    except Exception as e:
        logger.error("Error obtaining the public ip address")


def mainProcess(config):
    """ Main process loop """

    while True:
        logger.debug("Checking for IP Address Change")
        updateIP(config)

        time.sleep(600)


def updateIP(config):
    """ UPdates the IP Address"""

    ip = getMyIP()
    oldip = ""

    logger.debug("Observing our IP address as {}".format(ip))

    if os.path.exists('ip.txt'):

        with open('ip.txt','r') as fh:

            oldip  = fh.read().strip()

            logger.debug("Old ip is {}".format(oldip))

            fh.close()

            fh = None

    if oldip == ip:
        
        logger.info("No ip change detected, oldip={}, newip={}".format(oldip, ip))

        return

    with open('ip.txt','w') as fh:
        logger.debug("Saving ip address {} to ip.txt".format(ip))
        fh.write(ip)
        fh.close()
        fh = None

    try:

        viurl = "https://api.linode.com/v4/domains/{}/records/{}".format(config['default']['domains'], config['default']['records'])
        logger.debug("Linode API URL is {}".format(viurl))
        listurl = "https://api.linode.com/v4/domains/{}/records".format(config['default']['domains'])
        logger.debug("Linode List URL is {}".format(listurl))

        headers = {"Authorization" : "Bearer {}".format(config['default']['token']), 
                   "Content-Type" : "application/json" }

        data = {"type": "A",
                "target" : ip,
                "name" : "dev",
                "ttl_sec" : 300}

        logger.debug("Getting list of domains")
        domains =  requests.get(listurl, headers=headers).json()

        logger.debug("Updating domain with new ip address {}".format(ip))
        update =  requests.put(listurl, json=data, headers=headers).json()

    except Exception as e:

        logger.error("Error connecting to Linode and getting a list of domains: {}".format(str(e)))


def main():

    parser = argparse.ArgumentParser(description='Dynamically updates the DNS entry at linode for your environment')

    parser.add_argument('--configuration', help='configuration file', required=True)

    args = parser.parse_args()

    if  args.configuration is not None:

        if os.path.exists(args.configuration):

            config = configparser.ConfigParser()

            config.read(args.configuration)
            
            logger.debug("Found configuration {} ".format(args.configuration))

            mainProcess(config)

        else:

            logger.error("Unable to find configuration file")

    else:

        logger.error("Please set the configuration parameter")

if __name__ == '__main__':

    main()
