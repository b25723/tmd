import unittest
import sys
import os
import re
import yaml
import time


class demo1_positive(unittest.TestCase):
    #    def __init__(self):

    def setUp(self):
        with open('/opt/zetatauri/conf/init.yaml') as fh:
            self.f = fh.readlines()
            p = self.f.index('snmp:\n')
        del self.f[p:]
        with open('/opt/zetatauri/conf/init.yaml', 'w') as fh:
            fh.writelines(self.f)

    def test_v3(self):
        '''
        start snmpv3 with authpriv security_level and launch query snmpv3/authpriv with a priv_key(digit+alphabet).
        '''
        conf = '''snmp:
  enabled: true #true | false
  version: v3   #v1 | v2c | v3
  community: public
  security_name: snmpuser
  security_level: authPriv #authNoPriv | authPriv
  auth_protocol: SHA #MD5 | SHA
  auth_key: 1234567a
  priv_protocol: AES #
  priv_key: 1234567b'''

        with open('/opt/zetatauri/conf/init.yaml', 'a') as fh:
            fh.writelines(conf)

        os.popen('service snmpd stop')
        os.popen('service zeta-mgmt stop')
        os.popen('service zeta-mgmt start')
        time.sleep(3)
        pid = os.popen('pidof snmpd').read().strip()
        #time.sleep(1)
        self.assertTrue(pid)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v3 -u snmpuser -a SHA -x AES -A 1234567a -X 1234567b -l authPriv localhost iso.3.6.1.2.1.1.1').read()
        self.assertTrue(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v3 -u snmpuser -a SHA -x AES -A 1234567a -X 1234567a -l authPriv localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v1 -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v2c -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)

    def test_v1(self):
        '''
        start snmpv3 with authpriv security_level and launch query with snmpv3/authpriv but use auth_key(digit+alpabet) as priv_key.
        '''
        conf = '''snmp:
  enabled: true #true | false
  version: v1   #v1 | v2c | v3
  community: public
  security_name: snmpuser
  security_level: authPriv #authNoPriv | authPriv
  auth_protocol: SHA #MD5 | SHA
  auth_key: 1234567a
  priv_protocol: AES #
  priv_key: 1234567b'''

        with open('/var/lib/vnf/udata/init.yaml', 'a') as fh:
            fh.writelines(conf)

        os.popen('/bin/bringup_rc.d/rc.901.net_snmpd.sh restart').read().strip()
        time.sleep(0.5)
        pid = os.popen('pidof snmpd').read().strip()
        #time.sleep(1)
        self.assertFalse(pid)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v3 -u snmpuser -a SHA -x AES -A 1234567a -X 1234567a -l authPriv localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v1 -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertTrue(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v2c -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)


    def test_v2(self):
        '''
        start snmpv3 with authpriv security_level and launch query with snmpv3/authpriv but use auth_key(digit+alpabet) as priv_key.
        '''
        conf = '''snmp:
  enabled: true #true | false
  version: v2c   #v1 | v2c | v3
  community: public
  security_name: snmpuser
  security_level: authPriv #authNoPriv | authPriv
  auth_protocol: SHA #MD5 | SHA
  auth_key: 1234567a
  priv_protocol: AES #
  priv_key: 1234567b'''

        with open('/var/lib/vnf/udata/init.yaml', 'a') as fh:
            fh.writelines(conf)

        os.popen('/bin/bringup_rc.d/rc.901.net_snmpd.sh restart').read().strip()
        time.sleep(0.5)
        pid = os.popen('pidof snmpd').read().strip()
        #time.sleep(1)
        self.assertFalse(pid)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v3 -u snmpuser -a SHA -x AES -A 1234567a -X 1234567a -l authPriv localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v1 -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertFalse(sq)
        sq = os.popen('LD_LIBRARY_PATH=. ./snmpwalk -r1 -v2c -c public localhost iso.3.6.1.2.1.1.1').read()
        self.assertTrue(sq)




if __name__ == '__main__':
    unittest.main()
