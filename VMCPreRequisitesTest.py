import requests
import json
from random import randint
import atexit
import logging
import sys

class VMCValidation:

    #initialize variables
    def __init__( self):
        self.org_id= sys.argv[1] #'c5a81416-dc30-4a2e-83d2-3348a036de85' #param1
        self.refresh_token= sys.argv[2]#'072d43c7-a1c3-4c71-bf4c-17104afe7570' #param3
        self.sddc_id=None #'34a98450-ac9d-4e9d-9bf4-d1e72b959aae' #param2
        self.sddc_name=None
        self.csp_token_url='https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize'
        self.vmc_validation_test1_url=None
        self.vmc_validation_test2_url=None
        self.vmc_validation_test3_url=None
        self.vmc_validation_test4_url=None
        self.csp_token_str=None


    #This method gets SDDC id
    def get_sddc_id( self):
        try:

           #TODO Modify this code to retrieve sddc id
           self.sddc_id=sys.argv[3]#'34a98450-ac9d-4e9d-9bf4-d1e72b959aae'
           return self.sddc_id
        except Exception:
            logging.error("Error while getting the sddc id")

    # This method returns CSP Auth token. If the token can't be retrieved it returns 0

    def get_token(self):
        #url = 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize'
        params = {
            'refresh_token': self.refresh_token
        }
        header = {
            'Content-Type': 'application/json'
        }
        try:
            res = requests.post (self.csp_token_url, params=params , headers=header )
            print ( res.status_code )
            data = res.json ( )
            self.csp_token_str = data.get ( 'access_token' )
            print ( "self.csp_token_str = " + self.csp_token_str )
            assert (res.status_code == 200)
            return self.csp_token_str
        except AssertionError:
            logging.error('Error retrieving csp token:', res.content)


    def vmc_validation_test1(self):
        self.vmc_validation_test1_url = 'https://vmc.vmware.com/vmc/api/orgs/' + str(self.org_id) + '/sddcs/' + str(self.sddc_id) + '/networks/4.0/sddc/networks'
        print(self.vmc_validation_test1_url)
        testname = "API Test" + str(randint(1,10000))
        print(testname)
        number = str(randint(160,165))
        primaryaddress ='10.63.' + str(number) + '.1'
        print("primaryAddress = " + primaryaddress)
        iprange ='10.63.' + str(number) + '.2-10.63.' + str(number) + '.250'
        print("iprange = " + iprange)
        #vmc_test1_url = 'https://vmc.vmware.com/vmc/api/orgs/c5a81416-dc30-4a2e-83d2-3348a036de85/sddcs/34a98450-ac9d-4e9d-9bf4-d1e72b959aae/networks/4.0/sddc/networks'
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/json',
                   'Origin': 'https://vmc.vmware.com',
                   'Accept': 'text/plain',
                   'csp-auth-token': str(self.csp_token_str)
                   }
        payload = {
            "name": str(testname),
            "cgwId": "edge-2",
            "cgwName": "SDDC-CGW-1",
            "subnets": {
                "addressGroups": [
                    {
                        "primaryAddress": str(primaryaddress),
                        "prefixLength": "24"
                    }
                ]
            },
            "dhcpConfigs": {
                "ipPools": [
                    {
                        "ipRange": str(iprange)
                    }
                ]
            }
        }
        try:
            #res = requests.post ( vmc_test1_url , data=json.dumps ( payload ) , headers=headers )
            res = requests.post ( self.vmc_validation_test1_url , data=json.dumps ( payload ) , headers=headers )
            assert (res.status_code == 201), print(res.content,res.status_code)
            #TODO: Check what needs to be assert
        except AssertionError as e:
            logging.error('VMC validation test#1 failed:')


    def vmc_validation_test2(self):
        self.vmc_validation_test2_url = 'https://vmc.vmware.com/vmc/api/orgs/' + str(self.org_id) + '/sddcs/' + str(self.sddc_id) + '/dns/private'
        print(self.vmc_validation_test2_url)
        headers = {'Cache-Control': 'no-cache' ,
                   'Content-Type': 'application/json' ,
                   'csp-auth-token': str(self.csp_token_str)
                   }
        try:
            r = requests.put (self.vmc_validation_test2_url , headers=headers )
            print ( r.content )
            print(r.status_code)
            assert (r.status_code == 202)
        except AssertionError as e:
            logging.error('VMC Validation test#2 failed')


    def vmc_validation_test3(self):
        self.vmc_validation_test3_url = 'https://vmc.vmware.com/vmc/api/orgs/' + str(self.org_id) + '/sddcs/' + str(self.sddc_id) + '/networks/4.0/edges/edge-1/dns/config'
        print(self.vmc_validation_test3_url)
        #ipaddr1=str(randint(160,165))
        #ipaddr2=str(randint(160,165))
        ipaddress1='10.166.17.90'
        ipaddress2='10.166.17.91'
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/json',
                   'Origin': 'https://vmc.vmware.com',
                   'Accept': 'text/plain',
                   'csp-auth-token': str(self.csp_token_str)
                   }
        payload = {
            "featureType": "dns",
            "version": 12012,
            "enabled": "true",
            "cacheSize": 16,
            "listeners": {
                "type": "dhs_listener",
                "vnic": [
                    "any"
                ]
            },
            "dnsViews": {
                "dnsView": [
                    {
                        "viewId": "view-0",
                        "name": "vsm-default-view",
                        "enabled": "true",
                        "viewMatch": {
                            "ipAddress": [
                                "any"
                            ],
                            "vnic": [
                                "any"
                            ],
                            "ipSet": [

                            ]
                        },
                        "recursion": "false",
                        "forwarders": {
                            "ipAddress": [
                                str(ipaddress1),
                                str(ipaddress2)
                            ]
                        }
                    }
                ]
            },
            "logging": {
                "enable": "false",
                "logLevel": "info"
            }
        }
        try:
            r = requests.put(self.vmc_validation_test3_url, data=json.dumps(payload), headers=headers)
            print(r.status_code, r.content)
            assert (r.status_code == 202)
        except AssertionError as e:
            logging.error('VMC validation test#3 failed:')



    def vmc_validation_test4(self,name,edge):
        self.vmc_validation_test4_url = 'https://vmc.vmware.com/vmc/api/orgs/' + self.org_id + '/sddcs/' + self.sddc_id + '/networks/4.0/edges/' + str(edge) + '/firewall/config/rules'
        print(self.vmc_validation_test4_url)
        headers = {'Cache-Control': 'no-cache',
                   'Content-Type': 'application/json',
                   'Origin': 'https://vmc.vmware.com',
                   'Accept': 'text/plain',
                   'csp-auth-token': str(self.csp_token_str)
                   }
        payload = {
            "firewallRules": [
                {
                    "name": str(name),
                    "ruleType": "user",
                    "enabled": "true",
                    "loggingEnabled": "false",
                    "action": "accept",
                    "destination": {
                        "exclude": "false",
                        "ipAddress": [
                            "34.217.201.141",
                            "10.70.9.196"
                        ],
                        "groupingObjectId": [

                        ],
                        "vnicGroupId": [

                        ]
                    },
                    "application": {
                        "applicationId": [

                        ],
                        "service": [
                            {
                                "protocol": "TCP",
                                "port": [
                                    "443"
                                ],
                                "sourcePort": [
                                    "any"
                                ]
                            }
                        ]
                    }
                }
            ]
        }
        try:
            r = requests.post(self.vmc_validation_test4_url, data=json.dumps(payload), headers=headers)
            assert (r.status_code == 201),print(r.content,r.status_code)
        except AssertionError as e:
            logging.error('VMC validation test#4 failed')


c = VMCValidation()
c.sddc_id=c.get_sddc_id()
c.csp_token_str=c.get_token()
c.vmc_validation_test1()
#c.vmc_validation_test2()
#c.vmc_validation_test3()
#c.vmc_validation_test4('vCenter_Web','edge-1')
#print(t)