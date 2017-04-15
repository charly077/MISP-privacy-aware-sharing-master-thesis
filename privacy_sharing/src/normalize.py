#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Do not duplicate code in both readMisp and match Rules !
The goal first to normalize URLs and IPv6 addresses
URLs:
    - standards normalization as done with the library
    - additionnal 'normalizations' steps explained in the report
        (could transform the URL but better for matching)
IPv6: 
    - # TODO 
"""
import re, urllib
from url_normalize import url_normalize


def normalize(ioc):
    for attr_type in ioc:
        # distinction bewtwee url|uri|link is often misused
        # Thus they are considered the same
        if attr_type == 'url' or\
            attr_type == 'uri' or\
            attr_type == 'link':
                # just solve one specific case:
                if not '..org' in ioc[attr_type]:
                    ioc[attr_type] = urlNorm(ioc[attr_type])
        elif attr_type == 'hostname':
                ioc[attr_type] = ioc[attr_type].lower()
    return ioc


directory_indexes = ['default.asp', 'index.html', 'index.php', 'index.shtml'\
                    'index.jsp', '\?']
def urlNorm(url):
    url = url_normalize(url)
    # removes fragment
    url = urllib.parse.urldefrag(url)[0]

    # remove index directories if it is at the end
    for index in directory_indexes:
        url = re.sub(index+ '$', '', url)
    
    # remove http https
    url = re.sub("^https?://(www.)?", '', url)
    return url
