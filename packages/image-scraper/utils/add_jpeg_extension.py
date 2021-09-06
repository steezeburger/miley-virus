import os

import click


@click.command()
@click.argument('directory_path')
def add_jpeg_extension(directory_path):
    """
    Renames image files and adds .jpeg extension.
    """
    working_directory = os.path.join(os.getcwd(), directory_path)

    for filename in os.listdir(working_directory):
        if filename == '.gitkeep':
            continue

        click.echo(f'renaming {filename}...')
        old = os.path.join(working_directory, filename)
        new = os.path.join(working_directory, f'{filename}.jpeg')
        os.rename(old, new)


if __name__ == '__main__':
    add_jpeg_extension()
