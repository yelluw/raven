#!/usr/local/bin python

"""
Script automates renewing letsencrypt certs
Python2.7

This was copied from https://manikos.github.io/webfaction-letsencrypt-django

It is being used 
"""



#!/usr/local/bin python

from os import chdir, environ, getcwd, listdir, stat

from sys import exit

from subprocess import Popen, PIPE

from xmlrpclib import ServerProxy, Fault

HIDDEN_ACME_DIR_NAME = '.acme.sh'

def data_to_var(filename):
    try:
        assert (filename in listdir('.') and stat(filename).st_size > 0)
    except AssertionError as exc:
        exit('The file \"{}\" does not exist inside \"{}\" or is empty. Exception: {}'.format(filename, getcwd(), exc))
    else:
        with open(filename, 'r') as f:
            var_cert = f.read()
        return var_cert

if __name__ == '__main__':
    # Run the command advised by acme.sh script in order to renew the certificates.
    # Each certificate lasts 90 days and the max permitted day to renew a certificate is 60 days from the issue date -
    # in other words the earlier we can renew a certificate is 30 days before expiration. This can be changed through
    # the --days argument during the --issue step. Type ".acme.sh/acme.sh --help" for more information.
    # This script will run as a cron job every day in order for the certs to be renewed when appropriate.

    acme_process = Popen(['%s/acme.sh' % HIDDEN_ACME_DIR_NAME, 'cron'], stdout=PIPE, stderr=PIPE)
    out, err = acme_process.communicate()

    if err:
        exit("An error occurred during the renewal process. Error: {}".format(err))

    if 'Cert success.' in out:
        hostname, err = Popen(['hostname', '-s'], stdout=PIPE, stderr=PIPE).communicate()
        if err:
            exit("An error occurred while trying to determine the hostname. Error: {}".format(err))
        d = {
            'url': 'https://api.webfaction.com/',  # Fixed. Not to be changed.
            'version': 2,  # Fixed. Not to be changed.
            's_name': hostname.strip('\n').title(),
            'user': environ.get('USER'),
            'pwd': 'password',  # Your Webfaction password.
            'domain': 'mysite.com',  # Your domain name where you issued the certificate.
            'cert_name': 'mysite_cert',  # Your certification name (see step #20).
        }

        # Initially empty values (to be filled later with data from files)
        domain_cert, pv_key, intermediate_cert = '', '', ''
        # Directory declarations in order to know where to work
        valid_cert_dir = '{home}/{acme}/{domain}'.\
            format(home=environ.get('HOME'), acme=HIDDEN_ACME_DIR_NAME, domain=d.get('domain'))

        # Change directory to the one that matches our domain
        chdir(valid_cert_dir)
        # Test if current working directory is the valid one
        try:
            assert getcwd() == valid_cert_dir
        except AssertionError:
            exit('Current working directory is not {}! Instead is {}.'.format(valid_cert_dir, getcwd()))

        # try to connect to Webfaction API
        try:
            server = ServerProxy(d.get('url'))
            session_id, _ = server.login(d.get('user'), d.get('pwd'), d.get('s_name'), d.get('version'))
        except Fault as e:
            exit("Exception occurred at connection with Webfaction's API. {}".format(e))
        else:
            # Connection is successful. Proceed...

            # read domain certificate and store it as a variable
            domain_cert = data_to_var('{}.cer'.format(d.get('domain')))

            # read private key certificate and store it as a variable
            pv_key = data_to_var('{}.key'.format(d.get('domain')))

            # read intermediate certificate and store it as a variable
            intermediate_cert = data_to_var('ca.cer')

            # Install the renewed certificate to your Web server through the Webfaction's API
            if domain_cert and pv_key and intermediate_cert:
                # https://docs.webfaction.com/xmlrpc-api/apiref.html#method-update_certificate
                # update_certificate(session_id, name, certificate, private_key, intermediates)
                server.update_certificate(session_id, d.get('cert_name'), domain_cert, pv_key, intermediate_cert)
