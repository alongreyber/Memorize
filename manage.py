import click
import os

@click.command()
@click.argument('environment', required=True, type=click.Choice(['dev', 'prod']))
@click.argument('action', required=True, type=click.Choice(['logs', 'up', 'down', 'ssh', 'sloc', 'test']))
def manage(environment, action):
    # Handle other commands (sloc, ssh)
    if action == 'ssh':
        os.system('ssh root@<not implemented>')
        return
    elif action == 'test':
        os.system('docker-compose build backend')
        os.system('docker-compose run backend pytest')
        return
    elif action == 'sloc':
        os.system("find . -name '*.py' | xargs wc -l")
        os.system("find . -name '*.vue' | xargs wc -l")
        return
    # Main commands (logs, up, down)
    if environment == 'prod':
        host = "DOCKER_HOST='ssh://root@<not implemented>'"
    else:
        host = ""

    if environment == 'prod':
        compose_file = 'docker-compose.prod.yml'
    else:
        compose_file = 'docker-compose.dev.yml'

    if action == 'up':
        extra_args = "--build "
        if environment == 'prod':
            extra_args += "--detach"
        else:
            extra_args += "--abort-on-container-exit"
    else:
        extra_args = ""
    command = f"{host} docker-compose -f docker-compose.yml -f {compose_file} {action} {extra_args}"
    print(command)
    os.system(command)

if __name__ == '__main__':
    manage()
