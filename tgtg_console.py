import cmd
from utils import *
from user import *
from favorites import *
from poll import start_poll
from abc import ABCMeta, abstractmethod

class ClientContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class ContextConsole(cmd.Cmd):
    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.context = context

class MainConsole(ContextConsole):
    def __init__(self, context):
        ContextConsole.__init__(self, context)
        self.account_menu = CreateAccountConsole(context)
        self.add_fav_menu = AddFavConsole(context)
        self.rm_fav_menu = RmFavConsole(context)
        self.prompt = '>'
        self.intro = 'Welcome to the TGTG automated poller.   Type help or ? to list commands.\n'

    def do_debug_mode_on(self, args):
        'Activate debug mode for nerds'
        context.debug=True
        print('Debug mode ON \n')

    def do_create_account(self, args):
        'Creates a new account. WARNING: you will have to re-add all of your favorites!'
        self.account_menu.cmdloop('This will reset your favorites list! Are you sure you wish to continue? (Y/N)')

    def do_list_favs(self, args):
        'List all favorites associated with this account'
        list_favorites(client)

    def do_add_fav(self, args):
        'Add favorite to this account. Type the store name as close as you can to how its name appears on the app. Example: add_fav Le Petit Casino - Place du Pont Neuf'
        closest_match, context.tmpId = closest_favorite(context.client, args, context.debug)
        self.add_fav_menu.cmdloop('Closest match found is {}. Do you wish to continue? (Y/N)'.format(closest_match))
        
    def do_rm_fav(self, args):
        'Remove favorite from this account. Type the store name as close as you can to how its name appears on the app. Example: rm_fav Le Petit Casino - Place du Pont Neuf'
        closest_match, context.tmpId = closest_favorite(context.client, args, context.debug)
        self.rm_fav_menu.cmdloop('Closest match found is {}. Do you wish to continue? (Y/N)'.format(closest_match))

    def do_start_poll(self, args):
        'Begin watching favorites. Will beep every time a new item is made available'
        start_poll(context.client, context.debug)

    def do_quit(self, args):
        'Exits the application'
        return True

class AbstractConfirmationConsole(ContextConsole):
    __metaclass__ = ABCMeta
    def __init__(self, context):
        ContextConsole.__init__(self, context)
        self.prompt = '>>'
    
    @abstractmethod
    def perform_action(self, args):
        pass
        
    def do_Y(self, args):
        self.perform_action(args)
        return True
    
    def do_N(self, args):
        print('\n')
        return True

class CreateAccountConsole(AbstractConfirmationConsole):
    
    def perform_action(self, args):
        context.client = create_account(context.debug)
        print('Created user ' + context.client.email +'\n')

class AddFavConsole(AbstractConfirmationConsole):
    def perform_action(self, args):
        add_favorite(client, context.tmpId)
        print('Store added to favorites')
    
class RmFavConsole(ContextConsole):
    def perform_action(self, args):
        rm_favorite(client, context.tmpId)
        print('Store removed from favorites')

if __name__ == '__main__':
    initial_debug = True # TODO CHANGEME
    #TODO check file presence instead of relying on exception
    try:
        client = read_user()
        print('Using existing login ' + client.email)
    except OSError:
        client = create_account(initial_debug)
        print('No existing login found, created user ' + client.email)
    
    context = ClientContext(debug=initial_debug,client=client)
    con = MainConsole(context)
    con.cmdloop()