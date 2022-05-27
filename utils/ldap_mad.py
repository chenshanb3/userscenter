import ldap3.core.exceptions
from ldap3 import *
from django.conf import settings
from utils.custom_log import log_start
import json

logger = log_start('ldap')


class LdapMadTools(object):
    def __init__(self):
        self.domain = settings.AUTH_LDAP_DOMAIN
        self.ldap_server_uri = settings.AUTH_LDAP_SERVER_URI
        self.base_dn = settings.BASE_DN
        self.user = settings.AUTH_LDAP_BIND_USER
        self.password = settings.AUTH_LDAP_BIND_PASSWORD
        self.ldap_port = settings.AUTH_LDAP_SERVER_PORT
        self.use_ssl = settings.AUTH_LDAP_USER_SSL

        try:
            self.server = Server(self.ldap_server_uri, port=self.ldap_port, use_ssl=self.use_ssl)
            self.conn = Connection(self.server, user=self.user, password=self.password, authentication=NTLM,
                                   auto_bind=True)
        except ldap3.core.exceptions.LDAPExceptionError as e:
            logger.error('ldap conn失败，原因为: %s' % str(e))

    def ldap_search_dn(self, uid):
        try:
            obj = self.conn
            obj.search(search_base=self.base_dn,
                       search_filter='(sAMAccountName={})'.format(uid),
                       search_scope=SUBTREE,
                       attributes=['displayName'])
            entry = obj.response[0]
            dn = entry['dn']
            return dn
        except Exception as e:
            logger.error(('获取用户%s 失败，原因为: %s' % (uid, str(e))))
            return None

    def ldap_get_user(self, uid):
        obj = self.conn
        obj.search(search_base=self.base_dn,
                   search_filter='(sAMAccountName={})'.format(uid),
                   search_scope=SUBTREE,
                   attributes=ALL_ATTRIBUTES)
        entry = obj.response[0]
        attr_dict = entry['attributes']
        return attr_dict

    def ldap_add_user(self):
        pass

    def check_user_status(self):
        pass

    def ldap_get_vaild(self, uid, password):
        logger.info("start ldap vaild")
        user = self.domain + uid
        try:
            self.server = Server(self.ldap_server_uri, port=self.ldap_port, use_ssl=self.use_ssl)
            self.conn = Connection(self.server, user=user, password=password, authentication=NTLM,
                                   auto_bind=True)
            return True
        except ldap3.core.exceptions.LDAPExceptionError as e:
            logger.error('ldap conn失败，原因为: %s' % str(e))
            return False

    def ldap_update_password(self, uid, pwd):
        try:
            obj = self.conn
            dn = self.ldap_search_dn(uid)
            print(dn)
            obj.extend.microsoft.modify_password(dn, pwd)
            return True
        except ldap3.core.exceptions.LDAPExceptionError as e:
            logger.error('ldap 修改密码失败，原因为: %s' % str(e))
            return False

    def ldap_update_user(self, dicts, uid):
        dn = self.ldap_search_dn(uid)
        obj = self.conn
        change = {}
        # c.modify('cn=user1,ou=users,o=company',
        #          {'givenName': [(MODIFY_REPLACE, ['givenname-1-replaced'])],
        #           'sn': [(MODIFY_REPLACE, ['sn-replaced'])]})
        for key, value in dicts.items():
            change[key] = "[(MODIFY_REPLACE, [{}])]".format(value)
        obj.modify(dn, change)
