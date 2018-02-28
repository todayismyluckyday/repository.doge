################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import zipfile
import uservar
import fnmatch
import base64
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin
from resources.libs import extract, downloader, notify, debridit, traktit, loginit, skinSwitch, uploadLog, wizard as wiz

ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID,'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(ADDONPATH, 'fanart.jpg')
ICON             = os.path.join(ADDONPATH, 'icon.png')
ART              = os.path.join(ADDONPATH, 'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
INSTALLMETHOD    = wiz.getS('installmethod')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFREQ         = wiz.getS('autocleanfreq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
INCLUDEVIDEO     = wiz.getS('includevideo')
INCLUDEALL       = wiz.getS('includeall')
INCLUDECERSHO    = wiz.getS('includecerebroshow')
INCLUDECOVEN     = wiz.getS('includecovenant')
INCLUDEDEATH     = wiz.getS('includedeathstreams')
INCLUDEELYSIUM   = wiz.getS('includeelysium')
INCLUDEEXODUS    = wiz.getS('includeexodus')
INCLUDEINCUR     = wiz.getS('includeincursion')
INCLUDENEPTUNE	 = wiz.getS('includeneptune')
INCLUDEOCULU     = wiz.getS('includeoculus')
INCLUDEPLACEN    = wiz.getS('includeplacenta')
INCLUDEPOSEIDON  = wiz.getS('includeposeidon')
INCLUDEPROJM     = wiz.getS('includeprojectm')
INCLUDESPECTO    = wiz.getS('includespecto')
INCLUDESTREAMH   = wiz.getS('includestreamhub')
INCLUDEUKTURK    = wiz.getS('includeukturk')
INCLUDEXXXODUS   = wiz.getS('includexxxodus')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPLOGIN        = wiz.getS('keeplogin')
LOGINSAVE        = wiz.getS('loginlastsave')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
MYBUILDS         = os.path.join(BACKUPLOCATION, 'My_Builds', '')
AUTOFREQ          = int(float(AUTOFREQ)) if AUTOFREQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)
KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON 
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
THEME6           = uservar.THEME6
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONSPEED        = uservar.ICONSPEED if not uservar.ICONSPEED == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID
LOGINID          = loginit.LOGINID
MODURL           = 'http://tribeca.tvaddons.ag/tools/maintenance/modules/'
MODURL2          = 'http://mirrors.kodi.tv/addons/jarvis/'
INSTALLMETHODS   = ['Always Ask', 'Reload Profile', 'Force Close']
DEFAULTPLUGINS   = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

def index():
	if AUTOUPDATE == 'Yes':
		if wiz.workingURL(WIZARDFILE) == True:
			ver = wiz.checkWizard('version')
			if ver > VERSION: addFile('%s [[COLOR %s]v%s] [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (ADDONTITLE, COLOR1, VERSION, ver), 'wizardupdate', themeit=THEME2)
			else: addFile('%s [[COLOR %s]v%s[/COLOR]]' % (ADDONTITLE, COLOR1, VERSION), '', themeit=THEME2)
		#else: addFile('%s [[COLOR %s]v%s[/COLOR]]' % (ADDONTITLE, COLOR1, VERSION), '', themeit=THEME2)
	#else: addFile('%s [[COLOR %s]v%s[/COLOR]]' % (ADDONTITLE, COLOR1, VERSION), '', themeit=THEME2)
	if len(BUILDNAME) > 0:
		version = wiz.checkBuild(BUILDNAME, 'version')
		build = '%s ([COLOR %s]v%s[/COLOR])' % (BUILDNAME, COLOR1, BUILDVERSION)
		if version > BUILDVERSION: build = '%s [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (build, version)
		addDir(build,'viewbuild',BUILDNAME, themeit=THEME4)
		themefile = wiz.themeCount(BUILDNAME)
		if not themefile == False:
			addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME6)
	#else: addDir('None', 'builds', themeit=THEME4)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	#addDir ('Builds'        ,'builds',   icon=ICONBUILDS,   themeit=THEME1)
	#addDir ('Maintenance'   ,'maint',    icon=ICONMAINT,    themeit=THEME1)
	#addDir ('Internet Tools' ,'net', icon=ICONSPEED, themeit=THEME1)
	if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Forks n APKs' ,'apk', icon=ICONAPK, themeit=THEME1)
	if not ADDONFILE == 'http://': addDir ('Addon Installer' ,'addons', icon=ICONADDONS, themeit=THEME1)
	if not YOUTUBEFILE == 'http://' and not YOUTUBETITLE == '': addDir (YOUTUBETITLE ,'youtube', icon=ICONYOUTUBE, themeit=THEME1)
	#addDir ('Save Account Info'     ,'savedata', icon=ICONSAVE,     themeit=THEME1)
	if HIDECONTACT == 'No': addFile('Wizard Support' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	#addFile('Settings'      ,'settings', icon=ICONSETTINGS, themeit=THEME1)
	if DEVELOPER == 'true': addDir('Developer Options','developer', icon=ICONSETTINGS, themeit=THEME1)
	setView('files', 'viewType')

def buildMenu():
	WORKINGURL = wiz.workingURL(BUILDFILE)
	if not WORKINGURL == True:
		addFile('%s Version: [COLOR %s]%s[/COLOR]' % (MCNAME, COLOR2, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		addDir ('Save Account Info'       ,'savedata', icon=ICONSAVE,     themeit=THEME2)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		addFile('URL for txt file not valid', '', icon=ICONBUILDS, themeit=THEME2)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:
		total, count15, count16, count17, count18, adultcount, hidden = wiz.buildCount()
		third = False; addin = []
		link  = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"')
		match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
		if total == 1 and third == False:
			for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				if not DEVELOPER == 'true' and wiz.strTest(name): continue
				viewBuild(match[0][0])
				return
		addFile('%s Version: [COLOR %s]%s[/COLOR]' % (MCNAME, COLOR2, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		addDir ('Save Account Info'       ,'savedata', icon=ICONSAVE,     themeit=THEME2)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		if len(match) >= 1:
			if SEPERATE == 'true':
				for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if not DEVELOPER == 'true' and wiz.strTest(name): continue
					menu = createMenu('install', '', name)
					addDir('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			else:
				if count18 > 0:
					state = '+' if SHOW18 == 'false' else '-'
					addFile('[B]%s Leia Builds ([COLOR %s]%s[/COLOR])[/B]' % (state, COLOR2, count18), 'togglesetting',  'show18', themeit=THEME3)
					if SHOW18 == 'true':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 18:
								menu = createMenu('install', '', name)
								addDir('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count17 > 0:
					state = '+' if SHOW17 == 'false' else '-'
					addFile('[B]%s Krypton Builds ([COLOR %s]%s[/COLOR])[/B]' % (state, COLOR2, count17), 'togglesetting',  'show17', themeit=THEME3)
					if SHOW17 == 'true':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 17:
								menu = createMenu('install', '', name)
								addDir('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count16 > 0:
					state = '+' if SHOW16 == 'false' else '-'
					addFile('[B]%s Jarvis Builds ([COLOR %s]%s[/COLOR])[/B]' % (state, COLOR2, count16), 'togglesetting',  'show16', themeit=THEME3)
					if SHOW16 == 'true':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 16:
								menu = createMenu('install', '', name)
								addDir('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count15 > 0:
					state = '+' if SHOW15 == 'false' else '-'
					addFile('[B]%s Isengard and Below Builds ([COLOR %s]%s[/COLOR])[/B]' % (state, COLOR2, count15), 'togglesetting',  'show15', themeit=THEME3)
					if SHOW15 == 'true':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv <= 15:
								menu = createMenu('install', '', name)
								addDir('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if THIRDPARTY == 'true':
					if not THIRD1NAME == '' and not THIRD1URL == '': third = True; addin.append('1')
					if not THIRD2NAME == '' and not THIRD2URL == '': third = True; addin.append('2')
					if not THIRD3NAME == '' and not THIRD3URL == '': third = True; addin.append('3')
					if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
					addFile('[B]3rd Party Wizard(s):[/B]', '', icon=ICONBUILDS, themeit=THEME3)
				if third == True:
					for item in addin:
						name = eval('THIRD%sNAME' % item)
						addDir ("%s" % name, 'viewthirdparty', item, icon=ICONBUILDS, themeit=THEME2)
		elif hidden > 0: 
			if adultcount > 0:
				addFile('There is currently only Adult builds', '', icon=ICONBUILDS, themeit=THEME3)
				addFile('Enable Show Adults in Addon Settings > Misc', '', icon=ICONBUILDS, themeit=THEME3)
			else:
				addFile('Currently No Builds Offered from %s' % ADDONTITLE, '', icon=ICONBUILDS, themeit=THEME3)
		else: addFile('Text file for builds not formated correctly!', '', icon=ICONBUILDS, themeit=THEME3)
	setView('files', 'viewType')

def viewBuild(name):
	WORKINGURL = wiz.workingURL(BUILDFILE)
	if not WORKINGURL == True:
		addFile('URL for txt file is not valid', '', themeit=THEME3)
		addFile('%s' % WORKINGURL, '', themeit=THEME3)
		return
	if wiz.checkBuild(name, 'version') == False: 
		addFile('Error reading the txt file.', '', themeit=THEME3)
		addFile('%s was NOT found in the builds list.' % name, '', themeit=THEME3)
		return
	link = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % name).findall(link)
	for version, url, gui, kodi, themefile, icon, fanart, preview, adult, description in match:
		icon        = icon   if wiz.workingURL(icon)   else ICON
		fanart      = fanart if wiz.workingURL(fanart) else FANART
		build       = '%s ([COLOR %s]v%s[/COLOR])' % (name, COLOR1, version)
		if BUILDNAME == name and version > BUILDVERSION:
			build = '%s [COLOR red][CURRENT v%s][/COLOR]' % (build, BUILDVERSION)
		addFile(build, '', description=description, fanart=fanart, icon=icon, themeit=THEME5)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		addDir ('Save Account Info',       'savedata', icon=ICONSAVE,     themeit=THEME2)
		addFile('Build Information',    'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		if not preview == "http://": addFile('Build Review', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=THEME2)
		temp1 = int(float(KODIV)); temp2 = int(float(kodi))
		if not temp1 == temp2: 
			if temp1 == 16 and temp2 <= 15: warning = False
			else: warning = True
		else: warning = False
		if warning == True:
			addFile("[B][I][COLOR red]Build designed for Kodi version %s [COLOR white](Version Installed: %s!)[/COLOR][/I][/B]" % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile(wiz.sep(''), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile('Fresh Install'   , 'install', name, 'fresh'  , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		addFile('Standard Install', 'install', name, 'normal' , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not gui == 'http://': addFile('Apply GuiFix'    , 'install', name, 'gui'     , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not themefile == 'http://':
			if wiz.workingURL(themefile) == True:
				addFile(wiz.sep('THEMES'), '', fanart=fanart, icon=icon, themeit=THEME3)
				link  = wiz.openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
				for themename, themeurl, themeicon, themefanart, themeadult, description in match:
					if not SHOWADULT == 'true' and themeadult.lower() == 'yes': continue
					themeicon   = themeicon   if themeicon   == 'http://' else icon
					themefanart = themefanart if themefanart == 'http://' else fanart
					addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=THEME3)
	setView('files', 'viewType')

def viewThirdList(number):
	name = eval('THIRD%sNAME' % number)
	url  = eval('THIRD%sURL' % number)
	work = wiz.workingURL(url)
	if not work == True:
		addFile('URL for txt file is not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:
		type, buildslist = wiz.thirdParty(url)
		addFile("[B]%s[/B]" % name, '', themeit=THEME2)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		if type:
			for name, version, url, kodi, icon, fanart, adult, description in buildslist:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				addFile('[[COLOR %s]%s[/COLOR]] %s ([COLOR %s]v%s[/COLOR])' % (COLOR1, float(kodi), name, COLOR1, version), 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)
		else:
			for name, url, icon, fanart, description in buildslist:
				addFile(name, 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)

def editThirdParty(number):
	name  = eval('THIRD%sNAME' % number)
	url   = eval('THIRD%sURL' % number)
	name2 = wiz.getKeyboard(name, '[COLOR %s]Enter the Name of the Wizard:[/COLOR]' % COLOR1)
	url2  = wiz.getKeyboard(url, '[COLOR %s]Enter the URL of the Wizard txt file:[/COLOR]' % COLOR2)
	
	wiz.setS('wizard%sname' % number, name2)
	wiz.setS('wizard%surl' % number, url2)

def apkScraper(name=""):
	if name == 'kodi':
		kodiurl1 = 'http://mirrors.kodi.tv/releases/android/arm/'
		kodiurl2 = 'http://mirrors.kodi.tv/releases/android/arm/old/'
		url1 = wiz.openURL(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
		url2 = wiz.openURL(kodiurl2).replace('\n', '').replace('\r', '').replace('\t', '')
		x = 0
		match1 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
		match2 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url2)
		
		addFile("Official Kodi APKs", themeit=THEME1)
		rc = False
		for url, name, size, date in match1:
			if url in ['../', 'old/']: continue
			if not url.endswith('.apk'): continue
			if not url.find('_') == -1 and rc == True: continue
			try:
				tempname = name.split('-')
				if not url.find('_') == -1:
					rc = True
					name2, v2 = tempname[2].split('_')
				else: 
					name2 = tempname[2]
					v2 = ''
				title = "[COLOR %s]%s v%s%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, COLOR2, size.replace(' ', ''), COLOR1, date)
				download = urljoin(kodiurl1, url)
				addFile(title, 'apkinstall', "%s v%s%s %s" % (tempname[0].title(), tempname[1], v2.upper(), name2), download)
				x += 1
			except:
				wiz.log("Error on: %s" % name)
			
		for url, name, size, date in match2:
			if url in ['../', 'old/']: continue
			if not url.endswith('.apk'): continue
			if not url.find('_') == -1: continue
			try:
				tempname = name.split('-')
				title = "[COLOR %s]%s v%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], tempname[2], COLOR2, size.replace(' ', ''), COLOR1, date)
				download = urljoin(kodiurl2, url)
				addFile(title, 'apkinstall', "%s v%s %s" % (tempname[0].title(), tempname[1], tempname[2]), download)
				x += 1
			except:
				wiz.log("Error on: %s" % name)
		if x == 0: addFile("Error: Kodi Scraper Is Currently Down.")
	elif name == 'spmc':
		spmcurl1 = 'https://github.com/koying/SPMC/releases'
		url1 = wiz.openURL(spmcurl1).replace('\n', '').replace('\r', '').replace('\t', '')
		x = 0
		match1 = re.compile('<div.+?lass="release-body.+?div class="release-header".+?a href=.+?>(.+?)</a>.+?ul class="release-downloads">(.+?)</ul>.+?/div>').findall(url1)
		
		addFile("Official SPMC APKs", themeit=THEME1)

		for name, urls in match1:
			tempurl = ''
			match2 = re.compile('<li>.+?<a href="(.+?)" rel="nofollow">.+?<small class="text-gray float-right">(.+?)</small>.+?strong>(.+?)</strong>.+?</a>.+?</li>').findall(urls)
			for apkurl, apksize, apkname in match2:
				if apkname.find('armeabi') == -1: continue
				if apkname.find('launcher') > -1: continue
				tempurl = urljoin('https://github.com', apkurl)
				break
			if tempurl == '': continue
			try:
				name = "SPMC %s" % name
				title = "[COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, name, COLOR2, apksize.replace(' ', ''))
				download = tempurl
				addFile(title, 'apkinstall', name, download)
				x += 1
			except Exception, e:
				wiz.log("Error on: %s / %s" % (name, str(e)))
		if x == 0: addFile("Error: SPMC Scraper Is Currently Down.")

def apkMenu(url=None):
	if url == None:
		addDir ('Official Kodi APKs', 'apkscrape', 'kodi', icon=ICONAPK, themeit=THEME1)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	if not APKFILE == 'http://':
		if url == None:
			APKWORKING  = wiz.workingURL(APKFILE)
			TEMPAPKFILE = uservar.APKFILE
		else:
			APKWORKING  = wiz.workingURL(url)
			TEMPAPKFILE = url
		if APKWORKING == True:
			link = wiz.openURL(TEMPAPKFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for name, section, url, icon, fanart, adult, description in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if section.lower() == 'yes':
						x += 1
						addDir ("[B]%s[/B]" % name, 'apk', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						x += 1
						addFile(name, 'apkinstall', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					if x < 1:
						addFile("No addons added to this menu yet!", '', themeit=THEME2)
			else: wiz.log("[APK Menu] ERROR: Invalid Format.", xbmc.LOGERROR)
		else: 
			wiz.log("[APK Menu] ERROR: URL for APK list not working.", xbmc.LOGERROR)
			addFile('URL for txt file not valid', '', themeit=THEME2)
			addFile('%s' % APKWORKING, '', themeit=THEME3)
		return
	else: wiz.log("[APK Menu] No APK list added.")
	setView('files', 'viewType')

def addonMenu(url=None):
	if not ADDONFILE == 'http://':
		if url == None:
			ADDONWORKING  = wiz.workingURL(ADDONFILE)
			TEMPADDONFILE = uservar.ADDONFILE
		else:
			ADDONWORKING  = wiz.workingURL(url)
			TEMPADDONFILE = url
		if ADDONWORKING == True:
			link = wiz.openURL(TEMPADDONFILE).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for name, plugin, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if plugin.lower() == 'section':
						x += 1
						addDir ("[B]%s[/B]" % name, 'addons', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						try:
							add    = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
							if os.path.exists(add):
								name   = "[COLOR green][Installed][/COLOR] %s" % name
						except:
							pass
						x += 1
						addFile(name, 'addoninstall', plugin, TEMPADDONFILE, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					if x < 1:
						addFile("No addons added to this menu yet!", '', themeit=THEME2)
			else: 
				addFile('Text File not formated correctly!', '', themeit=THEME3)
				wiz.log("[Addon Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[Addon Menu] ERROR: URL for Addon list is not working.")
			addFile('URL for txt file is not valid', '', themeit=THEME2)
			addFile('%s' % ADDONWORKING, '', themeit=THEME3)
	else: wiz.log("[Addon Menu] No Addon list added.")
	setView('files', 'viewType')

def addonInstaller(plugin, url):
	if not ADDONFILE == 'http://':
		ADDONWORKING = wiz.workingURL(url)
		if ADDONWORKING == True:
			link = wiz.openURL(url).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
			if len(match) > 0:
				for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if os.path.exists(os.path.join(ADDONS, plugin)):
						do        = ['Launch Addon', 'Remove Addon']
						selected = DIALOG.select("[COLOR %s]Addon is already installed, what would you like to do?[/COLOR]" % COLOR1, do)
						if selected == 0:
							wiz.ebi('RunAddon(%s)' % plugin)
							xbmc.sleep(500)
							return True
						elif selected == 1:
							wiz.cleanHouse(os.path.join(ADDONS, plugin))
							try: wiz.removeFolder(os.path.join(ADDONS, plugin))
							except: pass
							if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you also like to remove the addon_data for:" % COLOR2, "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR %s]Yes, Remove[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Skip[/COLOR][/B]" % COLOR1):
								removeAddonData(plugin)
							else:
								wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, "[COLOR %s]Removing addon; skipping addon_data...[/COLOR]" % COLOR2)
								wiz.log("[Addon Installer] Addon_data for %s not removed: %s" % (plugin, repository))
							wiz.refresh()
							return True
						else:
							return False
					repo = os.path.join(ADDONS, repository)
					if not repository.lower() == 'none' and not os.path.exists(repo):
						wiz.log("Repository not installed, installing it")
						if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you also like to install the [COLOR %s]%s[/COLOR] repository for:" % (COLOR2, COLOR1, repository), "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR %s]Yes, Install[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Skip[/COLOR][/B]" % COLOR1): 
							ver = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': repository})
							if len(ver) > 0:
								repozip = '%s%s-%s.zip' % (repositoryurl, repository, ver[0])
								wiz.log(repozip)
								if KODIV >= 17: wiz.addonDatabase(repository, 1)
								installAddon(repository, repozip)
								wiz.ebi('UpdateAddonRepos()')
								#wiz.ebi('UpdateLocalAddons()')
								wiz.log("Installing Addon from Kodi")
								install = installFromKodi(plugin)
								wiz.log("Install from Kodi: %s" % install)
								if install:
									wiz.refresh()
									return True
							else:
								wiz.log("[Addon Installer] Repository not installed: Unable to grab url! (%s)" % repository)
						else:
							wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, "[COLOR %s]Skipping repo; installing addon...[/COLOR]" % COLOR2)
							wiz.log("[Addon Installer] Repository for %s not installed: %s" % (plugin, repository))
					elif repository.lower() == 'none':
						wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, "[COLOR %s]Installing addon...[/COLOR]" % COLOR2)
						wiz.log("No repository, installing addon")
						pluginid = plugin
						zipurl = url
						installAddon(plugin, url)
						wiz.refresh()
						return True
					else:
						wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, "[COLOR %s]Repo is installed; installing addon...[/COLOR]" % COLOR2)
						wiz.log("Repository installed, installing addon")
						install = installFromKodi(plugin, False)
						if install:
							wiz.refresh()
							return True
					if os.path.exists(os.path.join(ADDONS, plugin)): return True
					ver2 = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': plugin})
					if len(ver2) > 0:
						url = "%s%s-%s.zip" % (url, plugin, ver2[0])
						wiz.log(str(url))
						if KODIV >= 17: wiz.addonDatabase(plugin, 1)
						installAddon(plugin, url)
						wiz.refresh()
					else: 
						wiz.log("no match"); return False
			else: wiz.log("[Addon Installer] Invalid Format")
		else: wiz.log("[Addon Installer] Text File: %s" % ADDONWORKING)
	else: wiz.log("[Addon Installer] Not Enabled.")

def installFromKodi(plugin, over=True):
	if over == True:
		xbmc.sleep(2000)
	#wiz.ebi('InstallAddon(%s)' % plugin)
	wiz.ebi('RunPlugin(plugin://%s)' % plugin)
	if not wiz.whileWindow('yesnodialog'):
		return False
	xbmc.sleep(500)
	if wiz.whileWindow('okdialog'):
		return False
	wiz.whileWindow('progressdialog')
	if os.path.exists(os.path.join(ADDONS, plugin)): return True
	else: return False

def installAddon(name, url):
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip URL![/COLOR]' % (COLOR1, name, COLOR2)); return
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
	urlsplit = url.split('/')
	lib=os.path.join(PACKAGES, urlsplit[-1])
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
	DP.update(0, title,'', '[COLOR %s]Installing Dependencies...[/COLOR]' % COLOR2)
	installed(name)
	installDep(name, DP)
	DP.close()
	wiz.ebi('UpdateAddonRepos()')
	wiz.ebi('UpdateLocalAddons()')
	wiz.refresh()

def installDep(name, DP=None):
	dep=os.path.join(ADDONS,name,'addon.xml')
	if os.path.exists(dep):
		source = open(dep,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		for depends in match:
			if not 'xbmc.python' in depends:
				if not DP == None:
					DP.update(0, '', '[COLOR %s]%s[/COLOR]' % (COLOR1, depends))
				wiz.createTemp(depends)
				# continue
				# dependspath=os.path.join(ADDONS, depends)
				# if not os.path.exists(dependspath):
					# zipname = '%s-%s.zip' % (depends, match2[match.index(depends)])
					# depzip = urljoin("%s%s/" % (MODURL2, depends), zipname)
					# if not wiz.workingURL(depzip) == True:
						# depzip = urljoin(MODURL, '%s.zip' % depends)
						# if not wiz.workingURL(depzip) == True:
							# wiz.createTemp(depends)
							# if KODIV >= 17: wiz.addonDatabase(depends, 1)
							# continue
					# lib=os.path.join(PACKAGES, '%s.zip' % depends)
					# try: os.remove(lib)
					# except: pass
					# DP.update(0, '[COLOR %s][B]Downloading Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends), '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
					# downloader.download(depzip, lib, DP)
					# xbmc.sleep(100)
					# title = '[COLOR %s][B]Installing Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends)
					# DP.update(0, title, '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
					# percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
					# if KODIV >= 17: wiz.addonDatabase(depends, 1)
					# installed(depends)
					# installDep(depends)
					# xbmc.sleep(100)
					# DP.close()

def installed(addon):
	url = os.path.join(ADDONS,addon,'addon.xml')
	if os.path.exists(url):
		try:
			list  = open(url,mode='r'); g = list.read(); list.close()
			name = wiz.parseDOM(g, 'addon', ret='name', attrs = {'id': addon})
			icon  = os.path.join(ADDONS,addon,'icon.png')
			wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, name[0]), '[COLOR %s]Addon Enabled[/COLOR]' % COLOR2, '2000', icon)
		except: pass

def youtubeMenu(url=None):
	if not YOUTUBEFILE == 'http://':
		if url == None:
			YOUTUBEWORKING  = wiz.workingURL(YOUTUBEFILE)
			TEMPYOUTUBEFILE = uservar.YOUTUBEFILE
		else:
			YOUTUBEWORKING  = wiz.workingURL(url)
			TEMPYOUTUBEFILE = url
		if YOUTUBEWORKING == True:
			link = wiz.openURL(TEMPYOUTUBEFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, section, url, icon, fanart, description in match:
					if section.lower() == "yes":
						addDir ("[B]%s[/B]" % name, 'youtube', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						addFile(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[YouTube Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
			addFile('URL for txt file is not valid', '', themeit=THEME2)
			addFile('%s' % YOUTUBEWORKING, '', themeit=THEME3)
	else: wiz.log("[YouTube Menu] No YouTube list added.")
	setView('files', 'viewType')

def maintMenu(view=None):
	on = '[B][COLOR green]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
	autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
	cache       = 'true' if AUTOCACHE      == 'true' else 'false'
	packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
	thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
	maint       = 'true' if SHOWMAINT      == 'true' else 'false'
	includevid  = 'true' if INCLUDEVIDEO   == 'true' else 'false'
	includeall  = 'true' if INCLUDEALL     == 'true' else 'false'
	thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
	if wiz.Grab_Log(True) == False: kodilog = 0
	else: kodilog = errorChecking(wiz.Grab_Log(True), True, True)
	if wiz.Grab_Log(True, True) == False: kodioldlog = 0
	else: kodioldlog = errorChecking(wiz.Grab_Log(True,True), True, True)
	errorsinlog = int(kodilog) + int(kodioldlog)
	errorsfound = str(errorsinlog) + ' Error(s) Found' if errorsinlog > 0 else 'None Found'
	wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR green]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
	if includeall == 'true':
		includecer = 'true'
		includecov = 'true'
		includedea = 'true'
		includeely = 'true'
		includeexo = 'true'
		includeinc = 'true'
		includenep = 'true'
		includeocu = 'true'
		includepla = 'true'
		includepos = 'true'
		includepjm = 'true'
		includespe = 'true'
		includesth = 'true'
		includeukt = 'true'
		includexxx = 'true'
	else:
		includecer = 'true' if INCLUDECERSHO == 'true' else 'false'
		includecov = 'true' if INCLUDECOVEN == 'true' else 'false'
		includedea = 'true' if INCLUDEDEATH   == 'true' else 'false'
		includeely = 'true' if INCLUDEELYSIUM == 'true' else 'false'
		includeexo = 'true' if INCLUDEEXODUS == 'true' else 'false'
		includeinc = 'true' if INCLUDEINCUR == 'true' else 'false'
		includenep = 'true' if INCLUDENEPTUNE == 'true' else 'false'
		includeocu = 'true' if INCLUDEOCULU == 'true' else 'false'
		includepla = 'true' if INCLUDEPLACEN == 'true' else 'false'
		includepos = 'true' if INCLUDEPOSEIDON == 'true' else 'false'
		includepjm = 'true' if INCLUDEPROJM == 'true' else 'false'
		includespe = 'true' if INCLUDESPECTO  == 'true' else 'false'
		includesth = 'true' if INCLUDESTREAMH  == 'true' else 'false'
		includeukt = 'true' if INCLUDEUKTURK == 'true' else 'false'
		includexxx = 'true' if INCLUDEXXXODUS == 'true' else 'false'
	sizepack   = wiz.getSize(PACKAGES)
	sizethumb  = wiz.getSize(THUMBS)
	sizecache  = wiz.getCacheSize()
	totalsize  = sizepack+sizethumb+sizecache
	freq        = ['Always', 'Daily', '3 Days', 'Weekly']
	addDir ('[B]Cleaning Tools[/B]'       ,'maint', 'clean',  icon=ICONMAINT, themeit=THEME1)
	if view == "clean" or SHOWMAINT == 'true': 
		addFile('Total Cleanup: [COLOR %s][B]%s[/B][/COLOR]' % (COLOR2, wiz.convertSize(totalsize))    ,'fullclean',       icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Cache: [COLOR %s][B]%s[/B][/COLOR]' % (COLOR2, wiz.convertSize(sizecache))      ,'clearcache',      icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Packages: [COLOR %s][B]%s[/B][/COLOR]' % (COLOR2, wiz.convertSize(sizepack))    ,'clearpackages',   icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Thumbnails: [COLOR %s][B]%s[/B][/COLOR]' % (COLOR2, wiz.convertSize(sizethumb)) ,'clearthumb',      icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Old Thumbnails', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)
		addFile('Purge Databases',                'purgedb',         icon=ICONMAINT, themeit=THEME3)
		addFile('Fresh Start',                    'freshstart',      icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Addon Tools[/B]',       'maint', 'addon',  icon=ICONMAINT, themeit=THEME1)
	if view == "addon" or SHOWMAINT == 'true': 
		addFile('Remove Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
		addDir ('Remove Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
		addDir ('Enable/Disable Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
		addFile('Enable/Disable Adult Addons',    'toggleadult',     icon=ICONMAINT, themeit=THEME3)
		addFile('Force Update Addons',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
		addFile('Hide Passwords on Keyboard Entry',   'hidepassword',   icon=ICONMAINT, themeit=THEME3)
		addFile('Unhide Passwords on Keyboard Entry', 'unhidepassword', icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Misc Maintenance[/B]'     ,'maint', 'misc',   icon=ICONMAINT, themeit=THEME1)
	if view == "misc" or SHOWMAINT == 'true': 
		addFile('Kodi 17 Fix (Enable ALL Addons)','kodi17fix',       icon=ICONMAINT, themeit=THEME3)
		addFile('Reload Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
		addFile('Reload Profile',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)
		addFile('Force Close Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)
		addFile('Upload Kodi Log',                'uploadlog',       icon=ICONMAINT, themeit=THEME3)
		addFile('View Errors in Log: [COLOR %s]%s[/COLOR]' % (COLOR2, (errorsfound)), 'viewerrorlog',    icon=ICONMAINT, themeit=THEME3)
		addFile('View Kodi Log Files',            'viewlog',         icon=ICONMAINT, themeit=THEME3)
		addFile('View Wizard Log File',           'viewwizlog',      icon=ICONMAINT, themeit=THEME3)
		addFile('Clear Wizard Log File%s' % wizlogsize,'clearwizlog',     icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Backup/Restore[/B]'     ,'maint', 'backup',   icon=ICONMAINT, themeit=THEME1)
	if view == "backup" or SHOWMAINT == 'true':
		addFile('Clean Up Backup Folder',         'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
		addFile('BackUp Location: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
		addFile('[Back Up]: Build',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: GuiFix',              'backupgui',       icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: Theme',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: Local Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: Local GuiFix',        'restoregui',      icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: Local Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External Build',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External GuiFix',     'restoreextgui',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External Addon_data', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
	# addDir ('[B]Network Tools[/B]'		 ,'maint', 'network', icon=ICONMAINT, themeit=THEME1)
	# if view == "network" or SHOWMAINT == 'true':
		# addFile('SpeedTest',                      'speedtest',     icon=ICONMAINT,   themeit=THEME3)
	addDir ('[B]System Tweaks/Fixes[/B]',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
	if view == "tweaks" or SHOWMAINT == 'true': 
		if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
			addDir ('Advanced Settings',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
		else: 
			if os.path.exists(ADVANCED):
				addFile('View Current Advanced Settings',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
				addFile('Remove Current Advanced Settings', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
			addFile('Quick Configure Advanced Settings',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)
		addFile('Apply Youtube Fix',  'ytfix',    icon=ICONMAINT, themeit=THEME3)
		addFile('Scan for Broken Sources',  'checksources',    icon=ICONMAINT, themeit=THEME3)
		addFile('Scan for Broken Repositories',   'checkrepos',      icon=ICONMAINT, themeit=THEME3)
		addFile('Fix Addons Not Updating',        'fixaddonupdate',  icon=ICONMAINT, themeit=THEME3)
		addFile('Remove Non-Ascii Filenames',     'asciicheck',      icon=ICONMAINT, themeit=THEME3)
		addFile('Convert Paths to Special',       'convertpath',     icon=ICONMAINT, themeit=THEME3)
	addFile('Show [B]ALL[/B] [I][COLOR %s]([/COLOR]DOGE[COLOR %s])[/COLOR][/I]  Submenus: %s' % (COLOR1, COLOR1, maint.replace('true',on).replace('false',off)), 'togglesetting', 'showmaint', icon=ICONMAINT, themeit=THEME2)
	addDir ('[B][COLOR red]<<< RETURN TO MAIN MENU[/COLOR][/B]', icon=ICONMAINT, themeit=THEME3)
	#addDir ('[B][COLOR %s]<<< [COLOR %s]RETURN [COLOR %s]TO [COLOR %s]MAIN [COLOR %s]MENU[/COLOR][/B]' % (COLOR1, COLOR2, COLOR1, COLOR2, COLOR1), icon=ICONMAINT, themeit=THEME3)
	addFile('[B]Third Party Wizards:[/B] %s' % thirdparty.replace('true',on).replace('false',off) ,'togglesetting', 'enable3rd', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
	if thirdparty == 'true':
		first = THIRD1NAME if not THIRD1NAME == '' else 'Not Set'
		secon = THIRD2NAME if not THIRD2NAME == '' else 'Not Set'
		third = THIRD3NAME if not THIRD3NAME == '' else 'Not Set'
		addFile('Edit Third Party Wizard 1: [COLOR %s]%s[/COLOR]' % (COLOR2, first), 'editthird', '1', icon=ICONMAINT, themeit=THEME3)
		addFile('Edit Third Party Wizard 2: [COLOR %s]%s[/COLOR]' % (COLOR2, secon), 'editthird', '2', icon=ICONMAINT, themeit=THEME3)
		addFile('Edit Third Party Wizard 3: [COLOR %s]%s[/COLOR]' % (COLOR2, third), 'editthird', '3', icon=ICONMAINT, themeit=THEME3)
	addFile('Auto Clean', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
	addFile('Auto Cleanup on Startup: %s' % autoclean.replace('true',on).replace('false',off), 'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME3)
	if autoclean == 'true':
		addFile('[COLOR %s]   ---[/COLOR] Auto Clean Frequency: [B][COLOR %s]%s[/COLOR][/B]' % (COLOR2, COLOR2, freq[AUTOFREQ]), 'changefreq', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Clear Cache on Startup: %s' % (COLOR2, cache.replace('true',on).replace('false',off)), 'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Clear Packages on Startup: %s' % (COLOR2, packages.replace('true',on).replace('false',off)), 'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Clear Old Thumbs on Startup: %s' % (COLOR2, thumbs.replace('true',on).replace('false',off)), 'togglesetting', 'clearthumbs', icon=ICONMAINT, themeit=THEME3)
	addFile('Clear Video Cache', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
	addFile('Include Video Cache in Clear Cache: %s' % includevid.replace('true',on).replace('false',off), 'togglecache', 'includevideo', icon=ICONMAINT, themeit=THEME3)
	if includevid == 'true':
		addFile('[COLOR %s]   ---[/COLOR] Include All Video Addons: %s' % (COLOR2, includeall.replace('true',on).replace('false',off)), 'togglecache', 'includeall', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Cerebro Showbox: %s' % (COLOR2, includecer.replace('true',on).replace('false',off)), 'togglecache', 'includecerebroshow', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Covenant: %s' % (COLOR2, includecov.replace('true',on).replace('false',off)), 'togglecache', 'includecovenant', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Death Streams: %s' % (COLOR2, includedea.replace('true',on).replace('false',off)), 'togglecache', 'includedeathstreams', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Elysium: %s' % (COLOR2, includeely.replace('true',on).replace('false',off)), 'togglecache', 'includeelysium', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Exodus: %s' % (COLOR2, includeexo.replace('true',on).replace('false',off)), 'togglecache', 'includeexodus', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Incursion: %s' % (COLOR2, includeinc.replace('true',on).replace('false',off)), 'togglecache', 'includeincursion', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Neptune Rising: %s' % (COLOR2, includenep.replace('true',on).replace('false',off)), 'togglecache', 'includeneptune', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Oculus: %s' % (COLOR2, includeocu.replace('true',on).replace('false',off)), 'togglecache', 'includeoculus', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Placenta: %s' % (COLOR2, includepla.replace('true',on).replace('false',off)), 'togglecache', 'includeplacenta', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Poseidon: %s' % (COLOR2, includepos.replace('true',on).replace('false',off)), 'togglecache', 'includeposeidon', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Project M: %s' % (COLOR2, includepjm.replace('true',on).replace('false',off)), 'togglecache', 'includeprojectm', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include Specto: %s' % (COLOR2, includespe.replace('true',on).replace('false',off)), 'togglecache', 'includespecto', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include StreamHub: %s' % (COLOR2, includesth.replace('true',on).replace('false',off)), 'togglecache', 'includestreamhub', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include UK Turk Playlists: %s' % (COLOR2, includeukt.replace('true',on).replace('false',off)), 'togglecache', 'includeukturk', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Include XXX-O-DUS: %s' % (COLOR2, includexxx.replace('true',on).replace('false',off)), 'togglecache', 'includexxxodus', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Enable All Video Addons' % COLOR2, 'togglecache', 'true', icon=ICONMAINT, themeit=THEME3)
		addFile('[COLOR %s]   ---[/COLOR] Disable All Video Addons' % COLOR2, 'togglecache', 'false', icon=ICONMAINT, themeit=THEME3)
	setView('files', 'viewType')

def advancedWindow(url=None):
	if not ADVANCEDFILE == 'http://':
		if url == None:
			ADVANCEDWORKING = wiz.workingURL(ADVANCEDFILE)
			TEMPADVANCEDFILE = uservar.ADVANCEDFILE
		else:
			ADVANCEDWORKING  = wiz.workingURL(url)
			TEMPADVANCEDFILE = url
		addFile('Quick Configure Advanced Settings', 'autoadvanced', icon=ICONMAINT, themeit=THEME3)
		if os.path.exists(ADVANCED): 
			addFile('View Current Advanced Settings', 'currentsettings', icon=ICONMAINT, themeit=THEME3)
			addFile('Remove Current Advanced Settings', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
		if ADVANCEDWORKING == True:
			if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONMAINT, themeit=THEME3)
			link = wiz.openURL(TEMPADVANCEDFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, section, url, icon, fanart, description in match:
					if section.lower() == "yes":
						addDir ("[B]%s[/B]" % name, 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						addFile(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[Advanced Settings] ERROR: Invalid Format.")
		else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
	else: wiz.log("[Advanced Settings] not Enabled")

def writeAdvanced(name, url):
	ADVANCEDWORKING = wiz.workingURL(url)
	if ADVANCEDWORKING == True:
		if os.path.exists(ADVANCED): choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to overwrite your current Advanced Settings with [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR %s]Overwrite[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Cancel[/COLOR][/B]" % COLOR1)
		else: choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to download and install [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR %s]Install[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Cancel[/COLOR][/B]" % COLOR1)

		if choice == 1:
			file = wiz.openURL(url)
			f = open(ADVANCED, 'w'); 
			f.write(file)
			f.close()
			DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s][COLOR %s]advancedSettings.xml[/COLOR] file has been successfully written.' % (COLOR2, COLOR1), 'Once you click OK it will Force Close Kodi![/COLOR]' % COLOR1)
			wiz.killxbmc(True)
		else: 
			wiz.log("[Advanced Settings] install canceled!")
			wiz.LogNotify('[COLOR %s]Advanced Settings[/COLOR]' % COLOR1, "[COLOR %s]Download Cancelled![/COLOR]" % COLOR2)
			return
	else: 
		wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
		wiz.LogNotify('[COLOR %s]Advanced Settings[/COLOR]' % COLOR1, "[COLOR %s]URL Not Working![/COLOR]" % COLOR2)

def viewAdvanced():
	f = open(ADVANCED)
	a = f.read().replace('\t', '    ')
	wiz.TextBox("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s[/COLOR]" % (COLOR2, a))
	f.close()

def removeAdvanced():
	if os.path.exists(ADVANCED):
		choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Are you sure you wish to remove your current [COLOR %s]advancedSettings.xml[/COLOR] file?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR %s]Remove Settings[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Keep Settings[/COLOR][/B]" % COLOR1)
		if choice == 1:
			wiz.removeFile(ADVANCED)
		else: 
			wiz.LogNotify('[COLOR %s]Remove Current Advanced Settings[/COLOR]' % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
			sys.exit()
	else: LogNotify("[COLOR %s]Remove Current Advanced Settings[/COLOR]" % COLOR1, "[COLOR %s][COLOR %s]advancedSettings.xml[/COLOR] file NOT found![/COLOR]" % (COLOR2, COLOR1))

def showAutoAdvanced():
	notify.autoConfig()

def getIP():
	site  = 'http://whatismyipaddress.com/'
	if not wiz.workingURL(site): return 'Unknown', 'Unknown', 'Unknown'
	page  = wiz.openURL(site).replace('\n','').replace('\r','')
	if not 'Access Denied' in page:
		ipmatch   = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(page)
		ipfinal   = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
		details   = re.compile('"font-size:14px;">(.+?)</td>').findall(page)
		provider  = details[0] if (len(details) > 0) else 'Unknown'
		location  = details[1]+', '+details[2]+', '+details[3] if (len(details) > 2) else 'Unknown'
		return ipfinal, provider, location
	else: return 'Unknown', 'Unknown', 'Unknown'

def systemInfo():
	infoLabel = ['System.FriendlyName', 
				 'System.BuildVersion', 
				 'System.CpuUsage',
				 'System.ScreenMode',
				 'Network.IPAddress',
				 'Network.MacAddress',
				 'System.Uptime',
				 'System.TotalUptime',
				 'System.FreeSpace',
				 'System.UsedSpace',
				 'System.TotalSpace',
				 'System.Memory(free)',
				 'System.Memory(used)',
				 'System.Memory(total)']
	data      = []; x = 0
	for info in infoLabel:
		temp = wiz.getInfo(info)
		y = 0
		while temp == "Busy" and y < 10:
			temp = wiz.getInfo(info); y += 1; wiz.log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
		data.append(temp)
		x += 1
	storage_free  = data[8] if 'Una' in data[8] else wiz.convertSize(int(float(data[8][:-8]))*1024*1024)
	storage_used  = data[9] if 'Una' in data[9] else wiz.convertSize(int(float(data[9][:-8]))*1024*1024)
	storage_total = data[10] if 'Una' in data[10] else wiz.convertSize(int(float(data[10][:-8]))*1024*1024)
	ram_free      = wiz.convertSize(int(float(data[11][:-2]))*1024*1024)
	ram_used      = wiz.convertSize(int(float(data[12][:-2]))*1024*1024)
	ram_total     = wiz.convertSize(int(float(data[13][:-2]))*1024*1024)
	exter_ip, provider, location = getIP()
	
	picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []
	
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername == 'packages': continue
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			prov   = re.compile("<provides>(.+?)</provides>").findall(a)
			if len(prov) == 0:
				if foldername.startswith('skin'): skins.append(foldername)
				if foldername.startswith('repo'): repos.append(foldername)
				else: scripts.append(foldername)
			elif not (prov[0]).find('executable') == -1: programs.append(foldername)
			elif not (prov[0]).find('video') == -1: video.append(foldername)
			elif not (prov[0]).find('audio') == -1: music.append(foldername)
			elif not (prov[0]).find('image') == -1: picture.append(foldername)

	addFile('[B]Media Center Info:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Name:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[0]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Version:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[1]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Platform:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, wiz.platform().title()), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]CPU Usage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[2]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Screen Mode:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[3]), '', icon=ICONMAINT, themeit=THEME3)
	
	addFile('[B]Uptime:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Current Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[6]), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[7]), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]Local Storage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Used Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_free), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Free Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_used), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_total), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]RAM Usage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Used Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_free), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Free Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_used), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_total), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]Network:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Local IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[4]), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, exter_ip), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Provider:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, provider), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Location:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, location), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]MacAddress:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[5]), '', icon=ICONMAINT, themeit=THEME2)
	
	totalcount = len(picture) + len(music) + len(video) + len(programs) + len(scripts) + len(skins) + len(repos) 
	addFile('[B]Addons ([COLOR %s]%s[/COLOR]):[/B]' % (COLOR1, totalcount), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Video Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(video))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Program Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(programs))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Music Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(music))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Picture Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(picture))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(repos))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Skins:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(skins))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Scripts/Modules:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(scripts))), '', icon=ICONMAINT, themeit=THEME2)

def saveMenu():
	on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
	trakt      = 'true' if KEEPTRAKT     == 'true' else 'false'
	real       = 'true' if KEEPREAL      == 'true' else 'false'
	login      = 'true' if KEEPLOGIN     == 'true' else 'false'
	sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
	advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
	profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
	favourites = 'true' if KEEPFAVS      == 'true' else 'false'
	repos      = 'true' if KEEPREPOS     == 'true' else 'false'
	super      = 'true' if KEEPSUPER     == 'true' else 'false'
	whitelist  = 'true' if KEEPWHITELIST == 'true' else 'false'

	addDir ('Keep My Trakt Info',               'trakt',                icon=ICONTRAKT, themeit=THEME1)
	addDir ('Keep My Real Debrid Info',              'realdebrid',           icon=ICONREAL,  themeit=THEME1)
	addDir ('Keep My Login Info',               'login',                icon=ICONLOGIN, themeit=THEME1)
	addFile('Import ALL Account Info',              'managedata', 'import', icon=ICONSAVE,  themeit=THEME1)
	addFile('Export ALL Account Info',              'managedata', 'export', icon=ICONSAVE,  themeit=THEME1)
	addFile('- Click to Toggle Settings -', '', themeit=THEME3)
	addFile('Save My Trakt Info: %s' % trakt.replace('true',on).replace('false',off)                       ,'togglesetting', 'keeptrakt',      icon=ICONTRAKT, themeit=THEME1)
	addFile('Save My Real Debrid Info: %s' % real.replace('true',on).replace('false',off)                  ,'togglesetting', 'keepdebrid',     icon=ICONREAL,  themeit=THEME1)
	addFile('Save My Login Info: %s' % login.replace('true',on).replace('false',off)                  ,'togglesetting', 'keeplogin',      icon=ICONLOGIN, themeit=THEME1)
	addFile('Keep My Sources: %s' % sources.replace('true',on).replace('false',off)           ,'togglesetting', 'keepsources',    icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep My Profiles: %s' % profiles.replace('true',on).replace('false',off)         ,'togglesetting', 'keepprofiles',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep Advanced Settings: %s' % advanced.replace('true',on).replace('false',off) ,'togglesetting', 'keepadvanced',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep My Favourites: %s' % favourites.replace('true',on).replace('false',off)     ,'togglesetting', 'keepfavourites', icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep Super Favourites: %s' % super.replace('true',on).replace('false',off)            ,'togglesetting', 'keepsuper',      icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep My Installed Repos: %s' % repos.replace('true',on).replace('false',off)           ,'togglesetting', 'keeprepos',      icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep My WhiteList: %s' % whitelist.replace('true',on).replace('false',off)        ,'togglesetting', 'keepwhitelist',  icon=ICONSAVE,  themeit=THEME1)
	if whitelist == 'true':
		addFile('Create/Edit My WhiteList',        'whitelist', 'edit',   icon=ICONSAVE,  themeit=THEME1)
		addFile('View My WhiteList',        'whitelist', 'view',   icon=ICONSAVE,  themeit=THEME1)
		addFile('Clear My WhiteList',       'whitelist', 'clear',  icon=ICONSAVE,  themeit=THEME1)
		addFile('Import My WhiteList',      'whitelist', 'import', icon=ICONSAVE,  themeit=THEME1)
		addFile('Export My WhiteList',      'whitelist', 'export', icon=ICONSAVE,  themeit=THEME1)
	setView('files', 'viewType')

def traktMenu():
	trakt = '[COLOR green]ON[/COLOR]' if KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(TRAKTSAVE) if not TRAKTSAVE == '' else "Trakt Info hasn't been saved yet."
	addFile('[I]Create a FREE Account at [COLOR %s]http://trakt.tv[/I][/COLOR]' % COLOR1, '', icon=ICONTRAKT, themeit=THEME2)
	addFile('Save My Trakt Info: %s' % trakt, 'togglesetting', 'keeptrakt', icon=ICONTRAKT, themeit=THEME3)
	if KEEPTRAKT == 'true': addFile('Last Save: [COLOR %s]%s[/COLOR]' % (COLOR1, str(last)), '', icon=ICONTRAKT, themeit=THEME2)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONTRAKT, themeit=THEME3)
	
	for trakt in traktit.ORDER:
		name   = TRAKTID[trakt]['name']
		path   = TRAKTID[trakt]['path']
		saved  = TRAKTID[trakt]['saved']
		file   = TRAKTID[trakt]['file']
		user   = wiz.getS(saved)
		auser  = traktit.traktUser(trakt)
		icon   = TRAKTID[trakt]['icon']   if os.path.exists(path) else ICONTRAKT
		fanart = TRAKTID[trakt]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Trakt', trakt)
		menu2 = createMenu('save', 'Trakt', trakt)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=trakt)' %   (ADDON_ID, trakt)))
		
		addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME2)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Save All Trakt Info',          'savetrakt',    'all', icon=ICONTRAKT,  themeit=THEME2)
	addFile('Recover All Saved Trakt Info', 'restoretrakt', 'all', icon=ICONTRAKT,  themeit=THEME2)
	addFile('Import Trakt Info',            'importtrakt',  'all', icon=ICONTRAKT,  themeit=THEME2)
	addFile('Clear All Saved Trakt Info',   'cleartrakt',   'all', icon=ICONTRAKT,  themeit=THEME2)
	addFile('Clear All Addon Data',         'addontrakt',   'all', icon=ICONTRAKT,  themeit=THEME2)
	setView('files', 'viewType')

def realMenu():
	real = '[COLOR green]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(REALSAVE) if not REALSAVE == '' else "Real Debrid Info hasn't been saved yet."
	addFile('[I][COLOR %s]http://real-debrid.com[/COLOR] is a PAID service.[/I]' % COLOR1, '', icon=ICONREAL, themeit=THEME2)
	addFile('Save My Real Debrid Info: %s' % real, 'togglesetting', 'keepdebrid', icon=ICONREAL, themeit=THEME3)
	if KEEPREAL == 'true': addFile('Last Save: [COLOR %s]%s[/COLOR]' % (COLOR1, str(last)), '', icon=ICONREAL, themeit=THEME2)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONREAL, themeit=THEME3)
	
	for debrid in debridit.ORDER:
		name   = DEBRIDID[debrid]['name']
		path   = DEBRIDID[debrid]['path']
		saved  = DEBRIDID[debrid]['saved']
		file   = DEBRIDID[debrid]['file']
		user   = wiz.getS(saved)
		auser  = debridit.debridUser(debrid)
		icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else ICONREAL
		fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Debrid', debrid)
		menu2 = createMenu('save', 'Debrid', debrid)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))
		
		addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME2)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Save All Real Debrid Info',          'savedebrid',    'all', icon=ICONREAL,  themeit=THEME2)
	addFile('Recover All Saved Real Debrid Info', 'restoredebrid', 'all', icon=ICONREAL,  themeit=THEME2)
	addFile('Import Real Debrid Info',            'importdebrid',  'all', icon=ICONREAL,  themeit=THEME2)
	addFile('Clear All Saved Real Debrid Info',   'cleardebrid',   'all', icon=ICONREAL,  themeit=THEME2)
	addFile('Clear All Addon Data',               'addondebrid',   'all', icon=ICONREAL,  themeit=THEME2)
	setView('files', 'viewType')

def loginMenu():
	login = '[COLOR green]ON[/COLOR]' if KEEPLOGIN == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(LOGINSAVE) if not LOGINSAVE == '' else "Login Info hasn't been saved yet."
	addFile('[I]Several of these addons are [COLOR %s]PAID[/COLOR] services.[/I]' % COLOR1, '', icon=ICONLOGIN, themeit=THEME2)
	addFile('Save My Login Info: %s' % login, 'togglesetting', 'keeplogin', icon=ICONLOGIN, themeit=THEME3)
	if KEEPLOGIN == 'true': addFile('Last Save: [COLOR %s]%s[/COLOR]' % (COLOR1, str(last)), '', icon=ICONLOGIN, themeit=THEME2)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONLOGIN, themeit=THEME3)

	for login in loginit.ORDER:
		name   = LOGINID[login]['name']
		path   = LOGINID[login]['path']
		saved  = LOGINID[login]['saved']
		file   = LOGINID[login]['file']
		user   = wiz.getS(saved)
		auser  = loginit.loginUser(login)
		icon   = LOGINID[login]['icon']   if os.path.exists(path) else ICONLOGIN
		fanart = LOGINID[login]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Login', login)
		menu2 = createMenu('save', 'Login', login)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=login)' %   (ADDON_ID, login)))
		
		addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME2)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authlogin', login, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authlogin', login, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importlogin', login, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savelogin', login, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Save All Login Info',          'savelogin',    'all', icon=ICONLOGIN,  themeit=THEME2)
	addFile('Recover All Saved Login Info', 'restorelogin', 'all', icon=ICONLOGIN,  themeit=THEME2)
	addFile('Import Login Info',            'importlogin',  'all', icon=ICONLOGIN,  themeit=THEME2)
	addFile('Clear All Saved Login Info',   'clearlogin',   'all', icon=ICONLOGIN,  themeit=THEME2)
	addFile('Clear All Addon Data',         'addonlogin',   'all', icon=ICONLOGIN,  themeit=THEME2)
	setView('files', 'viewType')

def fixUpdate():
	if KODIV < 17: 
		dbfile = os.path.join(DATABASE, wiz.latestDB('Addons'))
		try:
			os.remove(dbfile)
		except Exception, e:
			wiz.log("Unable to remove %s, Purging DB" % dbfile)
			wiz.purgeDb(dbfile)
	else:
		xbmc.log("Requested Addons.db to be removed, but it doesn't work in Kod17.")

def removeAddonMenu():
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	addonnames = []; addonids = []
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		elif foldername in DEFAULTPLUGINS: continue
		elif foldername == 'packages': continue
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			match  = wiz.parseDOM(a, 'addon', ret='id')

			addid  = foldername if len(match) == 0 else match[0]
			try: 
				add = xbmcaddon.Addon(id=addid)
				addonnames.append(add.getAddonInfo('name'))
				addonids.append(addid)
			except:
				pass
	if len(addonnames) == 0:
		wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Found![/COLOR]" % COLOR2)
		sys.exit()
	if KODIV > 16:
		selected = DIALOG.multiselect("[COLOR %s]Select the addons you wish to remove:[/COLOR]" % COLOR1, addonnames)
	else:
		selected = []; choice = 0
		tempaddonnames = ["-- Click here to Continue --"] + addonnames
		while choice == 0:
			choice = DIALOG.select("[COLOR %s]Select the addons you wish to remove:[/COLOR]" % COLOR1, tempaddonnames)
			if choice == -1: 
				wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
				sys.exit()
			elif choice == 0: 
				wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
				sys.exit()
			else: 
				choice2 = (choice-1)
				if choice2 in selected:
					selected.remove(choice2)
					tempaddonnames[choice] = addonnames[choice2]
				else:
					selected.append(choice2)
					tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
	if selected == None: 
			wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
			sys.exit()
	if len(selected) > 0:
		wiz.addonUpdates('set')
		for addon in selected:
			removeAddon(addonids[addon], addonnames[addon], True)
		xbmc.sleep(500)
		if INSTALLMETHOD == 1: todo = 1
		elif INSTALLMETHOD == 2: todo = 0
		else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to [COLOR %s]Force Close[/COLOR] Kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
		if todo == 1: wiz.reloadFix('remove addon')
		else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
	else: wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)

def removeAddonDataMenu():
	if os.path.exists(ADDOND):
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		fold = glob.glob(os.path.join(ADDOND, '*/'))
		for folder in sorted(fold, key = lambda x: x):
			foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
			icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
			fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
			folderdisplay = foldername
			replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR green][SCRIPT] [/COLOR]', 'service.':'[COLOR green][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
			for rep in replace:
				folderdisplay = folderdisplay.replace(rep, replace[rep])
			if foldername in EXCLUDES: folderdisplay = '[COLOR green][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
			else: folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
			addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
	else:
		addFile('No Addon data folder found.', '', themeit=THEME3)
	setView('files', 'viewType')

def enableAddons():
	addFile("[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]", '', icon=ICONMAINT)
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	x = 0
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		if foldername in DEFAULTPLUGINS: continue
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			x += 1
			fold   = folder.replace(ADDONS, '')[1:-1]
			f      = open(addonxml)
			a      = f.read().replace('\n','').replace('\r','').replace('\t','')
			match  = wiz.parseDOM(a, 'addon', ret='id')
			match2 = wiz.parseDOM(a, 'addon', ret='name')
			try:
				pluginid = match[0]
				name = match2[0]
			except:
				continue
			try:
				add    = xbmcaddon.Addon(id=pluginid)
				state  = "[COLOR green][Enabled][/COLOR]"
				goto   = "false"
			except:
				state  = "[COLOR red][Disabled][/COLOR]"
				goto   = "true"
				pass
			icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
			fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
			addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
			f.close()
	if x == 0:
		addFile("No Addons Found to Enable or Disable!", '', icon=ICONMAINT)
	setView('files', 'viewType')

def changefreq():
	freq        = ['Every Startup', 'Every Day', 'Every Three Days', 'Every Week']
	change     = DIALOG.select("[COLOR %s]Select frequency of Auto Clean on Startup:[/COLOR]" % COLOR1, freq)
	if not change == -1: 
		wiz.setS('autocleanfreq', str(change))
		wiz.LogNotify('[COLOR %s]Auto Cleanup[/COLOR]' % COLOR1, '[COLOR %s]Frequency Now: [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, freq[change]))
	else: 
		wiz.LogNotify('[COLOR %s]Auto Cleanup[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
		sys.exit()

def developer():
	#addFile('Convert Text Files to 0.1.7',         'converttext',           themeit=THEME1)
	addFile('Create QR Code',                      'createqr',              themeit=THEME1)
	addFile('Test Notifications',                  'testnotify',            themeit=THEME1)
	addFile('Test Build Update',                         'testupdate',            themeit=THEME1)
	addFile('Test First Run',                      'testfirst',             themeit=THEME1)
	addFile('Test First Run Settings',             'testfirstrun',          themeit=THEME1)
	addFile('Test Forks',             'testapk',          themeit=THEME1)
	
	setView('files', 'viewType')

###########################
###### Build Install ######
###########################
def buildWizard(name, type, theme=None, over=False):
	if over == False:
		testbuild = wiz.checkBuild(name, 'url')
		if testbuild == False:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Unable to find build![/COLOR]" % COLOR2)
			return
		testworking = wiz.workingURL(testbuild)
		if testworking == False:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Build Zip Error: %s[/COLOR]" % (COLOR2, testworking))
			return
	if type == 'gui':
		if name == BUILDNAME:
			if over == True: yes = 1
			else: yes = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to apply the GuiFix for:' % COLOR2, '[COLOR %s]%s[/COLOR]?[/COLOR]' % (COLOR1, name), nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Apply Fix[/COLOR][/B]' % COLOR2)
		else: 
			yes = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "[COLOR %s][COLOR %s]%s[/COLOR] build is not currently installed." % (COLOR2, COLOR1, name), "Would you like to apply the GuiFix anyway?[/COLOR]", nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Apply Fix[/COLOR][/B]' % COLOR2)
		if yes:
			buildzip = wiz.checkBuild(name,'gui')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Invalid Zip URL![/COLOR]' % COLOR2); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading GuiFix:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
			lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
			DP.update(0, title, '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
			extract.all(lib,USERDATA,DP, title=title)
			DP.close()
			wiz.defaultSkin()
			wiz.lookandFeelData('save')
			if INSTALLMETHOD == 1: todo = 1
			elif INSTALLMETHOD == 2: todo = 0
			else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]The GuiFix has been installed." % COLOR2, "[COLOR %s]Would you like to Reload the Profile or Force Close Kodi?[/COLOR]" % COLOR1, yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
			if todo == 1: wiz.reloadFix()
			else: DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]To save changes you need to Force Close Kodi. Press OK to Force Close Kodi now.[/COLOR]" % COLOR2); wiz.killxbmc('true')
		else:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Cancelled![/COLOR]' % COLOR2)
	elif type == 'fresh':
		freshStart(name)
	elif type == 'normal':
		if url == 'normal':
			if KEEPTRAKT == 'true':
				traktit.autoUpdate('all')
				wiz.setS('traktlastsave', str(THREEDAYS))
			if KEEPREAL == 'true':
				debridit.autoUpdate('all')
				wiz.setS('debridlastsave', str(THREEDAYS))
			if KEEPLOGIN == 'true':
				loginit.autoUpdate('all')
				wiz.setS('loginlastsave', str(THREEDAYS))
		temp_kodiv = int(KODIV); buildv = int(float(wiz.checkBuild(name, 'kodi')))
		if not temp_kodiv == buildv: 
			if temp_kodiv == 16 and buildv <= 15: warning = False
			else: warning = True
		else: warning = False
		if warning == True:
			yes_pressed = DIALOG.yesno("[COLOR %s]%s -[/COLOR] [COLOR red]WARNING!![/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]There is a chance that the skin will not appear correctly when installing a Kodi %s build on Kodi %s!" % (COLOR2, wiz.checkBuild(name, 'kodi'), KODIV), "[COLOR %s]Would you still like to install the: [COLOR %s]%s v%s[/COLOR] build?[/COLOR]" % (COLOR1, COLOR2, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Yes, Install[/COLOR][/B]' % COLOR2)
		else:
			if not over == False: yes_pressed = 1
			else: yes_pressed = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to Download and Install:' % COLOR2, '[COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Yes, Install[/COLOR][/B]' % COLOR2)
		if yes_pressed:
			wiz.clearS('build')
			buildzip = wiz.checkBuild(name, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Invalid Zip URL![/COLOR]' % COLOR2); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')),'', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version'))
			DP.update(0, title, '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
			percent, errors, error = extract.all(lib,HOME,DP, title=title)
			if int(float(percent)) > 0:
				wiz.fixmetas()
				wiz.lookandFeelData('save')
				wiz.defaultSkin()
				#wiz.addonUpdates('set')
				wiz.setS('buildname', name)
				wiz.setS('buildversion', wiz.checkBuild( name,'version'))
				wiz.setS('buildtheme', '')
				wiz.setS('latestversion', wiz.checkBuild( name,'version'))
				wiz.setS('lastbuildcheck', str(NEXTCHECK))
				wiz.setS('installed', 'true')
				wiz.setS('extract', str(percent))
				wiz.setS('errors', str(errors))
				wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
				try: os.remove(lib)
				except: pass
				if int(float(errors)) > 0:
					yes=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s][COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild( name,'version')), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the Errors?[/COLOR]', nolabel='[B][COLOR %s]No Thanks[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]View Errors[/COLOR][/B]' % COLOR2)
					if yes:
						if isinstance(errors, unicode):
							error = error.encode('utf-8')
						wiz.TextBox("[COLOR %s]Build Install Errors:[/COLOR]" % COLOR1, error)
				DP.close()
				themefile = wiz.themeCount(name)
				if not themefile == False:
					buildWizard(name, 'theme')
				if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
				if INSTALLMETHOD == 1: todo = 1
				elif INSTALLMETHOD == 2: todo = 0
				else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to [COLOR %s]Force Close[/COLOR] Kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
				if todo == 1: wiz.reloadFix()
				else: wiz.killxbmc(True)
			else:
				if isinstance(errors, unicode):
					error = error.encode('utf-8')
				wiz.TextBox("[COLOR %s]%s: Error Installing Build[/COLOR]" % (COLOR1, ADDONTITLE), error)
		else:
			wiz.LogNotify("[COLOR %s]Standard Install[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
	elif type == 'theme':
		if theme == None:
			themefile = wiz.checkBuild(name, 'theme')
			themelist = []
			if not themefile == 'http://' and wiz.workingURL(themefile) == True:
				themelist = wiz.themeCount(name, False)
				if len(themelist) > 0:
					if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]The Build [COLOR %s]%s[/COLOR] comes with [COLOR %s]%s[/COLOR] different themes" % (COLOR2, COLOR1, name, COLOR1, len(themelist)), "Would you like to install one now?[/COLOR]", yeslabel="[B][COLOR %s]Install Theme[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Cancel Themes[/COLOR][/B]" % COLOR1):
						wiz.log("Theme List: %s " % str(themelist))
						ret = DIALOG.select("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), themelist)
						wiz.log("Theme install selected: %s" % ret)
						if not ret == -1: theme = themelist[ret]; installtheme = True
						else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
			else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: None Found![/COLOR]' % COLOR2)
		else: installtheme = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to install the theme:' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, theme), 'for [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), yeslabel="[B][COLOR %s]Install Theme[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Cancel Themes[/COLOR][/B]" % COLOR1)
		if installtheme:
			themezip = wiz.checkTheme(name, theme, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(themezip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Invalid Zip URL![/COLOR]' % COLOR2); return False
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme), '', '[COLOR %s]Please Wait...[/COLOR]' %COLOR2)
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(themezip, lib, DP)
			xbmc.sleep(500)
			DP.update(0,"", "[COLOR %s]Installing %s [/COLOR]" % (COLOR2, name))
			test = False
			if url not in ["fresh", "normal"]:
				test = testTheme(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
				test2 = testGui(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
				if test == True:
					wiz.lookandFeelData('save')
					skin     = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
					gotoskin = xbmc.getSkinDir()
					#if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Installing the theme [COLOR %s]%s[/COLOR] requires the skin to be swaped back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, theme, COLOR1, skin[5:]), "Would you like to switch the skin?[/COLOR]", yeslabel="[B][COLOR %s]Switch Skin[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Switch[/COLOR][/B]" % COLOR1):
					skinSwitch.swapSkins(skin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)
					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return
					xbmc.sleep(500)
			title = '[COLOR %s][B]Installing Theme:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme)
			DP.update(0, title, '', '[COLOR %s]Please Wait...[/COLOR]' %COLOR2)
			percent, errors, error = extract.all(lib,HOME,DP, title=title)
			wiz.setS('buildtheme', theme)
			wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
			DP.close()
			if url not in ["fresh", "normal"]: 
				wiz.forceUpdate()
				if KODIV >= 17: wiz.kodi17Fix()
				if test2 == True:
					wiz.lookandFeelData('save')
					wiz.defaultSkin()
					gotoskin = wiz.getS('defaultskin')
					skinSwitch.swapSkins(gotoskin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)

					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					wiz.lookandFeelData('restore')
				elif test == True:
					skinSwitch.swapSkins(gotoskin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)

					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return
					wiz.lookandFeelData('restore')
				else:
					wiz.ebi("ReloadSkin()")
					xbmc.sleep(1000)
					wiz.ebi("Container.Refresh") 
		else:
			wiz.LogNotify("[COLOR %s]Theme Install[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)

def thirdPartyInstall(name, url):
	if not wiz.workingURL(url):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Invalid URL for Build[/COLOR]' % COLOR2); return
	type = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to perform a [COLOR %s]Fresh Install[/COLOR] or [COLOR %s]Standard Install[/COLOR] for the chosen build:[/COLOR]" % (COLOR2, COLOR1, COLOR1), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name), yeslabel="[B][COLOR %s]Fresh Install[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Standard Install[/COLOR][/B]" % COLOR1)
	if type == 1:
		freshStart('third', True)
	wiz.clearS('build')
	zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
	lib=os.path.join(PACKAGES, '%s.zip' % zipname)
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	xbmc.sleep(500)
	title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title, '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,HOME,DP, title=title)
	if int(float(percent)) > 0:
		wiz.fixmetas()
		wiz.lookandFeelData('save')
		wiz.defaultSkin()
		#wiz.addonUpdates('set')
		wiz.setS('installed', 'true')
		wiz.setS('extract', str(percent))
		wiz.setS('errors', str(errors))
		wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
		try: os.remove(lib)
		except: pass
		if int(float(errors)) > 0:
			yes=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the Errors?[/COLOR]', nolabel='[B][COLOR %s]No Thanks[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]View Errors[/COLOR][/B]' % COLOR2)
			if yes:
				if isinstance(errors, unicode):
					error = error.encode('utf-8')
				wiz.TextBox("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), error)
	DP.close()
	if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to [COLOR %s]Force Close[/COLOR] Kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
	if todo == 1: wiz.reloadFix()
	else: wiz.killxbmc(True)

def testTheme(path):
	zfile = zipfile.ZipFile(path)
	for item in zfile.infolist():
		if '/settings.xml' in item.filename:
			return True
	return False

def testGui(path):
	zfile = zipfile.ZipFile(path)
	for item in zfile.infolist():
		if '/guisettings.xml' in item.filename:
			return True
	return False

def apkInstaller(apk, url):
	wiz.log(apk)
	wiz.log(url)
	if wiz.platform() == 'android':
		yes = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to download and install:" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, apk), yeslabel="[B][COLOR %s]Download[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Cancel[/COLOR][/B]" % COLOR1)
		if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
		display = apk
		if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
		if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]APK Installer: Invalid APK URL![/COLOR]' % COLOR2); return
		DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display), '', '[COLOR %s]Please Wait...[/COLOR]' % COLOR2)
		lib=os.path.join(PACKAGES, "%s.apk" % apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
		try: os.remove(lib)
		except: pass
		downloader.download(url, lib, DP)
		xbmc.sleep(100)
		DP.close()
		notify.apkInstaller(apk)
		wiz.ebi('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
	else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Non-Android Device![/COLOR]' % COLOR2)

###########################
###### Misc Functions######
###########################

def createMenu(type, add, name):
	if   type == 'saveaddon':
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'save'    :
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Register %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Import %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'install'  :
		menu_items=[]
		name2 = urllib.quote_plus(name)
		menu_items.append((THEME2 % name,                                'RunAddon(%s, ?mode=viewbuild&name=%s)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Fresh Install',                     'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Standard Install',                    'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Apply GuiFix',                      'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Build Information',                 'RunPlugin(plugin://%s/?mode=buildinfo&name=%s)'  % (ADDON_ID, name2)))
	menu_items.append((THEME2 % '%s Settings' % ADDONTITLE,              'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
	return menu_items

def toggleCache(state):
	cachelist = ['includevideo', 'includeall', 'includecerebroshow', 'includecovenant', 'includedeathstreams', 'includeelysium', 'includeexodus', 'includeincursion', 'includeneptune', 'includeoculus', 'includeplacenta', 'includeposeidon', 'includeprojectm', 'includespecto', 'includestreamhub', 'includeukturk', 'includexxxodus']
	titlelist = ['Include Video Addons', 'Include All Addons', 'Include Cerebro Showbox', 'Include Covenant', 'Include Death Streams', 'Include Elysium', 'Include Exodus', 'Include Incursion', 'Include Neptune', 'Include Oculus', 'Include Placenta', 'Include Poseidon', 'Include Project M', 'Include Specto', 'Include StreamHub', 'Include UK Turk Playlists', 'Include XXX-O-DUS']
	if state in ['true', 'false']:
		for item in cachelist:
			wiz.setS(item, state)
	else:
		if not state in ['includevideo', 'includeall'] and wiz.getS('includeall') == 'true':
			try:
				item = titlelist[cachelist.index(state)]
				DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]You will need to turn off [COLOR %s]Include All Video Addons[/COLOR] to disable [COLOR %s]%s[/COLOR]![/COLOR]" % (COLOR2, COLOR1, COLOR1, item))
			except:
				wiz.LogNotify("[COLOR %s]Toggle Cache[/COLOR]" % COLOR1, "[COLOR %s]Invalid ID: %s[/COLOR]" % (COLOR2, state))
			sys.exit()
		else:
			new = 'true' if wiz.getS(state) == 'false' else 'false'
			wiz.setS(state, new)

def playVideo(url):
	if 'watch?v=' in url:
		a, b = url.split('?')
		find = b.split('&')
		for item in find:
			if item.startswith('v='):
				url = item[2:]
				break
			else: continue
	elif 'embed' in url or 'youtu.be' in url:
		a = url.split('/')
		if len(a[-1]) > 5:
			url = a[-1]
		elif len(a[-2]) > 5:
			url = a[-2]
	wiz.log("YouTube URL: %s" % url)
	yt.PlayVideo(url)

def viewLogFile():
	mainlog = wiz.Grab_Log(True)
	oldlog  = wiz.Grab_Log(True, True)
	which = 0; logtype = mainlog
	if not oldlog == False and not mainlog == False:
		which = DIALOG.select("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), ["View %s" % mainlog.replace(LOG, ""), "View %s" % oldlog.replace(LOG, "")])
		if which == -1: wiz.LogNotify('[COLOR %s]View Log[/COLOR]' % COLOR1, '[COLOR %s]View Log Cancelled![/COLOR]' % COLOR2); return
	elif mainlog == False and oldlog == False:
		wiz.LogNotify('[COLOR %s]View Log[/COLOR]' % COLOR1, '[COLOR %s]Log File NOT found![/COLOR]' % COLOR2)
		return
	elif not mainlog == False: which = 0
	elif not oldlog == False: which = 1
	
	logtype = mainlog if which == 0 else oldlog
	msg     = wiz.Grab_Log(False) if which == 0 else wiz.Grab_Log(False, True)
	
	wiz.TextBox("[COLOR %s]%s[/COLOR] - [COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE, COLOR2, logtype), msg)

def errorChecking(log=None, count=None, all=None):
	if log == None:
		mainlog = wiz.Grab_Log(True)
		oldlog  = wiz.Grab_Log(True, True)
		if not oldlog == False and not mainlog == False:
			which = DIALOG.select("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), ["[COLOR %s]View %s: %s error(s)[/COLOR]" % (COLOR2, mainlog.replace(LOG, ""), errorChecking(mainlog, True, True)), "[COLOR %s]View %s: %s error(s)[/COLOR]" % (COLOR1, oldlog.replace(LOG, ""), errorChecking(oldlog, True, True))])
			if which == -1: wiz.LogNotify('[COLOR %s]View Errors in Log[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2); return
		elif mainlog == False and oldlog == False:
			wiz.LogNotify('[COLOR %s]View Errors in Log[/COLOR]' % COLOR1, '[COLOR %s]Log File NOT found![/COLOR]' % COLOR2)
			return
		elif not mainlog == False: which = 0
		elif not oldlog == False: which = 1
		log = mainlog if which == 0 else oldlog
	if log == False:
		if count == None:
			wiz.LogNotify("[COLOR %s]View Errors in Log[/COLOR]" % COLOR1, "[COLOR %s]Log File NOT found![/COLOR]" % COLOR2)
			return False
		else: 
			return 0
	else:
		if os.path.exists(log):
			f = open(log,mode='r'); a = f.read().replace('\n', '').replace('\r', ''); f.close()
			match = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(a)
			if not count == None:
				if all == None: 
					x = 0
					for item in match:
						if ADDON_ID in item: x += 1
					return x
				else: return len(match)
			if len(match) > 0:
				x = 0; msg = ""
				for item in match:
					if all == None and not ADDON_ID in item: continue
					else: 
						x += 1
						msg += "[COLOR %s]Error Number %s[/COLOR]\n[COLOR %s](PythonToCppException) : -->Python callback/script returned the following error<--%s-->End of Python script error report<--\n\n[/COLOR]" % (COLOR1, x, COLOR2, item.replace('                                          ', '\n').replace('\\\\','\\').replace(HOME, ''))
				if x > 0:
					wiz.TextBox("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), msg)
				else: wiz.LogNotify("[COLOR %s]View Errors in Log[/COLOR]" % COLOR1, "[COLOR %s]No Errors Found in Selected Log![/COLOR]" % COLOR2)
			else: wiz.LogNotify("[COLOR %s]View Errors in Log[/COLOR]" % COLOR1, "[COLOR %s]No Errors Found in Selected Log![/COLOR]" % COLOR2)
		else: wiz.LogNotify("[COLOR %s]View Errors in Log[/COLOR]" % COLOR1, "Log File NOT found!")

ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

def LogViewer(default=None):
	class LogViewer(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.default = kwargs['default']

		def onInit(self):
			self.title      = 101
			self.msg        = 102
			self.scrollbar  = 103
			self.upload     = 201
			self.kodi       = 202
			self.kodiold    = 203
			self.wizard     = 204 
			self.okbutton   = 205 
			f = open(self.default, 'r')
			self.logmsg = f.read()
			f.close()
			self.titlemsg = "%s: %s" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR2, self.default.replace(LOG, '').replace(ADDONDATA, '')))
			self.showdialog()

		def showdialog(self):
			self.getControl(self.title).setLabel(self.titlemsg)
			self.getControl(self.msg).setText(wiz.highlightText(self.logmsg))
			self.setFocusId(self.scrollbar)
			
		def onClick(self, controlId):
			if   controlId == self.okbutton: self.close()
			elif controlId == self.upload: self.close(); uploadLog.Main()
			elif controlId == self.kodi:
				newmsg = wiz.Grab_Log(False)
				filename = wiz.Grab_Log(True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE))
					self.getControl(self.msg).setText("Log File Does Not Exist!")
				else:
					self.titlemsg = "%s: %s" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR2, filename.replace(LOG, '')))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.kodiold:  
				newmsg = wiz.Grab_Log(False, True)
				filename = wiz.Grab_Log(True, True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE))
					self.getControl(self.msg).setText("Log File Does Not Exist!")
				else:
					self.titlemsg = "%s: %s" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR2, filename.replace(LOG, '')))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.wizard:
				newmsg = wiz.Grab_Log(False, False, True)
				filename = wiz.Grab_Log(True, False, True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE))
					self.getControl(self.msg).setText("Log File Does Not Exist!")
				else:
					self.titlemsg = "%s: %s" % ("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR2, filename.replace(ADDONDATA, '')))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
		
		def onAction(self, action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()
	if default == None: default = wiz.Grab_Log(True)
	lv = LogViewer( "LogViewer.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', default=default)
	lv.doModal()
	del lv

def removeAddon(addon, name, over=False):
	if not over == False:
		yes = 1
	else: 
		yes = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Are you sure you want to delete the addon:" % COLOR2, "Name: [COLOR %s]%s[/COLOR]" % (COLOR1, name), "ID: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, addon), yeslabel="[B][COLOR %s]Remove Addon[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1)
	if yes == 1:
		folder = os.path.join(ADDONS, addon)
		wiz.log("Removing Addon %s" % addon)
		wiz.cleanHouse(folder)
		xbmc.sleep(200)
		try: shutil.rmtree(folder)
		except Exception ,e: wiz.log("Error removing %s" % addon, xbmc.LOGNOTICE)
		removeAddonData(addon, name, over)
	if over == False:
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Removed[/COLOR]" % (COLOR2, name))

def removeAddonData(addon, name=None, over=False):
	if addon == 'all':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in your Userdata folder?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			wiz.cleanHouse(ADDOND)
		else:
			wiz.LogNotify("[COLOR %s]Remove ALL Addon Data[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	elif addon == 'uninstalled':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in your Userdata folder for [COLOR %s]UNINSTALLED[/COLOR] addons?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]", nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			total = 0
			for folder in glob.glob(os.path.join(ADDOND, '*')):
				foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify("[COLOR %s]Remove Uninstalled Data[/COLOR]" % COLOR1, "[COLOR %s]%s Folder(s) Removed[/COLOR]" % (COLOR2, total))
		else:
			wiz.LogNotify("[COLOR %s]Remove Uninstalled Data[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	elif addon == 'empty':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] EMPTY addon data folders in your Userdata folder?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			total = wiz.emptyfolder(ADDOND)
			wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
		else:
			wiz.LogNotify("[COLOR %s]Remove Empty Folders[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("[COLOR %s]Protected Plugin[/COLOR]" % COLOR1, "[COLOR %s]NOT allowed to remove this![/COLOR]" % COLOR2)
			sys.exit()
		elif os.path.exists(addon_data):  
			if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove the addon data for:[/COLOR]" % COLOR2, "[COLOR %s]%s[COLOR %s]?[/COLOR]" % (COLOR1, addon, COLOR2), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error deleting: %s" % addon_data)
			else: 
				wiz.LogNotify("[COLOR %s]Remove Addon Data[/COLOR]" % COLOR1, "[COLOR %s]NOT Removed![/COLOR]" % COLOR2)
				wiz.log('Addon data for %s was NOT removed' % addon)
				sys.exit()
	wiz.refresh()

def restoreit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Restore Local Build: Cancelled![/COLOR]" % COLOR2); return
	if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
		wiz.skinToDefault()
	wiz.restoreLocal(type)

def restoreextit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Restore External Build: Cancelled![/COLOR]" % COLOR2); return
	wiz.restoreExternal(type)

def buildInfo(name):
	if wiz.workingURL(BUILDFILE) == True:
		if wiz.checkBuild(name, 'url'):
			name, version, url, gui, kodi, theme, icon, fanart, preview, adult, description = wiz.checkBuild(name, 'all')
			adult = 'Yes' if adult.lower() == 'yes' else 'No'
			msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
			msg += "[COLOR %s]Build Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
			if not theme == "http://":
				themecount = wiz.themeCount(name, False)
				msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
			msg += "[COLOR %s]Software Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
			msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
			msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)
			wiz.TextBox("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, ADDONTITLE), msg)
		else: wiz.log("Invalid Build Name!")
	else: wiz.log("Build text file not working: %s" % WORKINGURL)

def buildVideo(name):
	if wiz.workingURL(BUILDFILE) == True:
		videofile = wiz.checkBuild(name, 'preview')
		if videofile and not videofile == 'http://': playVideo(videofile)
		else: wiz.log("[%s]Unable to find URL for video preview" % name)
	else: wiz.log("Build text file not working: %s" % WORKINGURL)

def dependsList(plugin):
	addonxml = os.path.join(ADDONS, plugin, 'addon.xml')
	if os.path.exists(addonxml):
		source = open(addonxml,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		items  = []
		for depends in match:
			if not 'xbmc.python' in depends:
				items.append(depends)
		return items
	return []

def manageSaveData(do):
	if do == 'import':
		TEMP = os.path.join(ADDONDATA, 'temp')
		if not os.path.exists(TEMP): os.makedirs(TEMP)
		source = DIALOG.browse(1, '[COLOR %s]Select the [COLOR %s]SaveData.zip[/COLOR] file you wish to import:[/COLOR]' % (COLOR1, COLOR2), 'files', '.zip', False, False, HOME)
		if not source.endswith('SaveData.zip'):
			wiz.LogNotify("[COLOR %s]Import ALL Account Info[/COLOR]" % COLOR1, "[COLOR %s]SaveData.zip File NOT Selected![/COLOR]" % (COLOR2))
			return
		tempfile = os.path.join(MYBUILDS, 'SaveData.zip')
		goto = xbmcvfs.copy(source, tempfile)
		wiz.log("%s" % str(goto))
		extract.all(xbmc.translatePath(tempfile), TEMP)
		trakt  = os.path.join(TEMP, 'trakt')
		login  = os.path.join(TEMP, 'login')
		debrid = os.path.join(TEMP, 'debrid')
		x = 0
		if os.path.exists(trakt):
			x += 1
			files = os.listdir(trakt)
			if not os.path.exists(traktit.TRAKTFOLD): os.makedirs(traktit.TRAKTFOLD)
			for item in files:
				old  = os.path.join(traktit.TRAKTFOLD, item)
				temp = os.path.join(trakt, item)
				if os.path.exists(old):
					if not DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR %s]Yes, Replace[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Skip[/COLOR][/B]" % COLOR1): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			traktit.importlist('all')
			traktit.traktIt('restore', 'all')
		if os.path.exists(login):
			x += 1
			files = os.listdir(login)
			if not os.path.exists(loginit.LOGINFOLD): os.makedirs(loginit.LOGINFOLD)
			for item in files:
				old  = os.path.join(loginit.LOGINFOLD, item)
				temp = os.path.join(login, item)
				if os.path.exists(old):
					if not DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR %s]Yes, Replace[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Skip[/COLOR][/B]" % COLOR1): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			loginit.importlist('all')
			loginit.loginIt('restore', 'all')
		if os.path.exists(debrid):
			x += 1
			files = os.listdir(debrid)
			if not os.path.exists(debridit.REALFOLD): os.makedirs(debridit.REALFOLD)
			for item in files:
				old  = os.path.join(debridit.REALFOLD, item)
				temp = os.path.join(debrid, item)
				if os.path.exists(old):
					if not DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR %s]Yes, Replace[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]No, Skip[/COLOR][/B]" % COLOR1): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			debridit.importlist('all')
			debridit.debridIt('restore', 'all')
		wiz.cleanHouse(TEMP)
		wiz.removeFolder(TEMP)
		os.remove(tempfile)
		if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import ALL Account Info: Failed![/COLOR]" % COLOR2)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import ALL Account Info: Complete[/COLOR]" % COLOR2)
	elif do == 'export':
		mybuilds = xbmc.translatePath(MYBUILDS)
		dir = [traktit.TRAKTFOLD, debridit.REALFOLD, loginit.LOGINFOLD]
		traktit.traktIt('update', 'all')
		loginit.loginIt('update', 'all')
		debridit.debridIt('update', 'all')
		source = DIALOG.browse(3, '[COLOR %s]Select where you wish to export your [COLOR %s]SaveData.zip[/COLOR] file to:[/COLOR]' % (COLOR1, COLOR2), 'files', '', False, True, HOME)
		if source == "":
			wiz.LogNotify("[COLOR %s]Export ALL Account Info[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		source = xbmc.translatePath(source)
		tempzip = os.path.join(mybuilds, 'SaveData.zip')
		zipf = zipfile.ZipFile(tempzip, mode='w')
		for fold in dir:
			if os.path.exists(fold):
				files = os.listdir(fold)
				for file in files:
					zipf.write(os.path.join(fold, file), os.path.join(fold, file).replace(ADDONDATA, ''), zipfile.ZIP_DEFLATED)
		zipf.close()
		if source == mybuilds:
			DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Trakt/RD/Login Info has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))
		else:
			try:
				xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
				DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Trakt/RD/Login Info has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'SaveData.zip')))
			except:
				DIALOG.ok("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Trakt/RD/Login Info has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))

#######################################
###### Fresh Start/Fresh Install ######
#######################################
def freshStart(install=None, over=False):
	if KEEPTRAKT == 'true':
		traktit.autoUpdate('all')
		wiz.setS('traktlastsave', str(THREEDAYS))
	if KEEPREAL == 'true':
		debridit.autoUpdate('all')
		wiz.setS('debridlastsave', str(THREEDAYS))
	if KEEPLOGIN == 'true':
		loginit.autoUpdate('all')
		wiz.setS('loginlastsave', str(THREEDAYS))
	if not install == 'restore' and not install == None:
		myFresh = "Fresh Install"
	else:
		myFresh = "Fresh Start"
	if over == True: yes_pressed = 1
	elif install == 'restore': yes_pressed=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Do you wish to restore your Kodi configuration to default settings before installing the build backup?[/COLOR]" % COLOR2, nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Continue[/COLOR][/B]' % COLOR2)
	elif install: yes_pressed=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Do you wish to restore your Kodi configuration to default settings before installing the [COLOR %s]%s[/COLOR] build?" % (COLOR2, COLOR1, install), nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Continue[/COLOR][/B]' % COLOR2)
	else: yes_pressed=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Do you wish to restore your Kodi configuration to default settings?[/COLOR]" % COLOR2, nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Continue[/COLOR][/B]' % COLOR2)
	if yes_pressed:
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
			#yes=DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]The skin needs to be set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, skin[5:]), "Before doing a fresh install to clear all Texture files,", "Would you like us to do that for you?[/COLOR]", yeslabel="[B][COLOR %s]Switch Skins[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]I'll Do It[/COLOR][/B]" % COLOR1);
			#if yes:
			skinSwitch.swapSkins(skin)
			x = 0
			xbmc.sleep(1000)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
				x += 1
				xbmc.sleep(200)
				wiz.ebi('SendAction(Select)')
			if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				wiz.ebi('SendClick(11)')
			else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), '[COLOR %s]Skin Swap Timed Out![/COLOR]' % COLOR2); return False
			xbmc.sleep(1000)
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), '[COLOR %s]Skin Swap Failed![/COLOR]' % COLOR2)
			return
		wiz.addonUpdates('set')
		xbmcPath=os.path.abspath(HOME)
		DP.create("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), "[COLOR %s]Calculating files and folders" % COLOR2, '', '[COLOR %s]Please Wait...[/COLOR]' %COLOR2)
		total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
		DP.update(0, "[COLOR %s]Gathering Excludes list" % COLOR2)
		EXCLUDES.append('My_Builds')
		EXCLUDES.append('archive_cache')
		if KEEPREPOS == 'true':
			repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
			for item in repos:
				repofolder = os.path.split(item[:-1])[1]
				if not repofolder == EXCLUDES:
					EXCLUDES.append(repofolder)
		if KEEPSUPER == 'true':
			EXCLUDES.append('plugin.program.super.favourites')
		if KEEPWHITELIST == 'true':
			pvr = ''
			whitelist = wiz.whiteList('read')
			if len(whitelist) > 0:
				for item in whitelist:
					try: name, id, fold = item
					except: pass
					if fold.startswith('pvr'): pvr = id 
					depends = dependsList(fold)
					for plug in depends:
						if not plug in EXCLUDES:
							EXCLUDES.append(plug)
						depends2 = dependsList(plug)
						for plug2 in depends2:
							if not plug2 in EXCLUDES:
								EXCLUDES.append(plug2)
					if not fold in EXCLUDES:
						EXCLUDES.append(fold)
				if not pvr == '': wiz.setS('pvrclient', fold)
		if wiz.getS('pvrclient') == '':
			for item in EXCLUDES:
				if item.startswith('pvr'):
					wiz.setS('pvrclient', item)
		DP.update(0, "[COLOR %s]Clearing out files and folders:" % COLOR2)
		latestAddonDB = wiz.latestDB('Addons')
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				del_file += 1
				fold = root.replace('/','\\').split('\\')
				x = len(fold)-1
				if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep My Sources: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep My Favourites: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep My Profiles: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name in LOGFILES: wiz.log("Keep Log File: %s" % name, xbmc.LOGNOTICE)
				elif name.endswith('.db'):
					try:
						if name == latestAddonDB and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV), xbmc.LOGNOTICE)
						else: os.remove(os.path.join(root,name))
					except Exception, e: 
						if not name.startswith('Textures13'):
							wiz.log('Failed to delete, Purging DB', xbmc.LOGNOTICE)
							wiz.log("-> %s" % (str(e)), xbmc.LOGNOTICE)
							wiz.purgeDb(os.path.join(root,name))
				else:
					DP.update(int(wiz.percentage(del_file, total_files)), '', '[COLOR %s]File: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '')
					try: os.remove(os.path.join(root,name))
					except Exception, e: 
						wiz.log("Error removing %s" % os.path.join(root, name), xbmc.LOGNOTICE)
						wiz.log("-> / %s" % (str(e)), xbmc.LOGNOTICE)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
				return False
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				DP.update(100, '', '[COLOR %s]Cleaning Up Empty Folder(s): [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, name), '')
				if name not in ["Database","userdata","temp","addons","addon_data"]:
					shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
				return False
		DP.close()
		wiz.clearS('build')
		if over == True:
			return True
		elif install == 'restore': 
			return True
		elif install: 
			buildWizard(install, 'normal', over=True)
		else:
			if INSTALLMETHOD == 1: todo = 1
			elif INSTALLMETHOD == 2: todo = 0
			else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to [COLOR %s]Force Close[/COLOR] Kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
			if todo == 1: wiz.reloadFix('fresh')
			else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
	else: 
		if not install == 'restore':
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, myFresh), '[COLOR %s]Cancelled![/COLOR]' % COLOR2)

#########################################NET TOOLS#############################################
def net_tools(view=None):
	if HIDESPACERS == 'No': addFile(wiz.sep('Net Tools'), '', themeit=THEME3)
	addFile ('Speed Tester' ,'speed', icon=ICONSPEED, themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	setView('files', 'viewType')
def speedMenu():
	xbmc.executebuiltin('Runscript("special://home/addons/plugin.program.dogewizard/speedtest.py")')
######################################################################################################################
######################################################################################################################		
			
#############################
###DELETE CACHE##############
####THANKS TO GUYS @ NaN ####
def clearCache():
	choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to Clear Cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Clear Cache[/COLOR][/B]' % COLOR2)
	if choice == 1:
		wiz.clearCache()
	else: 
		wiz.log('Clear Cache Cancelled!')
		wiz.LogNotify("[COLOR %s]Clear Cache[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		sys.exit()

def totalClean():
	choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to Clear Cache, Packages and Thumbnails?[/COLOR]' % COLOR2, nolabel='[B][COLOR %s]Cancel Process[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Clean All[/COLOR][/B]' % COLOR2)
	if choice == 1:
		wiz.clearCache()
		clearThumb('total')
		wiz.clearPackages('total')
	else: 
		wiz.log('Total Cleanup Cancelled!')
		wiz.LogNotify("[COLOR %s]Total Cleanup[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		sys.exit()

def clearThumb(type=None):
	latest = wiz.latestDB('Textures')
	if not type == None: choice = 1
	else: choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to delete the %s file and Thumbnails folder?" % (COLOR2, latest), "[COLOR %s]Don't worry, they will repopulate on the next startup.[/COLOR]" % COLOR1, nolabel="[B][COLOR %s]Don't Delete[/COLOR][/B]" % COLOR1, yeslabel='[B][COLOR %s]Delete Thumbs[/COLOR][/B]' % COLOR2)
	if choice == 1:
		try: wiz.removeFile(os.join(DATABASE, latest))
		except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
		wiz.removeFolder(THUMBS)
		#if not type == 'total': wiz.killxbmc()   ### This is commented out so that a Force Close isn't performed after the Clear Thumbnails process completes! ###
		wiz.redoThumbs()
	else: 
		wiz.LogNotify("[COLOR %s]Clear Thumbnails[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		wiz.log('Clear Thumbnails Cancelled!')
		sys.exit()

def purgeDb():
	DB = []; display = []
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIV >= 16:
		choice = DIALOG.multiselect("[COLOR %s]Select DB File to Purge:[/COLOR]" % COLOR1, display)
		if choice == None: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = DIALOG.select("[COLOR %s]Select DB File to Purge:[/COLOR]" % COLOR1, display)
		if choice == -1: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		elif choice == 0: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
		else: wiz.purgeDb(DB[purge])

##########################
### DEVELOPER Options #######
##########################
def testnotify():
	url = wiz.workingURL(NOTIFICATION)
	if url == True:
		try:
			id, msg = wiz.splitNotify(NOTIFICATION)
			if id == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Notification: Not Formatted Correctly[/COLOR]" % COLOR2); return
			notify.notification(msg, True)
		except Exception, e:
			wiz.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
	else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Invalid URL for Notification![/COLOR]" % COLOR2)

def testupdate():
	if BUILDNAME == "":
		notify.updateWindow()
	else:
		notify.updateWindow(BUILDNAME, BUILDVERSION, BUILDLATEST, wiz.checkBuild(BUILDNAME, 'icon'), wiz.checkBuild(BUILDNAME, 'fanart'))

def testfirst():
	notify.firstRun()

def testfirstRun():
	notify.firstRunSettings()

###########################
## Making the Directory####
###########################

def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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

params=get_params()
url=None
name=None
mode=None

try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass

wiz.log('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ URL : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
	if wiz.getS('auto-view')=='true':
		views = wiz.getS(viewType)
		if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
		if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
		wiz.ebi("Container.SetViewMode(%s)" %  views)

if   mode==None             : index()

elif mode=='wizardupdate'   : wiz.wizardUpdate()
elif mode=='builds'         : buildMenu()
elif mode=='viewbuild'      : viewBuild(name)
elif mode=='buildinfo'      : buildInfo(name)
elif mode=='buildpreview'   : buildVideo(name)
elif mode=='install'        : buildWizard(name, url)
elif mode=='theme'          : buildWizard(name, mode, url)
elif mode=='viewthirdparty' : viewThirdList(name)
elif mode=='installthird'   : thirdPartyInstall(name, url)
elif mode=='editthird'      : editThirdParty(name); wiz.refresh()

elif mode=='maint'          : maintMenu(name)
elif mode=='kodi17fix'      : wiz.kodi17Fix()
elif mode=='advancedsetting': advancedWindow(name)
elif mode=='autoadvanced'   : showAutoAdvanced(); wiz.refresh()
elif mode=='removeadvanced' : removeAdvanced(); wiz.refresh()
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='backupaddon'    : wiz.backUpOptions('addondata')
elif mode=='oldThumbs'      : wiz.oldThumbs()
elif mode=='clearbackup'    : wiz.cleanupBackup()
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='currentsettings': viewAdvanced()
elif mode=='fullclean'      : totalClean(); wiz.refresh()
elif mode=='clearcache'     : clearCache(); wiz.refresh()
elif mode=='clearpackages'  : wiz.clearPackages(); wiz.refresh()
elif mode=='clearcrash'     : wiz.clearCrash(); wiz.refresh()
elif mode=='clearthumb'     : clearThumb(); wiz.refresh()
elif mode=='checksources'   : wiz.checkSources(); wiz.refresh()
elif mode=='ytfix'          : wiz.ytfix(); wiz.refresh()
elif mode=='checkrepos'     : wiz.checkRepos(); wiz.refresh()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceprofile'   : wiz.reloadProfile(wiz.getInfo('System.ProfileName'))
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='forceskin'      : wiz.ebi("ReloadSkin()"); wiz.refresh()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='enableaddons'   : enableAddons()
elif mode=='toggleaddon'    : wiz.toggleAddon(name, url); wiz.refresh()
elif mode=='togglecache'    : toggleCache(name); wiz.refresh()
elif mode=='toggleadult'    : wiz.toggleAdult(); wiz.refresh()
elif mode=='changefreq'      : changefreq(); wiz.refresh()
elif mode=='uploadlog'      : uploadLog.Main()
elif mode=='viewlog'        : LogViewer()
elif mode=='viewwizlog'     : LogViewer(WIZLOG)
elif mode=='viewerrorlog'   : errorChecking(all=True)
elif mode=='clearwizlog'    : f = open(WIZLOG, 'w'); f.close(); wiz.refresh(); wiz.LogNotify("[COLOR %s]Clear Wizard Log File[/COLOR]" % COLOR1,  "[COLOR %s]Log Cleared![/COLOR]" % COLOR2)
elif mode=='purgedb'        : purgeDb()
elif mode=='fixaddonupdate' : fixUpdate()
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Addon_Data Reset![/COLOR]" % COLOR2)
elif mode=='systeminfo'     : systemInfo()
elif mode=='restorezip'     : restoreit('Build')
elif mode=='restoregui'     : restoreit('GuiFix')
elif mode=='restoreaddon'   : restoreit('Addon_data')
elif mode=='restoreextzip'  : restoreextit('Build')
elif mode=='restoreextgui'  : restoreextit('GuiFix')
elif mode=='restoreextaddon': restoreextit('Addon_data')
elif mode=='speedtest'      : speedtest.speedtest ( self , list = False , mini = None , server = None , share = False , simple = False , src = None , timeout = 10 , units = ( 'bit' , 8 ) , version = False )
elif mode=='writeadvanced'  : writeAdvanced(name, url)

elif mode=='apk'            : apkMenu(name)
elif mode=='apkscrape'      : apkScraper(name)
elif mode=='apkinstall'     : apkInstaller(name, url)

elif mode=='youtube'        : youtubeMenu(name)
elif mode=='viewVideo'      : playVideo(url)

elif mode=='addons'         : addonMenu(name)
elif mode=='addoninstall'   : addonInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); wiz.refresh()
elif mode=='managedata'     : manageSaveData(name)
elif mode=='whitelist'      : wiz.whiteList(name)

elif mode=='trakt'          : traktMenu()
elif mode=='savetrakt'      : traktit.traktIt('update',      name)
elif mode=='restoretrakt'   : traktit.traktIt('restore',     name)
elif mode=='addontrakt'     : traktit.traktIt('clearaddon',  name)
elif mode=='cleartrakt'     : traktit.clearSaved(name)
elif mode=='authtrakt'      : traktit.activateTrakt(name); wiz.refresh()
elif mode=='updatetrakt'    : traktit.autoUpdate('all')
elif mode=='importtrakt'    : traktit.importlist(name); wiz.refresh()

elif mode=='realdebrid'     : realMenu()
elif mode=='savedebrid'     : debridit.debridIt('update',      name)
elif mode=='restoredebrid'  : debridit.debridIt('restore',     name)
elif mode=='addondebrid'    : debridit.debridIt('clearaddon',  name)
elif mode=='cleardebrid'    : debridit.clearSaved(name)
elif mode=='authdebrid'     : debridit.activateDebrid(name); wiz.refresh()
elif mode=='updatedebrid'   : debridit.autoUpdate('all')
elif mode=='importdebrid'   : debridit.importlist(name); wiz.refresh()

elif mode=='login'          : loginMenu()
elif mode=='savelogin'      : loginit.loginIt('update',      name)
elif mode=='restorelogin'   : loginit.loginIt('restore',     name)
elif mode=='addonlogin'     : loginit.loginIt('clearaddon',  name)
elif mode=='clearlogin'     : loginit.clearSaved(name)
elif mode=='authlogin'      : loginit.activateLogin(name); wiz.refresh()
elif mode=='updatelogin'    : loginit.autoUpdate('all')
elif mode=='importlogin'    : loginit.importlist(name); wiz.refresh()

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(name); wiz.refresh()
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); wiz.refresh()

elif mode=='developer'      : developer()
elif mode=='converttext'    : wiz.convertText()
elif mode=='createqr'       : wiz.createQR()
elif mode=='testnotify'     : testnotify()
elif mode=='testupdate'     : testupdate()
elif mode=='testfirst'      : testfirst()
elif mode=='testfirstrun'   : testfirstRun()
elif mode=='testapk'        : notify.apkInstaller('SPMC')

elif mode=='net'            : net_tools()
elif mode=='speed'          : speedMenu()

xbmcplugin.endOfDirectory(int(sys.argv[1]))