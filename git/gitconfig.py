from __future__ import absolute_import
from dotfiles.module_base import *
from dotfiles.package_base import *

class gitconfig(PackageBase):
    def add_config(self, name, value, comment = None):
        self.config.git.config[name] = value
        if comment is not None:
            self.config.git.config[name+'.comment'] = comment

    def build_config_file(self):
        with logger.trylog('configuring .gitconfig'):
            self.config.ensure('git.config')
            self.config.ensure('git.aliases')
            for name in sorted(self.config.git.aliases.keys()):
                value = self.config.git.aliases[name]
                comment = self.config.git.aliases[name+'.comment']
                self.add_config('alias.'+name, value, comment)

        with logger.trylog('Generating .gitconfig file'):
            with open(self.build_file('.gitconfig'), 'w') as f:
                for category in self.config.git.config.keys():
                    f.write('['+category+']\n')
                    for key in self.config.git.config[category].keys():
                        value = self.config.git.config[category][key]
                        comment = self.config.git.config[category][key+'.comment']
                        if comment is not None:
                            f.write('\t# '+comment+'\n')
                        f.write('\t'+key+' = '+self.eval_templates(value)+'\n')
                    f.write('\n')

    def install(self):
        return concat_lists(
            [self.build_config_file],
            self.action('file').symlink(self.home_file('.gitconfig'), self.build_file('.gitconfig'))
        )