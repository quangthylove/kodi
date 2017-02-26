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

import urllib,urllib2,re,os,sys,base64
import xbmcplugin,xbmcgui,xbmcaddon, xbmc

addon = xbmcaddon.Addon(id='plugin.video.thietkeweb30s.org.fshare')
profile = addon.getAddonInfo('profile')
home = addon.getAddonInfo('path')
dataPatch = xbmc.translatePath(os.path.join(home, 'resources'))
logos = xbmc.translatePath(os.path.join(dataPatch, 'logos\\'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
username = addon.getSetting('username')
password = addon.getSetting('password')
sys.path.append(os.path.join(home,'resources','lib'));from BeautifulSoup import BeautifulSoup;import urlfetch;import xsharetiny

dict = {'&amp;':'&', '&gt;':'', '&#8211;':'-', '&#8220;':'', '&#8221;':'', '&#8230;':'', '&#8216;':"'", '&#8217;':"'", '&#038;':"&", '<br/>':"-", '<br />':"-", '4.bp.blogspot.com':'lh3.googleusercontent.com', '3.bp.blogspot.com':'lh3.googleusercontent.com', '2.bp.blogspot.com':'lh3.googleusercontent.com', '1.bp.blogspot.com':'lh3.googleusercontent.com'}

def replace_all(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass

def alert(message,title="Thông báo!"):
    xbmcgui.Dialog().ok(title,"",message)		

def notification(message, timeout=3000):
    xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s, %s)' % ('fshare.vn', message, '', timeout)).encode("utf-8"))

def mess():
    if len(username) < 1 or len(password) < 1:
        alert(u'Hãy đăng nhập tài khoản [COLOR red]FSHARE VIP[/COLOR] của bạn để xem được Kho Phim này. Chọn [COLOR blue]OK[/COLOR] để đăng nhập.')
        addon.openSettings()
        return main()
    else:
        main()
	
def main():
	alert(u'Truy cập addon [COLOR red]HUEHDPLUS[/COLOR] để xem được nội dung này.'); return

def search(url):#1
    try:
        keyb=xbmc.Keyboard('', '[COLOR yellow]Nhâp tên phim cần tìm kiếm[/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
        if 'vaphim' in url:
            response = urlfetch.fetch('http://vaphim.com/?s='+urllib.quote_plus(searchText))
            items = re.compile("<a data=.+?<img.+?src=\"(.+?)\".+?<a href=\"(http://vaphim.com/.+?)\".+?>(.+?)</a>", re.DOTALL).findall(response.content)
            for item in items:
                name = re.sub(r'<.+?>', r'-', item[2])
                addDir( name, item[1], 5, item[0], isFolder=True)
        elif 'mphim' in url:
            url = 'http://mphim.net/tim-kiem/%s/trang-1.html' % (searchText.replace(' ','-').encode("utf-8"))
            medialist(url,page)
        elif 'fphim' in url:
            url = 'http://fsharefilm.com/?s=%s' % (searchText.encode("utf-8"))
            search_result(url,page)
    except:
        pass	
	
def sub_main(url,name):#2
    if 'Vphim' in name:
        addDir('[COLOR red]Tìm Kiếm (Vaphim)[/COLOR]', 'vaphim', 1, logos + 'timkiem.png', isFolder=True)
        content = makeRequest(url)
        match = re.compile('<li><a.+?href="/category/phim-2/(.+?)">(.+?)</a></li>').findall(content)
        for url, name in match:
	        addDir( name, ('%scategory/phim-2/%s' % (vaphim, url)), 4, logos+'theloai.png', isFolder=True)
    elif 'Mphim' in name:			
        addDir( '[COLOR red]Tìm Kiếm (mphim)[/COLOR]', 'mphim', 1, logos + 'timkiem.png', isFolder=True)
        content = makeRequest(url)
        match = re.compile('<li ><h2><a href="([^"]*).html">([^>]+)</a></h2>').findall(content)  
        for url, name in match:
            addDir( name, mphim + url + '/trang-' + str(page) +'.html', 4, logos+'theloai.png', page=1, isFolder=True)
        match = re.compile('<li ><h2><a href="([^"]*)">([^>]+)</a></h2>').findall(content)  
        for url, name in match:
            if '#' in url:	
                addDir( name, mphim, 3, logos+'theloai.png', '', isFolder=True)			
    elif 'Fphim' in name:
        addDir( '[COLOR red]Tìm Kiếm (fphim)[/COLOR]', 'fphim', 1, logos + 'timkiem.png', isFolder=True)
        addDir( '[COLOR orange]Xem Nhiều Trong Tháng[/COLOR]', 'http://fsharefilm.com/chuyen-muc/hai-kich/', 10, logos + 'TOP.png', page=1, isFolder=True)
        addDir( 'Hài Hước', 'http://fsharefilm.com/chuyen-muc/phim/hai-huoc/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Hành Động', 'http://fsharefilm.com/chuyen-muc/phim/hanh-dong/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Hoạt Hình', 'http://fsharefilm.com/chuyen-muc/phim/hoat-hinh/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Kinh Dị', 'http://fsharefilm.com/chuyen-muc/phim/kinh-di/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Thần Thoại', 'http://fsharefilm.com/chuyen-muc/phim/than-thoai/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Tình Cảm', 'http://fsharefilm.com/chuyen-muc/phim/tinh-cam/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Phim 18+', 'http://fsharefilm.com/chuyen-muc/phim/phim-18/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Việt Nam', 'http://fsharefilm.com/chuyen-muc/phim/viet-nam/', 4, logos + 'theloai.png', page=1, isFolder=True)
        addDir( 'Phim Bộ', 'http://fsharefilm.com/chuyen-muc/phim/phim-bo/', 4, logos + 'theloai.png', page=1, isFolder=True)		
    xbmc.executebuiltin('Container.SetViewMode(500)')

def categories(url,name,page=1):#3
    if 'Thể loại' in name:
        content = makeRequest(url)
        match = re.compile('<a href="/the-loai/([^"]*).html" title=".+?">([^>]+)</a>').findall(content)
        for url, name in match:  
            addDir( name, ('%s/the-loai/%s' % (mphim, url)) + '/trang-' + str(page) +'.html', 4, iconimage, page=1, isFolder=True)
    elif 'Quốc gia' in name:
        content = makeRequest(url)
        match = re.compile('<a href="/quoc-gia/([^"]*).html" title=".+?">([^>]+)</a>').findall(content)  
        for url, name in match:  
            addDir( name, ('%s/quoc-gia/%s' % (mphim, url)) + '/trang-' + str(page) +'.html', 4, iconimage, page=1, isFolder=True) 
    elif 'Năm Phát Hành' in name:
        content = makeRequest(url)
        match = re.compile('<li style="width:100px"><a href="/nam-phat-hanh/([^"]*).html">([^>]+)</a></li>').findall(content)  
        for url, name in match:  
            addDir( name, ('%s/nam-phat-hanh/%s' % (mphim, url))  + '/trang-' + str(page) +'.html', 4, iconimage, page=1, isFolder=True)	

def medialist(url,page=1):#4
    if 'vaphim' in url:
        content = makeRequest(url)
        match = re.compile('<img.+?src="(.+?)".+?\s*</span>\s*</a>\s*</div>\s*<h3 class="entry-title"><a href="(.+?)" rel="bookmark" >(.+?)</a></h3>').findall(content)
        for thumbnail, href, title in match:
	        title = title.split('] ')[-1]
	        title = replace_all(title, dict)
	        addDir( title, href, 5, thumbnail, isFolder=True)
        match = re.compile("<a href='(.+?)' class='nextpostslink'>(.+?)</a>").findall(content)
        for href, page in match:
	        addDir( '[COLOR red]Next >>>[/COLOR]', href, 4, logos+'NEXT.png', isFolder=True)	
    elif 'mphim' in url:
        content = makeRequest(url)
        soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup.findAll('a',{'class' : 'ntips'})
        for item in items:
            title = item.find('span',{'class':'title'}).string
            href = item.get('href')
            thumb = item.find('img',{'class':'lazy'}).get('data-original')
            addDir( title.encode('utf-8'), mphim + href, 5, replace_all(thumb, dict), isFolder=True)
        if len(items) == 25:		
            page = page+1
            next_page = url.split('trang')[0] + 'trang-' + str(page)+'.html'
            addDir( '[COLOR red]Next >>>[COLOR green] ' + 'trang ' + str(page) + '[/COLOR]', next_page, 4, logos + 'NEXT.png', page = page, isFolder=True)			
    elif 'fsharefilm' in url:
        content = makeRequest(url)	
        soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup.findAll('div',{'class' : 'movie col-xs-6 col-sm-4 col-md-3 col-lg-3'})#[:20]
        for item in items:
            href = item.find('a').get('href')
            title = item.find('img').get('alt')
            thumb = item.find('img').get('src').encode('utf-8')
            addDir( title.encode('utf-8'), href, 5, thumb, isFolder=True)
        if len(items) == 20:		
            page = page+1
            next_page = url.split('page/')[0] + 'page/' + str(page) + '/'
            addDir( '[COLOR red]Next >>>[COLOR green] ' + 'trang ' + str(page) + '[/COLOR]', next_page, 4, logos + 'NEXT.png', page = page, isFolder=True)

def episodes(url,iconimage):#5
    if 'vaphim' in url:
        content = makeRequest(url)
        match = re.compile('<a href="(.+?)".+?(.+?)</a>').findall(content)
        for link, title in match:
            if 'none' in title or 'Phụ Đề Việt' in title:
	            pass			
            elif 'fshare.vn/file' in link:
	            title = replace_all(title, dict)
	            xsharetiny.addir( title.replace('target="_blank">',''), link.replace('http:','https:'), iconimage, 100, isFolder=False)
            elif 'fshare.vn/folder' in link:
	            title = replace_all(title, dict)
	            addDir( title.replace('target="_blank">',''), link.replace('http:','https:'), 6, iconimage, isFolder=True)
    elif 'mphim' in url:
        content = makeRequest(url)
        match = re.compile('<a href="([^"]*)".+?target="_blank"><img src=".+?" alt=""/></a>').findall(content)
        if len(match) == 0:
	        notification(u'[COLOR red]Phim đang được cập nhật[/COLOR]');
        else:
            for href in match:
                content = makeRequest(href)
                item = re.compile('<a href="([^"]*)" target="_blank" style=".+?">.+?</a>').findall(content)
                for link in item:		
                    if 'fshare.vn/file' in link:
				        xsharetiny.addir( name, link, iconimage, 100, isFolder=False)
                    elif 'fshare.vn/folder' in link:
				        addDir( name, link, 6, iconimage, isFolder=True)
    elif 'fsharefilm' in url:
        content = makeRequest(url)
        match = re.compile('<a.+?href="(.+?)" target="_blank">(.+?</a>.+?)>').findall(content)
        if len(match) == 0:
	        notification(u'[COLOR red]Phim đang được cập nhật[/COLOR]');
        else:		
            for link, epi in match:
                #epi = epi.split('</a>')[-1]
                #epi = epi.split('</a>')[-1]
                if '4share' in link or 'Phụ đề Việt' in epi or 'Phụ Đề Việt' in epi:
			        pass 
                elif 'fshare.vn/file' in link:
			        if 'fshare.vn' in epi: artist = 'Link Vip'
			        else: artist = epi.split('</a>')[0]
			        xsharetiny.addir( replace_all(artist, dict), link.replace('http:','https:'), iconimage, 100, isFolder=False)
                elif 'fshare.vn/folder' in link:
			        if 'fshare.vn/folder' in epi: artist = 'Link Vip' + epi.split('</a>')[-1].replace('</p','')
			        else: artist = epi.replace('</a><br /','')
			        addDir( '[COLOR orange]' + replace_all(artist, dict) + '[/COLOR]', link.replace('http:','https:'), 6, iconimage, isFolder=True)
    xbmc.executebuiltin('Container.SetViewMode(51)')

def f_folder(url,iconimage):#6
	content = makeRequest(url)
	match = re.compile('<a class="filename".+?href="(.+?)".+?title="(.+?)">').findall(content)
	for href, name in match:
		if 'srt' in name: pass	
		else: xsharetiny.addir( name, href.replace('http:','https:'), '', 100, isFolder=False)	

def f_sub_folder(url,iconimage):#7
	content = makeRequest(url)
	match = re.compile('<a data-pjax class="filename folder" data-id="(.+?)".+?title="(.+?)">').findall(content)
	for id, title in match:
		xsharetiny.addir( '[COLOR orange]' + title + '[/COLOR]', 'https://www.fshare.vn/folder/%s' % id, '', 6, isFolder=True)		
		
def search_result(url,page=1):			
    if 'fsharefilm' in url:
        content = makeRequest(url)	
        soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup.findAll('div',{'class' : 'movie col-xs-6 col-sm-3 col-md-3 col-lg-3'})#[8:]
        for item in items:
            href = item.find('a').get('href')
            title = item.find('img').get('alt')
            thumb = item.find('img').get('src')
            addDir( title.encode('utf-8'), href, 5, thumb, isFolder=True)		

def rank_view(url,page=1):
    content = makeRequest(url)	
    soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.findAll('div',{'class' : 'movie'})#[8:]
    for item in items:
        href = item.find('a').get('href')
        title = item.find('img').get('alt').encode('utf-8')
        thumb = item.find('img').get('src').encode('utf-8')
        rank = '[COLOR orange]' + item.find('span',{'class':'movie-rank'}).string + '[/COLOR]' 
        addDir( str(rank) + '. ' + replace_all( title, dict), href, 5, thumb, isFolder=True)
			
def playlist(url):#50
    content = makeRequest(url)
    match = re.compile('<a id="(.+?)" href="(.+?)" img="(.+?)" fanart="">(.+?)</a>').findall(content)
    for id, link, thumb, title in match:
	        if id == '100' : isFolder = False
	        if id == '6' or id == '7' : isFolder = True
	        xsharetiny.addir( title, link, thumb, id, isFolder = isFolder)


def get_url():#90
    try:
        keyb = xbmc.Keyboard('https://www.fshare.vn/xxx/yyy', '[COLOR red]Nhập link fshare[/COLOR] [COLOR lime][xxx = file or folder; yyy = id fshare][/COLOR]')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText()).replace('%3A%2F%2F','://').replace('%2F','/').replace('%3F','?').replace('%3D','=').replace('%26','&').replace('%2C',',').replace('%3A',':')
            if 'fshare.vn/file' in searchText:
                xsharetiny.addir( searchText, searchText.replace('http:','https:'), iconimage, 100, isFolder=False)
            elif 'fshare.vn/folder' in searchText:
                addDir( searchText, searchText.replace('http:','https:'), 6, iconimage, isFolder=True)
    except:
        pass
		
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

def addDir(name,url,mode,iconimage,page=0,isFolder=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+str(page)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if not isFolder:
        liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
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

	
if 45 - 45: iiIIIII1i1iI - O0O0O - II1Ii - i11iII1iiI . oOo0O0Ooo / O0O0O
if 51 - 51: O0O0O + o0ooo
if 8 - 8: iiIIIII1i1iI * iI1Ii11111iIi - O0o00 - i11iII1iiI * oo % I1ii11iIi11i		
I1IiiI = base64.b64decode
if 6 - 6: OoOOo / i11iIiiIii + o0ooo * I1IiiI
O0O0O = 'aHR0cDovL2NvZGUudGhpZXRrZXdlYjMwcy5vcmcvU09VUkVDRS9NZW51Ri54bWw='
if 80 - 80: oOo0O0Ooo
if 83 - 83: O0Oooo00 . i11iIiiIii + oOo0O0Ooo . ii1II11I1ii1I * O0Oooo00
if 53 - 53: I1IiiI
	
vaphim = 'http://vaphim.com/'
mphim = 'http://mphim.net'
fphim = 'http://fsharefilm.com/'  
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
elif mode==1:search(url)
elif mode==2:sub_main(url,name)
elif mode==3:categories(url,name,page)
elif mode==4:medialist(url,page)
elif mode==5:episodes(url,iconimage)
elif mode==6:f_folder(url,iconimage)
elif mode==7:f_sub_folder(url,iconimage)
elif mode==10:rank_view(url,page)
elif mode==50:playlist(url)
elif mode==90:get_url()
elif mode==100:
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('***Thietkeweb30s.org***', 'Đang tải. Vui lòng chờ trong giây lát...')
    xsharetiny.play_url(url)
    dialogWait.close()
    del dialogWait
elif mode==101:addon.openSettings(); sys.exit() 
xbmcplugin.endOfDirectory(int(sys.argv[1]))