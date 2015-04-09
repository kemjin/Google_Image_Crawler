#########################################################################
#
# Google image crawler 
#
# Author: Jin Kim
# Website: http://fenrirsystems.com/
# email: wannaboxster@gmail.com
# 
# I modified some part of code of Jaime's code. Feel free to modify my code too. 
#
# Original google image download source code from Jaime Ivan Cervantes
# http://stackoverflow.com/questions/9318577/python-the-right-url-to-download-pictures-from-google-image-search
#
#
# Also, Special thanks to Stephen Raymond Ferg to provide this amazingly easy-to-use GUI framework
#
# Easygui info
#
# EasyGui version 0.97
#
# Copyright (c) 2014, Stephen Raymond Ferg
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Easygui website: http://easygui.sourceforge.net
#
#
#########################################################################

import os, sys, time, urllib2, json
from urllib import FancyURLopener
import easygui

# Define search term w/ GUI
e = easygui
msg = "What kind of image do you want to download?"
searchTerm = e.enterbox(msg, "Google image crawler", "Enter your keyword: ")
# Replace spaces ' ' in search term for '%20' in order to comply with request
searchTerm = searchTerm.replace(' ','%20')

e.msgbox("Where do you want to save images?", "Select your storage")
filepath = e.diropenbox(msg='Where do you want to save images?', title='Google image grawler', default=None)
filepath = filepath + '/'

# Start FancyURLopener with defined version 
class MyOpener(FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
myopener = MyOpener()

# This app will automatically stop after 64 pics downloaded. Google API sends only max 64 pic's data
for i in range(0,18):
    # Notice that the start changes for each iteration in order to request a new set of images for each loop
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
    print url
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

    # Get results using JSON
    results = json.load(response)
    data = results['responseData']
    dataInfo = data['results']

    # Iterate for each result and get unescaped url
    for myUrl in dataInfo:
        print myUrl['unescapedUrl']
        #Get file name
        url_encode = myUrl['unescapedUrl'].encode('ascii','ignore')
        file_name = url_encode.split('/')

        if (file_name[len(file_name)-1][-4:] == '.jpg' or file_name[len(file_name)-1][-4:] == '.JPG' or file_name[len(file_name)-1][-4:] == '.png' or file_name[len(file_name)-1][-4:] == '.PNG' or file_name[len(file_name)-1][-4:] == '.gif'):
            try:
                myopener.retrieve(myUrl['unescapedUrl'], filepath + file_name[len(file_name)-1])
            except:
                pass
        else:
            try:
                myopener.retrieve(myUrl['unescapedUrl'], filepath + file_name[len(file_name)-1] + '.jpg')
            except:
                pass
    # Sleep for one second to prevent IP blocking from Google
    time.sleep(3)
