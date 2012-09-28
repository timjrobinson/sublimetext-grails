import sublime, sublime_plugin
import os, string, re


class GrailsSyntaxCommand(sublime_plugin.EventListener):
    """ Attempts to set Grails Syntax when appropriate. """


    def __init__(self):
        super(GrailsSyntaxCommand, self).__init__()
        self.path = None
        self.name = None
        self.ext  = None
        self.view = None


    def on_load(self, view):
        self.check_syntax(view)


    def on_post_save(self, view):
        self.check_syntax(view)


    def check_syntax(self, view):
        self.view      = view
        self.file_name = view.file_name()
    
        if not self.file_name: # buffer has never been saved
            return

        self.set_file_variables()

        if not self.ext == '.groovy':
            return

        if self.is_domain():
            self.set_syntax('GrailsDomain', 'Grails/Domain')
        elif self.is_controller():
            self.set_syntax('GrailsController', 'Grails/Controller')
        else:
            self.set_syntax('Groovy', 'Groovy')


    def is_domain(self):
        if 'grails-app/domain' in self.path:
            return True
        return False


    def is_controller(self):
        if 'grails-app/controller' in self.path:
            return True
        return False


    def set_file_variables(self):
        self.path = os.path.dirname(self.file_name)
        self.name = os.path.basename(self.file_name).lower()
        self.name, self.ext = os.path.splitext(self.name)


    def set_syntax(self, syntax, path):
        new_syntax = 'Packages/' + path + '/' + syntax + '.tmLanguage'
        self.view.set_syntax_file(new_syntax)
      current_syntax = self.view.settings().get('syntax')

        if current_syntax != new_syntax:
            self.view.settings().set('syntax', new_syntax)
            print "Switched syntax to: " + syntax
