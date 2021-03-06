import re
import time
import BasePlayer
import ConVar.Server as sv
import UnityEngine.Random as random
from System import Action, Int32, String

DEV = False
LATEST_CFG = 5.3
LINE = '-' * 50
PROFILE = '76561198235146288'

class notifier:

    def __init__(self):

        self.Title = 'Notifier'
        self.Version = V(2, 11, 1)
        self.Author = 'SkinN'
        self.Description = 'Broadcasts chat messages as notifications and advertising.'
        self.ResourceId = 797

    # -------------------------------------------------------------------------
    # - CONFIGURATION / DATABASE SYSTEM
    def LoadDefaultConfig(self):
        ''' Hook called when there is no configuration file '''

        self.Config = {
            'CONFIG_VERSION': LATEST_CFG,
            'SETTINGS': {
                'PREFIX': '<white>[<end> <cyan>NOTIFIER<end> <white>]<end>',
                'BROADCAST TO CONSOLE': True,
                'RULES LANGUAGE': 'AUTO',
                'HIDE ADMINS': False,
                'PLAYERS LIST ON CHAT': True,
                'PLAYERS LIST ON CONSOLE': True,
                'ADVERTS INTERVAL': 6,
                'ENABLE PLAYERS DEFAULT COLORS': True,
                'ENABLE PLUGIN ICON': True,
                'ENABLE JOIN MESSAGE': True,
                'ENABLE LEAVE MESSAGE': True,
                'ENABLE WELCOME MESSAGE': True,
                'ENABLE ADVERTS': True,
                'ENABLE PLAYERS LIST': True,
                'ENABLE PLAYERS ONLINE': True,
                'ENABLE ADMINS LIST': False,
                'ENABLE PLUGINS LIST': False,
                'ENABLE RULES': True,
                'ENABLE MAP LINK': True,
                'ENABLE ADVERTS COMMAND': True
            },
            'MESSAGES': {
                'JOIN MESSAGE': '{username} joined the server, from <orange>{country}<end>.',
                'LEAVE MESSAGE': '{username} left the server. (Reason: {reason})',
                'CHECK CONSOLE': 'Check the console (press F1) for more info.',
                'PLAYERS ONLINE': 'There are <lime>{active}<end>/<lime>{maxplayers}<end> players online.',
                'ADMINS ONLINE': 'There are <cyan>{admins} Admins<end> online.',
                'PLAYERS STATS': 'Sleepers: <lime>{sleepers}<end> Alltime Players: <lime>{alltime}<end>',
                'MAP LINK': 'See where you are on the server map at: <lime>http://{ip}:{port}<end>',
                'NO RULES': 'Error, no rules found, contact the <cyan>Admins<end>.',
                'NO LANG': 'Error, <lime>{args}<end> language not supported or does not exist.',
                'NO ADMINS': 'There are no <cyan>Admins<end> online.',
                'ADVERTS INTERVAL CHANGED': 'Adverts interval changed to <lime>{minutes}<end> minutes',
                'SYNTAX ERROR': 'Syntax Error: {syntax}',
                'ADMINS LIST TITLE': 'ADMINS ONLINE',
                'PLUGINS LIST TITLE': 'SERVER PLUGINS',
                'PLAYERS LIST TITLE': 'PLAYERS LIST',
                'PLAYERS ONLINE TITLE': 'PLAYERS ONLINE',
                'RULES TITLE': 'SERVER RULES',
                'PLAYERS LIST DESC': '<orange>/players<end> <grey>-<end> List of all players in the server.',
                'ADMINS LIST DESC': '<orange>/admins<end> <grey>-<end> List of online <cyan>Admins<end> in the server.',
                'PLUGINS LIST DESC': '<orange>/plugins<end> <grey>-<end> List of plugins installed in the server.',
                'RULES DESC': '<orange>/rules<end> <grey>-<end> List of server rules.',
                'MAP LINK DESC': '<orange>/map<end> <grey>-<end> Server map url.',
                'ADVERTS DESC': '<orange>/adverts<end> <grey>-<end> Allows <cyan>Admins<end> to change the adverts interval ( i.g: /adverts 5 )',
                'PLAYERS ONLINE DESC': '<orange>/online<end> <grey>-<end> Shows the number of players and <cyan>Admins<end> online, plus a few server stats.'
            },
            'WELCOME MESSAGE': (
                '<size=17>Welcome {username}</size>',
                '<orange><size=20>•</size><end> Type <orange>/help<end> for all available commands.',
                '<orange><size=20>•</size><end> Check our server <orange>/rules<end>.',
                '<orange><size=20>•</size><end> See where you are on the server map at: <lime>http://{server.ip}:{server.port}<end>'
            ),
            'ADVERTS': (
                'Want to know the available commands? Type <orange>/help<end>.',
                'Respect the server <orange>/rules<end>.',
                'This server is running <orange>Oxide 2<end>.',
                '<red>Cheat is strictly prohibited.<end>',
                'Type <orange>/map<end> for the server map link.',
                'You are playing on: <lime>{server.hostname}<end>',
                '<orange>Players Online: <lime>{players}<end> / <lime>{server.maxplayers}<end> Sleepers: <lime>{sleepers}<end><end>'
            ),
            'COLORS': {
                'PREFIX': '#00EEEE',
                'JOIN MESSAGE': 'silver',
                'LEAVE MESSAGE': 'silver',
                'WELCOME MESSAGE': 'silver',
                'ADVERTS': 'silver',
                'SYSTEM': 'white',
                'BOARDS TITLE': 'silver'
            },
            'COMMANDS': {
                'PLAYERS LIST': 'players',
                'RULES': ('rules', 'regras', 'regles'),
                'PLUGINS LIST': 'plugins',
                'ADMINS LIST': 'admins',
                'PLAYERS ONLINE': 'online',
                'MAP LINK': 'map',
                'ADVERTS COMMAND': 'adverts'
            },
            'RULES': {
                'EN': (
                    'Cheating is strictly prohibited.',
                    'Respect all players',
                    'Avoid spam in chat.',
                    'Play fair and don\'t abuse of bugs/exploits.'
                ),
                'PT': (
                    'Usar cheats e totalmente proibido.',
                    'Respeita todos os jogadores.',
                    'Evita spam no chat.',
                    'Nao abuses de bugs ou exploits.'
                ),
                'FR': (
                    'Tricher est strictement interdit.',
                    'Respectez tous les joueurs.',
                    'Évitez le spam dans le chat.',
                    'Jouer juste et ne pas abuser des bugs / exploits.'
                ),
                'ES': (
                    'Los trucos están terminantemente prohibidos.',
                    'Respeta a todos los jugadores.',
                    'Evita el Spam en el chat.',
                    'Juega limpio y no abuses de bugs/exploits.'
                ),
                'DE': (
                    'Cheaten ist verboten!',
                    'Respektiere alle Spieler',
                    'Spam im Chat zu vermeiden.',
                    'Spiel fair und missbrauche keine Bugs oder Exploits.'
                ),
                'TR': (
                    'Hile kesinlikle yasaktır.',
                    'Tüm oyuncular Saygı.',
                    'Sohbet Spam kaçının.',
                    'Adil oynayın ve böcek / açıkları kötüye yok.'
                ),
                'IT': (
                    'Cheating è severamente proibito.',
                    'Rispettare tutti i giocatori.',
                    'Evitare lo spam in chat.',
                    'Fair Play e non abusare di bug / exploit.'
                ),
                'DK': (
                    'Snyd er strengt forbudt.',
                    'Respekt alle spillere.',
                    'Undgå spam i chatten.',
                    'Play fair og ikke misbruger af bugs / exploits.'
                ),
                'RU': (
                    'Запрещено использовать читы.',
                    'Запрещено спамить и материться.',
                    'Уважайте других игроков.',
                    'Играйте честно и не используйте баги и лазейки.'
                ),
                'NL': (
                    'Vals spelen is ten strengste verboden.',
                    'Respecteer alle spelers',
                    'Vermijd spam in de chat.',
                    'Speel eerlijk en maak geen misbruik van bugs / exploits.'
                ),
                'UA': (
                    'Обман суворо заборонено.',
                    'Поважайте всіх гравців',
                    'Щоб уникнути спаму в чаті.',
                    'Грати чесно і не зловживати помилки / подвиги.'
                ),
                'RO': (
                    'Cheaturile sunt strict interzise!',
                    'Respectați toți jucătorii!',
                    'Evitați spamul în chat!',
                    'Jucați corect și nu abuzați de bug-uri/exploituri!'
                ),
                'HU': (
                    'Csalás szigorúan tilos.',
                    'Tiszteld minden játékostársad.',
                    'Kerüld a spammolást a chaten.',
                    'Játssz tisztességesen és nem élj vissza a hibákkal.'
                )
            }
        }

        self.con('* Loading default configuration file')

    # -------------------------------------------------------------------------
    def UpdateConfig(self):
        ''' Function to update the configuration file on plugin Init '''

        if (self.Config['CONFIG_VERSION'] <= LATEST_CFG - 0.2) or DEV:

            self.con('* Configuration version is too old, reseting to default')

            adverts = self.Config['ADVERTS']

            self.Config.clear()

            self.LoadDefaultConfig()

            if not DEV: self.Config['ADVERTS'] = adverts

        else:

            self.con('* Applying new changes to configuration file')

            self.Config['MESSAGES']['LEAVE MESSAGE'] = '{username} left the server. (Reason: {reason})'

            self.Config['CONFIG_VERSION'] = LATEST_CFG

        self.SaveConfig()

    # -------------------------------------------------------------------------
    # - MESSAGE SYSTEM
    def con(self, text, f=False):
        ''' Function to send a server con message '''

        if self.Config['SETTINGS']['BROADCAST TO CONSOLE'] or f:

            print('[%s v%s] :: %s' % (self.Title, str(self.Version), self.format(text, True)))

    # --------------------------------------------------------------------------
    def pcon(self, player, text, color='silver'):
        ''' Function to send a message to a player console '''

        player.SendConsoleCommand(self.format('echo <%s>%s<end>' % (color, text)))

    # -------------------------------------------------------------------------
    def say(self, text, color='silver', f=True, profile=False):
        ''' Function to send a message to all players '''

        if self.prefix and f:

            rust.BroadcastChat(self.format('%s <%s>%s<end>' % (self.prefix, color, text)), None, PROFILE if not profile else profile)

        else:

            rust.BroadcastChat(self.format('<%s>%s<end>' % (color, text)), None, PROFILE if not profile else profile)

        self.con(self.format(text, True))

    # -------------------------------------------------------------------------
    def tell(self, player, text, color='silver', f=True, profile=False):
        ''' Function to send a message to a player '''

        if self.prefix and f:

            rust.SendChatMessage(player, self.format('%s <%s>%s<end>' % (self.prefix, color, text)), None, PROFILE if not profile else profile)

        else:

            rust.SendChatMessage(player, self.format('<%s>%s<end>' % (color, text)), None, PROFILE if not profile else profile)

    # -------------------------------------------------------------------------
    def log(self, filename, text):
        ''' Logs text into a specific file '''

        if self.logs:

            try:

                filename = 'notifier_%s_%s.txt' % (filename, self.log_date())

                sv.Log('oxide/logs/%s' % filename, text)

            except:

                self.con('An error as occurred when writing a connection log to a file! ( Missing directory )')
                self.con('Logs are now off, please make sure you have the following path on your server files: .../%s/oxide/logs' % sv.identity)

    # -------------------------------------------------------------------------
    # - PLUGIN HOOKS
    def Init(self):
        ''' Hook called when the plugin initializes '''

        self.con(LINE)

        # Update Config File
        if self.Config['CONFIG_VERSION'] < LATEST_CFG or DEV:

            self.UpdateConfig()

        else: self.con('* Configuration file is up to date')

        # Global / Class Variables
        global MSG, PLUGIN, COLOR, CMDS, ADVERTS, RULES
        MSG, COLOR, PLUGIN, CMDS, ADVERTS, RULES = [self.Config[x] for x in \
        ('MESSAGES', 'COLORS', 'SETTINGS', 'COMMANDS', 'ADVERTS', 'RULES')]

        self.prefix = '<%s>%s<end>' % (COLOR['PREFIX'], PLUGIN['PREFIX']) if PLUGIN['PREFIX'] else False
        self.cache = {}
        self.connected = []
        self.lastadvert = 0
        self.adverts_loop = False
        self.logs = True

        # Countries Data
        self.countries = data.GetData('notifier_countries_db')
        self.countries.update(self.countries_dict())
        data.SaveData('notifier_countries_db')

        # Use Plugin Icon?
        if not PLUGIN['ENABLE PLUGIN ICON']:

            global PROFILE
            PROFILE = '0'

        # Initiate active players
        for player in self.activelist(): self.OnPlayerInit(player, False)

        # Start Adverts Loop
        if PLUGIN['ENABLE ADVERTS']:

            mins = PLUGIN['ADVERTS INTERVAL']
            secs = mins * 60 if mins else 60

            self.adverts_loop = timer.Repeat(secs, 0, Action(self.send_advert), self.Plugin)

            self.con('* Starting Adverts loop, set to %s minute/s' % mins)

        else: self.con('* Adverts are disabled')

        # Create Plugin Commands
        n = 0

        self.con('* Enabling commands:')

        for cmd in CMDS:

            if PLUGIN['ENABLE %s' % cmd]:

                n += 1

                if isinstance(CMDS[cmd], tuple):

                    for i in CMDS[cmd]:

                        command.AddChatCommand(i, self.Plugin, '%s_CMD' % cmd.replace(' ','_').lower())

                    self.con('  - %s (/%s)' % (cmd.title(), ', /'.join(CMDS[cmd])))

                else:

                    command.AddChatCommand(CMDS[cmd], self.Plugin, '%s_CMD' % cmd.replace(' ','_').lower())

                    self.con('  - %s (/%s)' % (cmd.title(), CMDS[cmd]))

        if not n: self.con('  - No commands are enabled')

        command.AddChatCommand('notifier', self.Plugin, 'plugin_CMD')

        self.con(LINE)

    # --------------------------------------------------------------------------
    def Unload(self):
        ''' Hook called on plugin unload '''

        # Destroy adverts loop
        if self.adverts_loop: self.adverts_loop.Destroy()

    # -------------------------------------------------------------------------
    # - PLAYER HOOKS
    def OnPlayerInit(self, player, send=True):

        if player and player.net:

            # Cache player and list him to connected
            self.cache_player(player.net.connection)

            uid = self.playerid(player)

            if uid not in self.connected: self.connected.append(uid)

            self.webrequest_filter(player, send)

    # -------------------------------------------------------------------------
    def OnPlayerDisconnected(self, player, reason):
        ''' Hook called when a player disconnects from the server '''

        uid = self.playerid(player)

        if uid in self.cache:

            ply = self.cache[uid]

            # Is Player connected?
            if uid in self.connected:

                self.connected.remove(uid)

                if PLUGIN['ENABLE LEAVE MESSAGE']:
                    
                    if not (PLUGIN['HIDE ADMINS'] and int(ply['auth']) > 0):

                        reason = reason[8:] if reason.startswith('Kicked:') else reason

                        self.say(MSG['LEAVE MESSAGE'].format(reason=reason, **ply), COLOR['LEAVE MESSAGE'], uid)

                # Log disconnect
                self.log('connections', '{username} disconnected from {country} [UID: {steamid}][IP: {ip}]'.format(**ply))

            # Decache player
            del self.cache[uid]

    # -------------------------------------------------------------------------
    # - COMMAND FUNCTIONS
    def rules_CMD(self, player, cmd, args):
        ''' Rules command function '''

        lang = self.playerlang(player, args[0] if args else None)

        if lang:

            rules = RULES[lang]

            s = {
                'EN': 'English', 'PT': 'Portuguese', 'ES': 'Spanish',
                'RO': 'Romanian', 'FR': 'French', 'IT': 'Italian',
                'DK': 'Danish', 'TR': 'Turk', 'NL': 'Dutch',
                'RU': 'Russian', 'UA': 'Ukrainian', 'DE': 'German',
                'HU': 'Hungarian'
            }

            if rules:

                self.tell(player, '%s <%s>%s<end>:' % (self.prefix if self.prefix else '', COLOR['BOARDS TITLE'], MSG['RULES TITLE']), f=False)
                self.tell(player, LINE, f=False)

                for n, line in enumerate(rules):

                    self.tell(player, '%s. %s' % (n + 1, line), 'orange', f=False)

                if lang in s:

                    self.tell(player, LINE, f=False)
                    self.tell(player, 'Language: <grey>%s<end>' % s[lang], 'silver', f=False)

            else: self.tell(player, MSG['NO RULES'], COLOR['white'])

    # -------------------------------------------------------------------------
    def players_list_CMD(self, player, cmd, args):
        ''' Players List command function '''

        active = self.activelist()

        title = '%s <%s>%s<end>:' % (self.prefix if self.prefix else '', COLOR['BOARDS TITLE'], MSG['PLAYERS LIST TITLE'])

        # Show list on chat?
        if PLUGIN['PLAYERS LIST ON CHAT']:

            # Divide names in chunks before sending to chat
            names = [self.cache[self.playerid(i)]['username'] for i in active]
            names = [names[i:i+3] for i in xrange(0, len(names), 3)]

            self.tell(player, title, f=False)
            self.tell(player, LINE, f=False)

            for i in names:
            
                self.tell(player, ', '.join(i), COLOR['SYSTEM'], f=False)

        if PLUGIN['PLAYERS LIST ON CONSOLE']:

            self.tell(player, LINE, f=False)
            self.tell(player, '(%s)' % MSG['CHECK CONSOLE'], 'orange', f=False)

            self.pcon(player, LINE)
            self.pcon(player, title)
            self.pcon(player, LINE)

            inv = {v: k for k, v in self.countries.items()}

            for n, ply in enumerate(active):

                i = self.cache[self.playerid(ply)]

                self.pcon(player, '<orange>{num}<end> | {steamid}| {countryshort} | <lime>{username}<end>'.format(
                    num='%03d' % (n + 1),
                    countryshort=inv[i['country']],
                    **i
                ), 'white')

            self.pcon(player, LINE)
            self.pcon(player, MSG['PLAYERS ONLINE'].format(active=str(len(active)), maxplayers=sv.maxplayers), 'orange')
            self.pcon(player, LINE)

    # -------------------------------------------------------------------------
    def players_online_CMD(self, player, cmd, args):
        ''' Player Online command function '''

        active = self.activelist()
        sleepers = self.sleeperlist()

        self.tell(player, '%s <%s>%s<end>:' % (self.prefix if self.prefix else '', COLOR['BOARDS TITLE'], MSG['PLAYERS ONLINE TITLE']), f=False)
        self.tell(player, LINE, f=False)
        self.tell(player, MSG['PLAYERS ONLINE'].format(active=str(len(active)), maxplayers=str(sv.maxplayers)), f=False)

        if not PLUGIN['HIDE ADMINS']:

            admins = [i for i in active if i.IsAdmin()]

            self.tell(player, MSG['ADMINS ONLINE'].format(admins=str(len(admins))), f=False)

        self.tell(player, MSG['PLAYERS STATS'].format(sleepers=str(len(sleepers)), alltime=str(len(active) + len(sleepers))), f=False)

    # --------------------------------------------------------------------------
    def admins_list_CMD(self, player, cmd, args):
        ''' Admins List command function '''

        names = [self.cache[self.playerid(i)]['username'] for i in self.activelist() if i.IsAdmin()]
        names = [names[i:i+3] for i in xrange(0, len(names), 3)]

        if names and not PLUGIN['HIDE ADMINS'] or player.IsAdmin():

            self.tell(player, '%s <%s>%s<end>:' % (self.prefix if self.prefix else '', COLOR['BOARDS TITLE'], MSG['ADMINS LIST TITLE']), f=False)
            self.tell(player, LINE, f=False)

            for i in names: self.tell(player, ', '.join(i), 'white', f=False)

        else: self.tell(player, MSG['NO ADMINS'], COLOR['SYSTEM'])

    # -------------------------------------------------------------------------
    def plugins_list_CMD(self, player, cmd, args):
        ''' Plugins List command function '''

        self.tell(player, '%s <%s>%s<end>:' % (self.prefix if self.prefix else '', COLOR['BOARDS TITLE'], MSG['PLUGINS LIST TITLE']), f=False)
        self.tell(player, LINE, f=False)

        for i in plugins.GetAll():

            if i.Author != 'Oxide Team':
                
                self.tell(player, '<lime>{plugin.Title}<end> <grey>v{plugin.Version}<end> by {plugin.Author}'.format(plugin=i), f=False)

    # --------------------------------------------------------------------------
    def map_link_CMD(self, player, cmd, args):
        ''' Server Map command function '''

        self.tell(player, MSG['MAP LINK'].format(ip=str(sv.ip), port=str(sv.port)))

    # --------------------------------------------------------------------------
    def adverts_command_CMD(self, player, cmd, args):
        ''' Adverts Command command function '''

        if args:

            if player.IsAdmin() and self.adverts_loop:

                try:

                    n = int(args[0])

                    if n:

                        self.adverts_loop.Destroy()
                        self.adverts_loop = timer.Repeat(n * 60, 0, Action(self.send_advert), self.Plugin)

                        PLUGIN['ADVERTS INTERVAL'] = n

                        self.SaveConfig()

                        self.tell(player, MSG['ADVERTS INTERVAL CHANGED'].format(minutes=str(n)), COLOR['SYSTEM'])

                except: self.tell(player, MSG['SYNTAX ERROR'].format(syntax='/adverts <minutes> (i.g /adverts 5)'), 'red')

        else: self.tell(player, MSG['SYNTAX ERROR'].format(syntax='/adverts <minutes> (i.g /adverts 5)'), 'red')

    # --------------------------------------------------------------------------
    def plugin_CMD(self, player, cmd, args):
        ''' Plugin command function '''

        if args and args[0] == 'help':

            self.tell(player, '%s COMMANDS DESCRIPTION:', f=False)
            self.tell(player, LINE, f=False)

            for cmd in CMDS:

                i = '%s DESC' % cmd

                if i in MSG: self.tell(player, MSG[i], f=False)
        else:

            self.tell(player, '<#00EEEE><size=18>NOTIFIER</size> <grey>v%s<end><end>' % self.Version, profile='76561198235146288', f=False)
            self.tell(player, self.Description, profile='76561198235146288', f=False)
            self.tell(player, 'Plugin developed by <#9810FF>SkinN<end>, powered by <orange>Oxide 2<end>.', profile='76561197999302614', f=False)

    # -------------------------------------------------------------------------
    # - PLUGIN FUNCTIONS / HOOKS
    def playerid(self, player):
        ''' Function to return the player UserID '''

        return rust.UserIDFromPlayer(player)

    # -------------------------------------------------------------------------
    def playername(self, con):
        '''
            Returns the player name with player or Admin default name color
        '''

        if PLUGIN['ENABLE PLAYERS DEFAULT COLORS']:

            if int(con.authLevel) > 0 and not PLUGIN['HIDE ADMINS']:

                return '<#ADFF64>%s<end>' % con.username

            else:

                return '<#6496E1>%s<end>' % con.username

        else: return con.username

    # -------------------------------------------------------------------------
    def playerlang(self, player, f=None):
        ''' Rules language filter '''

        default = PLUGIN['RULES LANGUAGE']

        if f:

            if f.upper() in RULES: return f.upper()

            else:

                self.tell(player, MSG['NO LANG'].replace('{args}', f), COLOR['SYSTEM'])

                return False

        elif default == 'AUTO':

            inv = {v: k for k, v in self.countries.items()}
            lang = inv[self.cache[self.playerid(player)]['country']]

            if lang in ('PT','BR'): lang = 'PT'
            elif lang in ('ES','MX','AR'): lang = 'ES'
            elif lang in ('FR','BE','CH','MC','MU'): lang = 'FR'

            return lang if lang in RULES else 'EN'

        else: return default if default in RULES else 'EN'

    # -------------------------------------------------------------------------
    def activelist(self):
        ''' Returns the active players list '''

        return BasePlayer.activePlayerList

    # -------------------------------------------------------------------------
    def sleeperlist(self):
        ''' Returns the sleepers list '''

        return BasePlayer.sleepingPlayerList

    # -------------------------------------------------------------------------
    def log_date(self):
        ''' Get current date string for logging '''

        localtime = time.localtime()

        return '%02d-%s' % (localtime[1], localtime[0])

    # -------------------------------------------------------------------------
    def cache_player(self, con):
        ''' Caches player information '''

        if con:

            uid = rust.UserIDFromConnection(con)

            self.cache[uid] = {
                'username': self.playername(con),
                'steamid': uid,
                'auth': con.authLevel,
                'country': 'Unknown',
                'ip': con.ipaddress
            }

    # -------------------------------------------------------------------------
    def webrequest_filter(self, player, send=True):
        '''
            Multi functional filter:
            - Player Join Message
            - Cache player country
            - Welcome Message
        '''

        def response_handler(code, response):

            # Webrequest response
            country = response.replace('\n','')

            if country == 'undefined' or code != 200: country = 'Unknown'

            # Cache player country output
            uid = self.playerid(player)
            self.cache[uid]['country'] = self.countries[country]

            if send:

                # Join Message
                if PLUGIN['ENABLE JOIN MESSAGE']:

                    if not (PLUGIN['HIDE ADMINS'] and int(self.cache[uid]['auth']) > 0):

                        self.say(MSG['JOIN MESSAGE'].format(**self.cache[uid]), COLOR['JOIN MESSAGE'], uid)

                # Log player connection to file
                self.log('connections', '{username} connected from {country} [UID: {steamid}][IP: {ip}]'.format(**self.cache[uid]))

                # Welcome Messages
                if PLUGIN['ENABLE WELCOME MESSAGE']:

                    lines = self.Config['WELCOME MESSAGE']

                    if lines:

                        self.tell(player, '\n'*50, f=False)

                        for line in lines:

                            line = line.format(server=sv, **self.cache[uid])

                            self.tell(player, line, COLOR['WELCOME MESSAGE'], f=False)

                    else:

                        PLUGIN['ENABLE WELCOME MESSAGE'] = False

                        self.con('No lines found on Welcome Message, turning it off')

        if player:

            pip = player.net.connection.ipaddress.split(':')[0]
            webrequests.EnqueueGet('http://ipinfo.io/%s/country' % pip, Action[Int32,String](response_handler), self.Plugin)

    # -------------------------------------------------------------------------
    def send_advert(self):
        ''' Function to send adverts to chat '''

        if ADVERTS:

            index = self.lastadvert

            if len(ADVERTS) > 1:

                while index == self.lastadvert:

                    index = random.Range(0, len(ADVERTS))

                self.lastadvert = index

            self.say(ADVERTS[index].format(
                players= len(self.activelist()),
                sleepers=len(self.sleeperlist()),
                server=sv),
            COLOR['ADVERTS'])

        else:

            self.con('The Adverts list is empty, stopping Adverts loop')

            self.adverts_loop.Destroy()

    # -------------------------------------------------------------------------
    def format(self, text, con=False):
        '''
            Replaces color names and RGB hex code into HTML code
        '''

        colors = (
            'red', 'blue', 'green', 'yellow', 'white', 'black', 'cyan',
            'lightblue', 'lime', 'purple', 'darkblue', 'magenta', 'brown',
            'orange', 'olive', 'gray', 'grey', 'silver', 'maroon'
        )

        name = r'\<(\w+)\>'
        hexcode = r'\<(#\w+)\>'
        end = 'end'

        if con:
            for x in (end, name, hexcode):
                for c in re.findall(x, text):
                    if c.startswith('#') or c in colors or x == end:
                        text = text.replace('<%s>' % c, '')
        else:
            text = text.replace('<%s>' % end, '</color>')
            for f in (name, hexcode):
                for c in re.findall(f, text):
                    if c.startswith('#') or c in colors: text = text.replace('<%s>' % c, '<color=%s>' % c)
        return text

    # -------------------------------------------------------------------------
    def SendHelpText(self, player):
        ''' Hook called from HelpText plugin when /help is triggered '''

        self.tell(player, 'For all <#00EEEE>Notifier<end>\'s commands type <orange>/notifier help<end>', f=False)

    # -------------------------------------------------------------------------
    def countries_dict(self):
        ''' Returns a dictionary with countries full name '''

        return {
            'Unknown':'Unknown',
            'BD':'Bangladesh',
            'BE':'Belgium',
            'BF':'Burkina Faso',
            'BG':'Bulgaria',
            'BA':'Bosnia and Herzegovina',
            'BB':'Barbados',
            'WF':'Wallis and Futuna',
            'BN':'Brunei Darussalam',
            'BO':'Bolivia',
            'JP':'Japan',
            'BI':'Burundi',
            'BJ':'Benin',
            'BT':'Bhutan',
            'JM':'Jamaica',
            'BV':'Bouvet Island',
            'BW':'Botswana',
            'WS':'Samoa',
            'BQ':'British Antarctic Territory',
            'BR':'Brazil',
            'BS':'Bahamas',
            'JE':'Jersey',
            'BY':'Belarus',
            'BZ':'Belize',
            'RU':'Russia',
            'RW':'RWANDA',
            'TL':'Timor-Leste',
            'RE':'Reunion',
            'PA':'Panama',
            'BM':'Bermuda',
            'TJ':'Tajikistan',
            'RO':'Romania',
            'TK':'Tokelau',
            'GW':'Guinea-Bissau',
            'GU':'Guam',
            'GT':'Guatemala',
            'GS':'South Georgia and the South Sandwich Islands',
            'GR':'Greece',
            'GQ':'Equatorial Guinea',
            'GP':'Guadeloupe',
            'BH':'Bahrain',
            'GY':'Guyana',
            'GG':'Guernsey',
            'GF':'French Guiana',
            'GE':'Georgia',
            'GD':'Grenada',
            'GB':'United Kingdom',
            'GA':'Gabon',
            'GN':'Guinea',
            'GM':'Gambia',
            'GL':'Greenland',
            'GI':'Gibraltar',
            'GH':'Ghana',
            'OM':'Oman',
            'IL':'Israel',
            'JO':'Jordan',
            'HR':'Croatia',
            'HT':'Haiti',
            'HU':'Hungary',
            'HK':'Hong Kong',
            'HN':'Honduras',
            'KM':'Comoros',
            'HM':'Heard Island and Mcdonald Islands',
            'VE':'Venezuela',
            'PR':'Puerto Rico',
            'PS':'Palestinian Territory, Occupied',
            'PW':'Palau',
            'PT':'Portugal',
            'PU':'U.S. Miscellaneous Pacific Islands',
            'AF':'Afghanistan',
            'IQ':'Iraq',
            'LV':'Latvia',
            'PF':'French Polynesia',
            'PG':'Papua New Guinea',
            'PE':'Peru',
            'PK':'Pakistan',
            'PH':'Philippines',
            'PN':'Pitcairn',
            'TM':'Turkmenistan',
            'PL':'Poland',
            'PM':'Saint Pierre and Miquelon',
            'ZM':'Zambia',
            'EH':'Western Sahara',
            'EE':'Estonia',
            'EG':'Egypt',
            'ZA':'South Africa',
            'EC':'Ecuador',
            'AL':'Albania',
            'VN':'Viet Nam',
            'SB':'Solomon Islands',
            'ET':'Ethiopia',
            'SO':'Somalia',
            'ZW':'Zimbabwe',
            'SA':'Saudi Arabia',
            'ES':'Spain',
            'ER':'Eritrea',
            'ME':'Montenegro',
            'MD':'Moldova',
            'MG':'Madagascar',
            'MA':'Morocco',
            'MC':'Monaco',
            'UZ':'Uzbekistan',
            'MM':'Myanmar',
            'ML':'Mali',
            'MO':'Macao',
            'MN':'Mongolia',
            'MH':'Marshall Islands',
            'US':'United States',
            'UM':'U.S. Minor Outlying Islands',
            'MT':'Malta',
            'MW':'Malawi',
            'MV':'Maldives',
            'MQ':'Martinique',
            'MP':'Northern Mariana Islands',
            'MS':'Montserrat',
            'MR':'Mauritania',
            'IM':'Isle of Man',
            'UG':'Uganda',
            'TZ':'Tanzania',
            'UA':'Ukraine',
            'MX':'Mexico',
            'MZ':'Mozambique',
            'FQ':'French Southern and Antarctic Territories',
            'FR':'France',
            'AW':'Aruba',
            'FX':'Metropolitan France',
            'SH':'Saint Helena',
            'SJ':'Svalbard and Jan Mayen',
            'FI':'Finland',
            'FJ':'Fiji',
            'FK':'Falkland Islands (Malvinas)',
            'FM':'Federated States of Micronesia',
            'FO':'Faroe Islands',
            'NI':'Nicaragua',
            'NL':'Netherlands',
            'NO':'Norway',
            'NA':'Namibia',
            'VU':'Vanuatu',
            'NC':'New Caledonia',
            'NE':'Niger',
            'NF':'Norfolk Island',
            'NG':'Nigeria',
            'NZ':'New Zealand',
            'NP':'Nepal',
            'NR':'Nauru',
            'NU':'Niue',
            'CK':'Cook Islands',
            'CI':'Cote D\'Ivoire',
            'CH':'Switzerland',
            'CO':'Colombia',
            'CN':'China',
            'CM':'Cameroon',
            'CL':'Chile',
            'CC':'Cocos (Keeling) Islands',
            'CA':'Canada',
            'CG':'Congo',
            'CF':'Central African Republic',
            'CD':'Congo',
            'CZ':'Czech Republic',
            'CY':'Cyprus',
            'CX':'Christmas Island',
            'CS':'Serbia and Montenegro',
            'CR':'Costa Rica',
            'PY':'Paraguay',
            'CV':'Cape Verde',
            'CU':'Cuba',
            'SZ':'Swaziland',
            'SY':'Syrian Arab Republic',
            'KG':'Kyrgyzstan',
            'KE':'Kenya',
            'SR':'Suriname',
            'KI':'Kiribati',
            'KH':'Cambodia',
            'SV':'El Salvador',
            'SU':'Union of Soviet Socialist Republics',
            'ST':'Sao Tome and Principe',
            'SK':'Slovakia',
            'KR':'Republic of Korea',
            'SI':'Slovenia',
            'KP':'Korea',
            'KW':'Kuwait',
            'SN':'Senegal',
            'SM':'San Marino',
            'SL':'Sierra Leone',
            'SC':'Seychelles',
            'KZ':'Kazakhstan',
            'KY':'Cayman Islands',
            'SG':'Singapore',
            'SE':'Sweden',
            'SD':'Sudan',
            'DO':'Dominican Republic',
            'DM':'Dominica',
            'DJ':'Djibouti',
            'DK':'Denmark',
            'DD':'East Germany',
            'DE':'Germany',
            'YE':'Yemen',
            'DZ':'Algeria',
            'MK':'Macedonia',
            'UY':'Uruguay',
            'YT':'Mayotte',
            'MU':'Mauritius',
            'KN':'Saint Kitts and Nevis',
            'LB':'Lebanon',
            'LC':'Saint Lucia',
            'LA':'Lao People\'S Democratic Republic',
            'TV':'Tuvalu',
            'TW':'Taiwan, Province of China',
            'TT':'Trinidad and Tobago',
            'TR':'Turkey',
            'LK':'Sri Lanka',
            'LI':'Liechtenstein',
            'TN':'Tunisia',
            'TO':'Tonga',
            'LT':'Lithuania',
            'LU':'Luxembourg',
            'LR':'Liberia',
            'LS':'Lesotho',
            'TH':'Thailand',
            'TF':'French Southern Territories',
            'TG':'Togo',
            'TD':'Chad',
            'TC':'Turks and Caicos Islands',
            'LY':'Libyan Arab Jamahiriya',
            'VA':'Holy See (Vatican City State)',
            'VC':'Saint Vincent and the Grenadines',
            'AE':'United Arab Emirates',
            'AD':'Andorra',
            'AG':'Antigua and Barbuda',
            'VG':'British Virgin Islands',
            'AI':'Anguilla',
            'VI':'U.S. Virgin Islands',
            'IS':'Iceland',
            'IR':'Iran, Islamic Republic Of',
            'AM':'Armenia',
            'IT':'Italy',
            'AO':'Angola',
            'AN':'Netherlands Antilles',
            'AQ':'Antarctica',
            'AS':'American Samoa',
            'AR':'Argentina',
            'AU':'Australia',
            'AT':'Austria',
            'IO':'British Indian Ocean Territory',
            'IN':'India',
            'AX':'land Islands',
            'AZ':'Azerbaijan',
            'IE':'Ireland',
            'ID':'Indonesia',
            'MY':'Malaysia',
            'QA':'Qatar'
        }