```
Copied and pasted the content on https://manikos.github.io/webfaction-letsencrypt-django
(including comments) to this file in order to savw it for future reference
```




live in the pale blue dot

Alone Djangonaut
About
Portfolio
Webfaction LetsEncrypt Django
 Sat 31 December 2016 Nick Mavrakis Https python webfaction django letsencrypt
Why HTTPS
First things first. I do not work for Google nor I have any (social, financial, ethical etc) benefits from this gigantic company. But let be honest. If you are not ranked hign enough in Google's search results, your optimism about your website success is slowly betake to collapse. I think everybody that owns a website, wants his "e-property" to be shown amongst the first results in Google. Of course, you might say, that the search keywords added in the search bar are very important too, but that is not to be discussed here.

So, you have a website (maybe you have build it too) and your domain is i.e http://www.ilovewhatido.com/. Then you read this blog post by Google and got terrified about your ranking position. Thinking "Oh man, I have to change the http protocol to https. How painful will this be?" or "how much do I have to pay (monthly or yearly) in order to do that?" or "if I switch to https, will my web app behave the same as it was with http?".

Lets give answers to these questions:

"Oh man, I have to change the http protocol to https. How painful will this be?"
Super easy. Assuming your application is hosted on Webfaction, just follow the guide that follows!
"How much do I have to pay (monthly or yearly) in order to do that?"
None! Zero! Nothing! It's free! Using LetsEncrypt you get a certificate free of charge that lasts 3 months (60 days). You have the ability to renew the certificate 1 month (30 days) before expiration. Of course, you must be aware that there are various types of certificates. The most used ones are: Domain Validation - DV, Organization Validation - OV and Extended Validation - EV. Each type of certificate depends on its lifetime (months or years until expiration), procedure in order to be obtained (is it just one click away or you have to wait days or weeks in order to get it), cost (from free of charge up to thousands of dollars/euros). LetsEncrypt issues only DN certificates. You can learn more about the different types of certificates here.
So, why there are so many kind of certificates, you ask? Apart from the fact that certifiacte authorities (CA) have to earn money somehow, each certificate type varies by occasion (are you a small, medium or large-sized company, is it just a personal blog, is it a local news website, are you a medium-sized e-commerce website etc). So, for example, a small-sized business is not obliged to pay thousands of euros/dollars in order to obtain a certificate just to prove to the end user that it is what it claims to be. This kind of business can obtain a free one. Anyway, it is up to the website owner to choose the certificate of his preference. One sidenote though, have you ever noticed in your Web browser, that in some HTTPS sites the whole address bar turns green and the business' info are visible to the left of the URL, whereas in other HTTPS sites the browser's address bar is not green and it just shows a green lockpad? This is because in the first case the website owner choosed an EV certificate (which offers this green address bar) while in the latter case the website owner choosed either a DV or an OV certificate.
"If I switch to https, will my web app behave the same as it was with http?"
This depends extremely on the framework your application was build. Using Django there is nothing to worry about when switching to HTTPS. Just make sure you are including the SecurityMiddleware in your MIDDLEWARE setting. After you switch to HTTPS, run the following Django command in your server (to which you will be connected via ssh): python manage.py check --deploy. This will check your deployment settings and underline any potential warnings you should take a closer look.


Django, Webfaction and Letsencrypt (3 great friends!)
So, you have build your HTTP website using Django, uploaded to Webfaction and everything works smoothly. Now you want to switch to HTTPS. Here is what to do (do not be terrified of the too many steps, I am just too descriptive!): (Many thanks to cpbotha, Neilpang acme.sh and ryans answer. Forgive me if there is someone I forget.)

