#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import os
import re
import sys
import types
import warnings
import argparse
import inspect

__all__ = ["Command", "Server", "Manager", "Group", "Option"]

safe_actions = (argparse._StoreAction,
                argparse._StoreConstAction,
                argparse._StoreTrueAction,
                argparse._StoreFalseAction,
                argparse._AppendAction,
                argparse._AppendConstAction,
                argparse._CountAction)

try:
    import argcomplete
    ARGCOMPLETE_IMPORTED = True
except ImportError:
    ARGCOMPLETE_IMPORTED = False


def add_help(parser, help_args):
    if not help_args:
        return
    parser.add_argument(*help_args,
                        action='help', default=argparse.SUPPRESS, help= 'show this help message and exit')

iteritems = lambda d: iter(d.items())
izip = zip
text_type = str


class InvalidCommand(Exception):
    """\
        This is a generic error for "bad" commands.
        It is not used in Flask-Script itself, but you should throw
        this error (or one derived from it) in your command handlers,
        and your main code should display this error's message without
        a stack trace.

        This way, we maintain interoperability if some other plug-in code
        supplies Flask-Script hooks.
        """
    pass


class Group(object):
    """
    Stores argument groups and mutually exclusive groups for
    `ArgumentParser.add_argument_group <http://argparse.googlecode.com/svn/trunk/doc/other-methods.html#argument-groups>`
    or `ArgumentParser.add_mutually_exclusive_group <http://argparse.googlecode.com/svn/trunk/doc/other-methods.html#add_mutually_exclusive_group>`.

    Note: The title and description params cannot be used with the exclusive
    or required params.

    :param options: A list of Option classes to add to this group
    :param title: A string to use as the title of the argument group
    :param description: A string to use as the description of the argument
                        group
    :param exclusive: A boolean indicating if this is an argument group or a
                      mutually exclusive group
    :param required: A boolean indicating if this mutually exclusive group
                     must have an option selected
    """

    def __init__(self, *options, **kwargs):
        self.option_list = options

        self.title = kwargs.pop("title", None)
        self.description = kwargs.pop("description", None)
        self.exclusive = kwargs.pop("exclusive", None)
        self.required = kwargs.pop("required", None)

        if ((self.title or self.description) and
                (self.required or self.exclusive)):
            raise TypeError("title and/or description cannot be used with "
                            "required and/or exclusive.")

        super(Group, self).__init__(**kwargs)

    def get_options(self):
        """
        By default, returns self.option_list. Override if you
        need to do instance-specific configuration.
        """
        return self.option_list


