"""
Module to find the whois record
"""


import json
from Feature_Extractor.Extractor import parse_response
from Feature_Extractor.Extractor import whois_query
from Feature_Extractor.Extractor import ssl_cert
from Feature_Extractor.Extractor import extract_characteristics
from Feature_Extractor.Parser import url_parser
from Feature_Extractor.Parser import dom
from lxml import html
import re

#Procedure to extract all the whois information through the whois and dig linux command
#
# Find the domain name
# Find the registrar whois server
# Find IP address
# Find whois related to IP address
# Retrive a Json with information gathered

class main(): 

    def __init__(self,url):
        self.url=url
        self.whois=self.whois()
        

    def whois(self):
        """
        Method to return the whois information relate to the an url.
        Procedure:
        1.Find the domain name
        2. Find the registrar whois server
        3. Find IP address
        4. Find whois related to IP address
        5. Retrive a Json with information gathered
        """
        

        domain = dom.Dom.Url(self.url)
        urlw = url_parser.URL(self.url)
        wh = whois_query.Whois()

        #/////////////////////////////////
        data = wh.whois(dom = urlw.domain)
        certificate = ssl_cert.ssl_certificate(urlw.domain)
        #/////////////////////////////////

        url=lambda x : len(x)
        pathsfun=lambda x :True if x!='NaN' else False
        pathsfil=pathsfun(urlw.path)
        paths=lambda x : len(list(filter(pathsfun,x)))
        pathschar=lambda x : 1 if ('$'or'_'or'-'or'&'or'~'or'+'or'=') in str(x) else 2
        domains=lambda x: len(x)
        subdomains=lambda x :1 if len(x)==1 else 2
        """Dominios gTLD no restringidos"""
        tld=['com','info','net','org']
        """Dominios gTLD restringidos"""
        tld2=['biz','name','pro']
        """Dominios gTLD patrocinados"""
        tld3=['aero','asia','cat',	'coop','edu','gov','int','jobs','mil','mobi','museum','post','tel','travel','xxx']
        """Dominios gTLD paises"""
        tld4=['ac','ad','ae','af','ag','ai','al','am','ao','aq','ar','as','at','au','aw','ax','az','ba','bb','bd','be','bf','bg','bh','bi','bj','bm','bn','bo','br','bs','bt','bw','by','bz','ca','cc','cd','cf','cg','ch','ci','ck','cl','cm','cn','co','cr','cu','cv','cw','cx','cy','cz','de','dj','dk','dm','do','dz','ec','ee','eg','er','es','et','eu','fi','fj','fk','fm','fo','fr','ga','gd','ge','gf','gg','gh','gi','gl','gm','gn','gp','gq','gr','gs','gt','gu','gw','gy','hk','hm','hn','hr','ht','hu','id','ie','il','im','in','io','iq','ir','is','it','je','jm','jo','jp','ke','kg','kh','ki','km','kn','kp','kr','kw','ky','kz','la','lb','lc','li','lk','lr','ls','lt','lu','lv','ly','ma','mc','md','me','mg','mh','mk','ml','mm','mn','mo','mp','mq','mr','ms','mt','mu','mv','mw','mx','my','mz','na','nc','ne','nf','ng','ni','nl','no','np','nr','nu','nz','om','pa','pe','pf','pg','ph','pk','pl','pm','pn','pr','ps','pt','pw','py','qa','re','ro','rs','ru','rw','sa','sb','sc','sd','se','sg','sh','si','sk','sl','sm','sn','so','sr','st','su','sv','sx','sy','sz','tc','td','tf','tg','th','tj','tk','tl','tm','tn','to','tr','tt','tv','tw','tz','ua','ug','uk','us','uy','uz','va','vc','ve','vg','vi','vn','vu','wf','ws','ye','yt','za','zm','zw']


        tlds=lambda x: 1 if x.rsplit('.')[1] in str(tld) else 0
        tlds2=lambda x: 1 if x.rsplit('.')[1] in str(tld2) else 0
        tlds3=lambda x: 1 if x.rsplit('.')[1] in str(tld3) else 0
        tlds4=lambda x: 1 if x.rsplit('.')[1] in str(tld4) else 0
        verifyip=lambda x: 1 if( (len(re.findall(r"2[0-5][0-5]|1[0-9][0-9]|[0-9][0-9]|[0-9]|[a-zA-Z]",x)) >= 4) and (len(re.findall(r"\.",x)) == 3 )and (len(re.findall(r"[a-zA-Z]",x))== 0)) else 0
        homograph=lambda x: 1 if x.count("xn--") else 0
        dicc1 = {"url description": {"url_len": url(urlw.url), "domain_len": domains(urlw.domain),"homograph":homograph(urlw.domain), "subdomain_len": subdomains(urlw.subdomain),"tld_nores":tlds(urlw.domain),"tld_res":tlds2(urlw.domain),"tld_spons":tlds3(urlw.domain),"tld_countr":tlds4(urlw.domain),"special_chrtrs_count": pathschar(urlw.path) ,"urlip": verifyip(urlw.subdomain+urlw.domain),"paths_len": paths(urlw.path) }}
        forms = lambda x: 0 if len(x) == 0 else 1
        dicc1.update({'html description': {
            "forms": forms([str(domain.html.forms[i].action) for i in range(0, len(domain.html.forms))])}})
        dicc1.update({'html description': domain.formularios()})
        dicc1.update({"ssl": extract_characteristics.ssl_issuer(certificate) , "whois" : extract_characteristics.whois_characteristics(parse_response.jsonparser(data=data['w'],dict={},keyword='Domain Whois Record')) })
        return dicc1








