#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.pycharm')
use_plugin('pypi:pybuilder_pip_tools', '==1.*')

name = "NBATwitterCorrelation"
default_task = "publish"

@init
def set_properties(project):
    project.set_property('flake8_break_build', True)
    project.depends_on_requirements("requirements.txt")
    project.set_property('coverage_break_build', False)