[UPDATE, thanks to Ned Batchelder (see comments below)]: In order for the follow to work you should have openssl installed (just run which openssl and check if it's installed), otherwise install it following this guide.

Login to your Applications and click Add new application
Select a name for it, say my_ssl_app and under the App category menu select PHP. Under the App type select Static/CGI/PHP-7.0. Click the Save button.
Now navigate to your Websites, make an exact copy of your existent HTTP website and enable HTTPS on it. How? Simple create a new website, choose the same domains (with and without www), choose the same Application (not the one we have just created) but do not forget to select the button Encrypted website (https). Click Save.
You will notice that your HTTPS website says Security HTTPS, using shared certificate. That's OK for now. We'll fix that later.
Select your HTTP version of your website and under the Contents section remove your existing application. Then, add the new one we just created (my_ssl_app). Click Save.
Now, if you visit your site you will NOT get your usual homepage. We have not done any redirection to HTTPS yet. Stay with me!
From your local machine open terminal and ssh yourUserName@webXXX.webfaction.com
vim ~/webapps/my_ssl_app/.htaccess
Hit key i (to enter Insert mode and start writing), copy (Ctrl + c) the following text and paste it (Ctrl + Shift + v) to the opened file (.htaccess). After pasting, hit the Esc key and then write :wq (this will save the file and quit the vim editor):

RewriteEngine on
RewriteRule !^.well-known($|/) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
Done with redirection. Now if you visit your site (mysite.com) you will be redirected to https://mysite.com, BUT a security warning will arise saying that the site you are trying to visit may be dangerous or so. That's because we are using a shared certificate. Getting closer!

In terminal you must install the terrific acme.sh script. Simply:

curl https://get.acme.sh | sh
Everything is done automatically for you. Log out from the terminal and ssh to log back in.

Now you have the command acme.sh available globally. Time to use it.

Before, of course, to request a brand new official certificate from LetsEncrypt, we must request a staging (test) certifiacte, in order to be sure that everything is working properly. So...

acme.sh --issue --test -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app
If everything worked, you should have 7 files to the path ~/.acme.sh/mysite.com/ which are (ca.cer, fullchain.cer, mysite.com.cer,  mysite.com.conf, mysite.com.csr, mysite.com.csr.conf and mysite.com.key). If something is missing, then maybe this is because these are just test certificates and keys. Not usable in production.

Now that everything worked, it's time to issue for the real ones.

(notice the missing --test parameter)

acme.sh --issue -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app
The above command will fetch the same kind of files (with the same name) but this time this folks are official. Their lifetime is 90 days and LetsEncrypt lets you renew your certificates no earlier than 60 days after your last issue. For example, if you issued your certificates today (2016-12-31) then the earlier you can issue them again (renew them) is at 2017-02-31. Of course there is always the option to renew them earlier by using the  --force argument.

Now go to the SSL certificates, select Add SSL Certificate and choose Upload Certificate. This step, you only have to do it once. Give it a name, say mysite_cert (remember this name, it will be used in the last step) and then copy the contents of  ~/.acme.sh/mysite.com/mysite.com.cer to a file and the upload it to the Certificate section. Do the same with the  ~/.acme.sh/mysite.com.key and the Private Key section and finally with the ~/.acme.sh/ca.cer and the Intermediates/bundle section. All these could be done via the create_certificate funtion of the Webfaction's API, of course.

[SCRIPT UPDATED ON 2017-02-21] Now for my favourite part, automation. I have written a Python (2.7) script in order to talk to Webfaction's API and update my certificates automatically without bringing my site offline AND without having me (a human) to interact with the Control Panel every 2 months in order to install manually the renewed certificates. This Python script is executed every day (as a cron job).

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
Save the above to your server, say as .certificate_renewal.py and place it under your $HOME directory, ~/.certificate_renewal.py.

Now, crontab -e and delete the line at the very bottom that was inserted during the installation of the acme.sh script before (step #10).

Instead, write:

0 2 * * * /usr/local/bin/python $HOME/.certificate_renewal.py 2>> /path/to/your/log
The above cron job will run every day at 02.00 (am) and check if your certificates need any renewal. If so, then they will be automatically updated for you (via the function update_certificate) from the API.

Last step. Go to your websites and choose the HTTPS version of your domain. Under the "Security" section, "Choose a certificate" dropdown menu, choose the certificate you created (not the "Shared certificate", of course). You will find it with the name you gave it on step 20 (in this example we gave it the name mysite_cert).

[BONUS]: If you're using Python 3 (which you should) the following modification should be made in order for the script to work.

First: change from xmlrpclib import ServerProxy, Fault to from xmlrpc.client import ServerProxy, Fault`.
Second: change if 'Cert success.' in out: to if 'Cert success.' in out.decode('utf8'):`.
Third: change 's_name': hostname.strip('\n').title(), to 's_name': hostname.decode('utf8').strip('\n').title(),.
Fourth: in your cron job change /usr/local/bin/python (which defaults to python 2.7 but maybe not if you have already an alias to it with python 3. Better check it by simply typing python and check the version you got back. If its 3.x.x then do not alter the cron on step #24, otherwise continue to the change) to /usr/local/bin/python3.x where x is the version you want to use. That's it!
Wasn't that easy enough? Now you have a HTTPS secured website where the certification is automatically renewed every 2 months!

Happy New Year to all Earth(ians)!


Out there

 Twitter
 Github
 StackOverflow
Useful

 getpelican.com icon Pelican
 python.org icon Python.org
 jinja.pocoo.org icon Jinja2
Browse content by

 Categories
 Tags
 Feed
Disclaimer

This blog-website expresses my own thoughts, opinions and ideas in order to keep an order in my head. Any reference to an external source is linked.

 Back to top
Site generated by Pelican | Plumage theme by Kevin Deldycke | ☄ 2016 Nick Mavrakis



mtaysic • 16 days ago
Thank you for this! Super super super helpful.
 
•Reply•Share ›
Avatar
dave guandalino • 25 days ago
Thanks for the super useful guide. My question is when I have www and non-www domains. Which certificate should I upload, the www or the other?

Then, should I use two renewal scripts one for each domain?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  dave guandalino • 25 days ago
As the step #18 says, when you issue a certificate for both the www and non-www webiste (using the commad acme.sh --issue -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app), you should have these files under the dir yoursite.com/: ca.cer, fullchain.cer, mysite.com.cer, mysite.com.conf, mysite.com.csr, mysite.com.csr.conf and mysite.com.key.

As step #20 says, you should upload the mysite.com.cer, mysite.com.key and ca.cer to webfaction.

There is no difference (for certificates) between www and non-www website.
 
•Reply•Share ›
Avatar
Camilo • a month ago
Hey Nick, I'm successful with the test but when I try to issue "the real ones" I get the following error (mysite = my actual domain):

mysite.com:Verify error:Invalid response from http://mysite.com/.well-known/acme-challenge/zmaVN6Hg8EtMxu5hbkFOCoabHicIZXd1LE5u4fXqkTs:

Any idea what could be wrong?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Camilo • a month ago
Hello Camilo. The error you provide could be caused by a variety of reasons. Why not run acme.sh --issue --debug -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app or acme.sh --issue --debug 2 -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app and see a "debugged" output, with lots of information?
Have you completed all steps until step 17, correctly?

Also, check this and this github issues that may be of a help.
Do, let me know, in order to upgrade this guide and keep it bug-safe.
 
•Reply•Share ›
Avatar
Camilo  Nick Mavrakis • a month ago
Thanks for the answer. After having a look at everything (logs, debug, and the threads you linked) I ended up changing the website location from my_ssl_app to the actual application my site uses. Since the error was that the http site was not responding, I switched to the https one and it worked in the first try.

Changed this:

acme.sh --issue -d mysite.com -d www.mysite.com -w ~/webapps/my_ssl_app
To this:

acme.sh --issue -d mysite.com -d www.mysite.com -w ~/webapps/old_website_app
Hope this helps anyone having the same problem.

Best wishes!
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Camilo • a month ago
Very glad it worked for you. Soon, I'll revise this "tutorial" to cover cases like yours.
Best regards Camilo (and thank you for the feedback)!
 
•Reply•Share ›
Avatar
Jonny Webb • 2 months ago
Thanks for this great tutorial. I have no experience with Python and I'm not sure if I followed steps 21 to the end correctly. I am assuming I am supposed to modify the pwd, domain, and cert_name field in the .certificate_renewal.py file to the information valid to my account. Is that the only modification I have to make to that file? Also, with step 24, I wasn't sure if I was supposed to make any changes to that line of code. I saved the file to the root folder for my webfaction account. /home/username/.certificate_renewal.py Is this correct for the crontab script? I also didn't change /path/to/your/log at all since I wasn't sure what to change it to if I was supposed to. Any clarification or help would be greatly appreciated.
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Jonny Webb • 2 months ago
Hello Johnny.

1. Yes. For the step 21, the only variables you have to change are: pwd, domain, and cert_name.
2. Since you saved the python script (step 21) under the path /home/username/.certificate_renewal.py then you shouldn't change the cron entry. However, you should change the /path/to/your/log path. What would be that? Just the path to a plain file (/home/username/logs/renew.log) where you can put it anywhere. A prefferred location is under the Webfaction's logs directory under the /home/username/logs/access/ (if I recall correctly). Do a ls ~ and it will show you Webfaction's logs directory.

Hope that helps. If you have any other question, don't hesitate to reply!

Best regards!
 
•Reply•Share ›
Avatar
merhawie • 5 months ago
I am a bit of a python n00b. could you help me figure out how to modify your script to work on multiple domains?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  merhawie • 5 months ago
Please see this answer and let me know if that helped you!
 
•Reply•Share ›
Avatar
merhawie  Nick Mavrakis • 5 months ago
Hi nick - it was a bit more helpful, but I guess we will see if its renew function works. Is there a way to confirm that the renew function will function on cue?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  merhawie • 5 months ago
I believe the only way to check if that worked is to visit your SSL Cerificates page in about 2 months and see the expitation date. It should be 2 months later.
1  
•Reply•Share ›
Avatar
Ned Batchelder • 5 months ago
I tried this, and acme.sh wouldn't run because openssl isn't installed?
$ curl https://get.acme.sh | sh
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
111 671 111 671 0 0 1312 0 --:--:-- --:--:-- --:--:-- 5368
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 133k 100 133k 0 0 2594k 0 --:--:-- --:--:-- --:--:-- 4777k
[Sat Feb 25 01:18:15 UTC 2017] Installing from online archive.
[Sat Feb 25 01:18:15 UTC 2017] Downloading https://github.com/Neilpang...
[Sat Feb 25 01:18:15 UTC 2017] Extracting master.tar.gz
[Sat Feb 25 01:18:15 UTC 2017] Please install openssl first.
[Sat Feb 25 01:18:15 UTC 2017] We need openssl to generate keys.
[Sat Feb 25 01:18:15 UTC 2017] Pre-check failed, can not install.

I don't see any mention here of a step to get openssl installed. Any clue?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Ned Batchelder • 5 months ago
Sorry to hear this. Maybe openssl is not installed by default in Webfaction. Try running which openssl and if that fails then you must install it from source. I'll update my guide to do that but in the meantime try it from here. Do not forget to include the --prefix=$HOME/bin/ (assumes that the bin dir exists) to install openssl under this file, otherwise the default is to install it to /usr/local/ssl in which users do not have write priviledges.

If which openssl succeeds then maybe it is not in your PATH. Simply add it, so acme can find it. Open console and execute these two lines: 

export PATH=$HOME/openssl/bin:$PATH
export LD_LIBRARY_PATH=$HOME/openssl/lib
(taken from here).

Let me know if everything worked!
 
•Reply•Share ›
Avatar
Ned Batchelder  Nick Mavrakis • 5 months ago
It seems that WebFaction defined OPENSSL_BIN to refer to a directory that I could not read. Neilpang did a fantastic job jumping on the problem and fixing it: https://github.com/Neilpang...
 
•Reply•Share ›
Avatar
Ned Batchelder  Ned Batchelder • 5 months ago
Everything worked fine. I didn't need steps 8 and 9 (maybe my .htaccess configuration is slightly different already?), and at step 18 I had to add --force to get it to issue new certs. But now I am all set, thanks!
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Ned Batchelder • 5 months ago
That's great! In my installation it didn't crush on openssl that's why I did not include it as part of my tutorial. Thanks for the feedback and to Neilpang for fixing this asap! Let me know how the script went and if everything went smoothly!
 
•Reply•Share ›
Avatar
Rave Smith • 6 months ago
A fantastic guide, has helped me a lot.

I have a problem with the script for autorenovation, I have this error:

Traceback (most recent call last):
File "boda.py", line 21, in <module>
acme_process = Popen(['%s/acme.sh' % HIDDEN_ACME_DIR_NAME, 'cron'], stdout=PIPE, stderr=PIPE)
File "/usr/lib64/python2.6/subprocess.py", line 642, in __init__
errread, errwrite)
File "/usr/lib64/python2.6/subprocess.py", line 1238, in _execute_child
raise child_exception
OSError: [Errno 2] No such file or directory

Might you help me? In my server I have python 2.6, maybe that's the problem.

I would greatly appreciate your help.

Rave
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Rave Smith • 6 months ago
Hello and thanks for your nice comments about my post.

Regarding your traceback` I don't think that your server's python version is the problem. 
I suspect that the directory /home/{user}/{acme}/{domain} does not exist. Please note that an example directory might be something like /home/nik/.acme.sh/mywebsite.com/. In order for the script to work the dir mywebsite.com must be under acme.sh/ dir.

Tell if that was the issue.
 
•Reply•Share ›
Avatar
Rave Smith  Nick Mavrakis • 6 months ago
Hi Nick

thanks for your quick response.

It seems the problem was the path, I used absolute path and I do not get errors.

Now wait until February 14th to check if the certificate is renewed.
I'll let you know

Thank you very much for your help and your knowledge.
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Rave Smith • 6 months ago
February 14th has passed! Any news about the script? Did it work nicely?
 
•Reply•Share ›
Avatar
Rave Smith  Nick Mavrakis • 5 months ago
Hi Nick

Thanks for your interest

Unfortunately I have not been able to renew the certificates automatically. I've used the latest version of your script, but nothing happens. The script runs quickly, and the log file is empty. There are no error messages.

I do not know what the problem may be, the configuration options of the script are few and they are all correct. I use the script without modifications since my version of python is the 2.7.5 (I migrated to a new server, previously had the 2.6).

If you could give me some tips I would appreciate it.

Thank you for your time and help.

Rave.
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Rave Smith • 5 months ago
This happened because the certificates have been generated from Lets Encrypt (the 
Popen(['%s/acme.sh' % HIDDEN_ACME_DIR_NAME, 'cron'], stdout=PIPE, stderr=PIPE) has run) but for some reason the if 'Cert success.' in out: did not executed.
Please try again but this time change to this: Popen(['%s/acme.sh' % HIDDEN_ACME_DIR_NAME, 'cron', 'force'], stdout=PIPE, stderr=PIPE). This will force (no matter how many days remaining until renewal) to regenerate the certs (with a new expire date). Finally, because in the output of this command there will be no 'Cert success.', change to this if 'Cert success.' not in out:. Now, run the script. It should update the existing certificate with a new one (90 from the day you execute it). Now, back to the script and undo those changes!
Hope that helps you. Let me know if everything worked (for me it's working!)
Best regards
 
•Reply•Share ›
Avatar
Rave Smith  Nick Mavrakis • 5 months ago
Hi

Thank you a lot, with the changes the certificate is renewed. Will the next renewal be ok without script modifications?
 
•Reply•Share ›
Avatar
Nick Mavrakis Mod  Rave Smith • 6 months ago
No problem. Glad I could help.

Please let me know if it worked in order to amend the script, if necessary.

Best regards!
 
•Reply•Share ›