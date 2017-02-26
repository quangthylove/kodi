# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib,urllib2,re,os,base64
import xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon(id='plugin.video.thietkeweb30s.org.htvonline')
profile = addon.getAddonInfo('profile')
home = addon.getAddonInfo('path')
dataPatch = xbmc.translatePath(os.path.join(home, 'resources'))
logos = xbmc.translatePath(os.path.join(dataPatch, 'logos\\'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

def alert(message,title="Thông báo!"):
    xbmcgui.Dialog().ok(title,"",message)

def main():
    alert(u'Truy cập addon [COLOR red]*THIETKEWEB30S.ORG* MOVIE GTTH[/COLOR] để xem được nội dung này.'); return

def search():
    try:
        keyb = xbmc.Keyboard('', '[COLOR yellow]Nhâp từ khóa tìm kiếm[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
        url = 'http://htvonline.com.vn/tim-kiem/%s' % urllib.quote_plus(searchText.replace(' ','-'))
        results(url)
    except:
        pass
		
def results(url):
    content = makeRequest(url)
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.findAll('div',{'class' : 'content_results_2'})
    for item in items:
        href = item.find('a',{'class':'play_video_thumb_2'}).get('href')
        thumb = item.find('img').get('src')
        title = item.find('img').get('alt')		
        addDir( title.encode('utf-8'), href, 4, thumb)		
		
def livetv(url):
    content = makeRequest(url)
    match = re.compile('<a class=.+?data-original="([^"]*)"><img alt=.+?src="([^>]+)"></a>').findall(content)
    for url, thumb in match:
        title = url.split('livetv/')[1]
        name = title.split('-3')[0]
        name = name.replace('-',' ')	  
        addLink( name.upper(), url, 100, thumb)
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.xeebo':
        xbmc.executebuiltin('Container.SetViewMode(52)')  
    else:
        xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)

def medialist(url,page=1):
    content = makeRequest(url)
    items = re.compile('<a href="(.+?)" >\s*.+?\s*<img.+?alt="(.+?)" src="(.+?)"/>\s*</a>').findall(content)
    for item in items:
        addDir( item[1], item[0], 4, item[2])
    if len(items) == 20:
        page = page+1
        next_page = url.split('?page=')[0] + '?page=' + str(page)
        addDir( '[COLOR red]Next >>>[COLOR green] ' + 'trang ' + str(page) + '[/COLOR]', next_page, 3, logos + 'NEXT.png', page = page)

def episodes(url,name,iconimage):
    if 'xem-phim' in url:
        content = makeRequest(url)
        items = re.compile('<a data-tooltip=".+?" class=".+?" href="(.+?)">(.+?)</a>').findall(content)
        for item in items:
            addLink( '[[COLOR gold]' + item[1] + '[/COLOR]] ' + name, item[0], 100, iconimage)		
    else:
        content = makeRequest(url)
        items = re.compile('<a data-tooltip=".+?" class=".+?" href="(.+?)">\s*<span class=\'.+?\'>(.+?)</span></a>').findall(content)
        for item in items:
            addLink( '[[COLOR gold]' + item[1] + '[/COLOR]] ' + name, item[0], 100, iconimage)

def resolveUrl(url):
    content = makeRequest(url)
    mediaUrl = re.compile('data-source="(.+?)"').findall(content)[0]
    OOoO = advertisement()
    item=xbmcgui.ListItem(path=mediaUrl)  
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    if len(OOoO) > 0:
        try:
            xbmc.sleep(3000);xbmc.Player().setSubtitles(OOoO);print OOoO
        except:
            pass
    return

def advertisement():
    content = makeRequest(I1IiiI('aHR0cHM6Ly9kbC5kcm9wYm94dXNlcmNvbnRlbnQuY29tL3MvdTlkejc5NGdvdHpwb3BoLyVzLnR4dA==') % addon.getSetting('temp_patch'))
    OOoO = re.search('sub:"(.+?)",',content)
    if OOoO:OOoO = OOoO.group(1)
    else:OOoO = ''
    return OOoO	
	
def makeRequest(url, headers=None):
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                 'Referer' : 'http://www.google.com'}
    try:
        req = urllib2.Request(url,headers=headers)
        f = urllib2.urlopen(req)
        body=f.read()
        return body
    except:
        pass 
  
def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&iconimage="+urllib.quote_plus(iconimage)  
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')  
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  

def addDir(name,url,mode,iconimage,page=0):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
	  	
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

htv_phim = 'http://htvonline.com.vn/phim-viet-nam'
htv_tv = "http://htvonline.com.vn/livetv"
htv_show = 'http://htvonline.com.vn/shows'
I1IiiI = base64.b64decode	
params=get_params()
url=None
name=None
mode=None
iconimage=None
page=0

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try:page=int(urllib.unquote_plus(params["page"]))
except:pass

if mode==None or url==None or len(url)<1:main()
elif mode==1:search()
elif mode==2:livetv(url)
elif mode==3:medialist(url,page)
elif mode==4:episodes(url,name,iconimage)
elif mode==5:results(url)
elif mode==100:
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('*THIETKEWEB30S.ORG* MOVIE GTTH', 'Đang tải. Vui lòng chờ trong giây lát...')
    resolveUrl(url)
    dialogWait.close()
    del dialogWait
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))