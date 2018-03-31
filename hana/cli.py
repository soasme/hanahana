import click

@click.group()
def hana():
    pass

@hana.command()
def version():
    click.echo('0.1.0')

@hana.command()
def devserver():
    from hana.app import create_app
    app = create_app('HANA_SETTINGS')
    app.run(port=8964, host='0.0.0.0')
