import os

from fabric.api import local, abort, run, roles, cd, env, sudo, lcd, env, settings
from fabric.contrib.console import confirm

env.roledefs = {
    'local': ['localhost'],
    'production': [os.getenv('SERVER_DEPLOYMENT_URL')]
}

env.roledefs['all'] = [i for j in env.roledefs.values() for i in j]


def commit(message='updating...'):
    """
    commit changes to staging area
    :param message:
    :return:
    """
    local("git add --all")
    with settings(warn_only=True):
        result = local("git commit -m '%s'" % message, capture=True)
        if result.failed and not confirm("Tests failed. Continue anyway?"):
            abort("Aborting at your behest")


def pull():
    """
    update environment
    :return:
    """
    local("git pull")


def push(message='updating...', branch='master', should_commit=True):
    """
    push changes
    :param message
    :return:
    """
    if should_commit is True:
        commit(message)
    local("git push -u origin %s" % branch)


def ondulate_services(service_paths, cmd='restart'):
    """
    restart list of services
    :param service_paths
    :param cmd
    """
    if not isinstance(service_paths, (tuple, list)):
        raise TypeError('Invalid data type, should be a list')

    for _path in service_paths:
        sudo('/usr/sbin/service %s %s' % (_path, cmd))


def deploy():
    """
    update production environment
    :return:
    """
    with cd('/opt'):
        sudo('git clone https://github.com/stikks/Feature-Request.git')
        with cd('Feature-Request'):
            sudo('bash setup.sh')
            sudo('cat conf/gunicorn.conf >> /etc/init/gunicorn.conf')
            sudo('cp conf/feature /etc/nginx/sites-available/')
            sudo('ln -s /etc/nginx/sites-available/feature /etc/nginx/sites-enabled/feature')
            ondulate_services(['gunicorn', 'nginx'])


