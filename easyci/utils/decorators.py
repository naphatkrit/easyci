import click

from functools import update_wrapper


def print_markers(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        command = ctx.info_name
        assert command is not None
        _print_marker(' eci ' + command + ' ')
        try:
            return ctx.invoke(f, *args, **kwargs)
        finally:
            _print_marker(' end of eci ' + command + ' ')
    return update_wrapper(new_func, f)


def _print_marker(text):
    width, _ = click.get_terminal_size()
    if len(text) >= width:
        click.echo(text)  # this is probably never the case
    else:
        leftovers = width - len(text)
        click.echo('=' * (leftovers / 2), nl=False)
        click.echo(text, nl=False)
        click.echo('=' * (leftovers / 2 + leftovers % 2))