class Option(object):
    """
    Stores positional and optional arguments for `ArgumentParser.add_argument
    <http://argparse.googlecode.com/svn/trunk/doc/add_argument.html>`_.

    :param name_or_flags: Either a name or a list of option strings,
                          e.g. foo or -f, --foo
    :param action: The basic type of action to be taken when this argument
                   is encountered at the command-line.
    :param nargs: The number of command-line arguments that should be consumed.
    :param const: A constant value required by some action and nargs selections.
    :param default: The value produced if the argument is absent from
                    the command-line.
    :param type: The type to which the command-line arg should be converted.
    :param choices: A container of the allowable values for the argument.
    :param required: Whether or not the command-line option may be omitted
                     (optionals only).
    :param help: A brief description of what the argument does.
    :param metavar: A name for the argument in usage messages.
    :param dest: The name of the attribute to be added to the object
                 returned by parse_args().
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Command(object):
    """
    Base class for creating commands.

    :param func:  Initialize this command by introspecting the function.
    """

    option_list = ()
    help_args = None

    def __init__(self, func=None):
        if func is None:
            if not self.option_list:
                self.option_list = []
            return

        args, varargs, keywords, defaults = inspect.getargspec(func)
        if inspect.ismethod(func):
            args = args[1:]

        options = []

        # first arg is always "app" : ignore

        defaults = defaults or []
        kwargs = dict(izip(*[reversed(l) for l in (args, defaults)]))

        for arg in args:

            if arg in kwargs:

                default = kwargs[arg]

                if isinstance(default, bool):
                    options.append(Option('-%s' % arg[0],
                                          '--%s' % arg,
                                          action="store_true",
                                          dest=arg,
                                          required=False,
                                          default=default))
                else:
                    options.append(Option('-%s' % arg[0],
                                          '--%s' % arg,
                                          dest=arg,
                                          type=text_type,
                                          required=False,
                                          default=default))

            else:
                options.append(Option(arg, type=text_type))

        self.run = func
        self.__doc__ = func.__doc__
        self.option_list = options

    @property
    def description(self):
        description = self.__doc__ or ''
        return description.strip()

    def add_option(self, option):
        """
        Adds Option to option list.
        """
        self.option_list.append(option)

    def get_options(self):
        """
        By default, returns self.option_list. Override if you
        need to do instance-specific configuration.
        """
        return self.option_list

    def create_parser(self, *args, **kwargs):
        func_stack = kwargs.pop('func_stack',())
        parent = kwargs.pop('parent',None)
        parser = argparse.ArgumentParser(*args, add_help=False, **kwargs)
        help_args = self.help_args
        while help_args is None and parent is not None:
            help_args = parent.help_args
            parent = getattr(parent,'parent',None)

        if help_args:
            add_help(parser,help_args)

        for option in self.get_options():
            if isinstance(option, Group):
                if option.exclusive:
                    group = parser.add_mutually_exclusive_group(
                        required=option.required,
                    )
                else:
                    group = parser.add_argument_group(
                        title=option.title,
                        description=option.description,
                    )
                for opt in option.get_options():
                    group.add_argument(*opt.args, **opt.kwargs)
            else:
                parser.add_argument(*option.args, **option.kwargs)

        parser.set_defaults(func_stack=func_stack+(self,))

        self.parser = parser
        self.parent = parent
        return parser

    def __call__(self, app=None, *args, **kwargs):
        """
        Handles the command with the given app.
        Default behaviour is to call ``self.run`` within a test request context.
        """
        # with app.test_request_context():
        return self.run(*args, **kwargs)

    def run(self):
        """
        Runs a command. This must be implemented by the subclass. Should take
        arguments as configured by the Command options.
        """
        raise NotImplementedError


class Manager(object):
    """
    Controller class for handling a set of commands.

    Typical usage::

        class Print(Command):

            def run(self):
                print "hello"

        app = Flask(__name__)

        manager = Manager(app)
        manager.add_command("print", Print())

        if __name__ == "__main__":
            manager.run()

    On command line::

        python manage.py print
        > hello

    :param app: Flask instance, or callable returning a Flask instance.
    :param with_default_commands: load commands **runserver** and **shell**
                                  by default.
    :param disable_argcomplete: disable automatic loading of argcomplete.

    """
    help_args = ('-?','--help')

    def __init__(self, app=None, with_default_commands=None, usage=None,
                 help=None, description=None, disable_argcomplete=False):

        self.app = app

        self._commands = dict()
        self._options = list()

        self.usage = usage
        self.help = help if help is not None else usage
        self.description = description if description is not None else usage
        self.disable_argcomplete = disable_argcomplete
        self.with_default_commands = with_default_commands

        self.parent = None

    def add_default_commands(self):
        """
        Add runserver default commands. To override these,
        simply add your own equivalents using add_command or decorators.
        """

        if "runserver" not in self._commands:
            self.add_command("runserver", Server())

    def add_option(self, *args, **kwargs):
        """
        Adds a global option. This is useful if you want to set variables
        applying to the application setup, rather than individual commands.

        For this to work, the manager must be initialized with a factory
        function rather than a Flask instance. Otherwise any options you set
        will be ignored.

        The arguments are then passed to your function, e.g.::

            def create_my_app(config=None):
                app = Flask(__name__)
                if config:
                    app.config.from_pyfile(config)

                return app

            manager = Manager(create_my_app)
            manager.add_option("-c", "--config", dest="config", required=False)
            @manager.command
            def mycommand(app):
                app.do_something()

        and are invoked like this::

            > python manage.py -c dev.cfg mycommand

        Any manager options passed on the command line will not be passed to
        the command.

        Arguments for this function are the same as for the Option class.
        """

        self._options.append(Option(*args, **kwargs))

    def __call__(self, app=None, **kwargs):
        """
        This procedure is called with the App instance (if this is a
        sub-Manager) and any options.

        If your sub-Manager does not override this, any values for options will get lost.
        """
        if app is None:
            app = self.app
            if app is None:
                raise Exception("There is no app here. This is unlikely to work.")

        # if isinstance(app, Flask):
        #     if kwargs:
        #         import warnings
        #         warnings.warn("Options will be ignored.")
        #     return app

        # app = app(**kwargs)
        self.app = app
        return app

    def create_app(self, *args, **kwargs):
        warnings.warn("create_app() is deprecated; use __call__().", warnings.DeprecationWarning)
        return self(*args,**kwargs)

    def create_parser(self, prog, func_stack=(), parent=None):
        """
        Creates an ArgumentParser instance from options returned
        by get_options(), and subparser for the given commands.
        """
        prog = os.path.basename(prog)
        func_stack=func_stack+(self,)

        options_parser = argparse.ArgumentParser(add_help=False)
        for option in self.get_options():
            options_parser.add_argument(*option.args, **option.kwargs)

        parser = argparse.ArgumentParser(prog=prog, usage=self.usage,
                                         description=self.description,
                                         parents=[options_parser],
                                         add_help=False)
        add_help(parser, self.help_args)

        self._patch_argparser(parser)

        subparsers = parser.add_subparsers()

        for name, command in self._commands.items():
            usage = getattr(command, 'usage', None)
            help = getattr(command, 'help', None)
            if help is None: help = command.__doc__
            description = getattr(command, 'description', None)
            if description is None: description = command.__doc__

            command_parser = command.create_parser(name, func_stack=func_stack, parent=self)

            subparser = subparsers.add_parser(name, usage=usage, help=help,
                                              description=description,
                                              parents=[command_parser],
                                              add_help=False)

            if isinstance(command, Manager):
                self._patch_argparser(subparser)

        ## enable autocomplete only for parent parser when argcomplete is
        ## imported and it is NOT disabled in constructor
        if parent is None and ARGCOMPLETE_IMPORTED \
                and not self.disable_argcomplete:
            argcomplete.autocomplete(parser, always_complete_options=True)

        self.parser = parser
        return parser

    # def foo(self, app, *args, **kwargs):
    #     print(args)

    def _patch_argparser(self, parser):
        """
        Patches the parser to print the full help if no arguments are supplied
        """

        def _parse_known_args(self, arg_strings, *args, **kw):
            if not arg_strings:
                self.print_help()
                self.exit(2)

            return self._parse_known_args2(arg_strings, *args, **kw)

        parser._parse_known_args2 = parser._parse_known_args
        parser._parse_known_args = types.MethodType(_parse_known_args, parser)

    def get_options(self):
        return self._options

    def add_command(self, *args, **kwargs):
        """
        Adds command to registry.

        :param command: Command instance
        :param name: Name of the command (optional)
        :param namespace: Namespace of the command (optional; pass as kwarg)
        """

        if len(args) == 1:
            command = args[0]
            name = None

        else:
            name, command = args

        if name is None:
            if hasattr(command, 'name'):
                name = command.name

            else:
                name = type(command).__name__.lower()
                name = re.sub(r'command$', '', name)

        if isinstance(command, Manager):
            command.parent = self

        if isinstance(command, type):
            command = command()

        namespace = kwargs.get('namespace')
        if not namespace:
            namespace = getattr(command, 'namespace', None)

        if namespace:
            if namespace not in self._commands:
                self.add_command(namespace, Manager())

            self._commands[namespace]._commands[name] = command

        else:
            self._commands[name] = command

    def command(self, func):
        """
        Decorator to add a command function to the registry.

        :param func: command function.Arguments depend on the
                     options.

        """

        command = Command(func)
        self.add_command(func.__name__, command)

        return func

    def option(self, *args, **kwargs):
        """
        Decorator to add an option to a function. Automatically registers the
        function - do not use together with ``@command``. You can add as many
        ``@option`` calls as you like, for example::

            @option('-n', '--name', dest='name')
            @option('-u', '--url', dest='url')
            def hello(name, url):
                print "hello", name, url

        Takes the same arguments as the ``Option`` constructor.
        """

        option = Option(*args, **kwargs)

        def decorate(func):
            name = func.__name__

            if name not in self._commands:

                command = Command()
                command.run = func
                command.__doc__ = func.__doc__
                command.option_list = []

                self.add_command(name, command)

            self._commands[name].option_list.append(option)
            return func
        return decorate

    def set_defaults(self):
        if self.with_default_commands is None:
            self.with_default_commands = self.parent is None
        if self.with_default_commands:
            self.add_default_commands()
        self.with_default_commands = False

    def handle(self, prog, args=None):
        self.set_defaults()
        app_parser = self.create_parser(prog)

        args = list(args or [])
        app_namespace, remaining_args = app_parser.parse_known_args(args)

        # get the handle function and remove it from parsed options
        kwargs = app_namespace.__dict__
        func_stack = kwargs.pop('func_stack', None)
        if not func_stack:
            app_parser.error('too few arguments')

        last_func = func_stack[-1]
        if remaining_args and not getattr(last_func, 'capture_all_args', False):
            app_parser.error('too many arguments')

        args = []
        for handle in func_stack:

            # get only safe config options
            config_keys = [action.dest for action in handle.parser._actions
                               if handle is last_func or action.__class__ in safe_actions]

            # pass only safe app config keys
            config = dict((k, v) for k, v in iteritems(kwargs)
                          if k in config_keys)

            # remove application config keys from handle kwargs
            kwargs = dict((k, v) for k, v in iteritems(kwargs)
                          if k not in config_keys)

            if handle is last_func and getattr(last_func, 'capture_all_args', False):
                args.append(remaining_args)
            try:
                res = handle(*args, **config)
            except TypeError as err:
                err.args = ("{}: {}".format(handle,str(err)),)
                raise

            args = [res]

        assert not kwargs
        return res

    def run(self, commands=None, default_command=None):
        """
        Prepares manager to receive command line input. Usually run
        inside "if __name__ == "__main__" block in a Python script.

        :param commands: optional dict of commands. Appended to any commands
                         added using add_command().

        :param default_command: name of default command to run if no
                                arguments passed.
        """

        if commands:
            self._commands.update(commands)

        if default_command is not None and len(sys.argv) == 1:
            sys.argv.append(default_command)

        try:
            print sys.argv[0], sys.argv[1:]
            result = self.handle(sys.argv[0], sys.argv[1:])
        except SystemExit as e:
            result = e.code

        sys.exit(result or 0)
        
        
class Server(Command):
    """
    :param host: server host
    :param port: server port
    :param options: : options.
    """

    def __init__(self, host='127.0.0.1', port=5000, **options):

        self.port = port
        self.host = host

    def get_options(self):

        options = (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port)
        )

        return options

    def __call__(self, app, host, port):

        import tornado.ioloop
        import tornado.httpserver
        print host,port
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(port, host)
        tornado.ioloop.IOLoop.instance().start()