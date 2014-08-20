from __future__ import absolute_import
from __future__ import print_function
import os
import re
import inspect
import functools
import operator
import StringIO
from dotfiles.util import *
import dotfiles.logger as logger

__abstract__ = True

BUILD_DIR_NAME = 'build'
SRC_DIR_NAME = 'src'

class GlobalContext(object):
    def __init__(self, base_dir, src_dir, config, action_factories):
        self.base_dir = base_dir
        self.src_dir = src_dir
        self.config = config
        self.action_factories = action_factories

    def base_file(self, name):
        return os.path.join(self.base_dir, name)

    def src_file(self, name):
        return os.path.join(self.base_file(SRC_DIR_NAME), name)

    def build_file(self, name):
        return os.path.join(self.base_file(BUILD_DIR_NAME), name)

    def home_file(self, name):
        return os.path.expanduser(os.path.join('~/', name))

    def action(self, name):
        result = find_by_name(self.action_factories, name)
        if result is None:
            raise Exception('Could not find action factory: '+name)
        return result

    def eval_template_content(self, match):
        template_content = match.group(1)
        if '\n' in template_content:
            content = StringIO.StringIO()
            scope = {"__builtins__": __builtins__, "config": self.config, "out": content}
            exec(template_content, scope)
            return content.getvalue()
        else:
            return eval(template_content, {"__builtins__": __builtins__, "config": self.config})

    def eval_templates(self, content):
        return re.sub('{{{{(.*?)}}}}', self.eval_template_content, content, flags=re.DOTALL)


class ModuleContext(object):
    def __init__(self, global_context, wd, builddir, module_common):
        self.global_context = global_context
        self.wd = wd
        self.builddir = builddir
        self.module_common = module_common

    def module_file(self, name):
        return os.path.join(self.wd, name)

    def amend_build_file(self, name, amendment):
        with open(self.build_file(name), 'a') as f:
            f.write(amendment)
    def amend_build_file_with_file(self, name, other_file):
        with open(other_file, 'r') as f:
            self.amend_build_file(name, f.read())

    def concatenate_files_to_build(self, files, build_file):
        for f in files:
            with logger.trylog('amending ' + f + ' -> ' + build_file, verbose=True):
                self.amend_build_file_with_file(build_file, f)

    def download_build_file(self, name, url):
        with logger.trylog('downloading ' + url + ' -> ' + name):
            response = urllib2.urlopen(url)
            contents = response.read()
            with open(self.build_file(name), 'w') as f:
                f.write(contents)

    def eval_file_templates_to_build(self, input_file, out_name):
        with logger.trylog('evaluating templates ' + input_file + ' -> ' + out_name):
            open(self.build_file(out_name), 'w').write(self.eval_templates(open(input_file, 'r').read()))


class ModuleBase(object):
    def __init__(self, context):
        self.context = context
        self.config = context.config

    def __getattr__(self, name):
        return getattr(self.context, name)

    def def_common(self, name, value):
        if name in self.context.module_common.properties:
            raise Exception('Redefinition of ', name)
        self.context.module_common.properties[name] = value

def before(spec):
    def wrap(func):
        if not hasattr(func, 'before'):
            func.before = set()
        func.before.add(spec)
        return func
    return wrap
def after(spec):
    def wrap(func):
        if not hasattr(func, 'after'):
            func.after = set()
        func.after.add(spec)
        return func
    return wrap