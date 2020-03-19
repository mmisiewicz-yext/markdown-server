from __future__ import absolute_import
from bottle import route, run, static_file, abort, template
from .markdown_converter import MarkdownConverter
from .env import root_path, ms_host, ms_port, ms_debug
import os

converter = MarkdownConverter()


@route(r'/<resource:re:.*\.md>')
def gfmize(resource):
    if resource == 'favicon.ico':
        return ''

    html_file_name = os.path.basename(converter.convert(resource))
    if '/' in resource:
        html_file_name = '/'.join(resource.split('/')[:-1]) + \
            '/' + html_file_name
    try:
        return static_file(os.path.join('resources/html',
                                    html_file_name),
                       root=root_path)
    except FileNotFoundError:
        abort(404)


@route(r'/<path>')
def dir_listing(path):
    # Joining the base and the requested path
    abs_path = os.path.join(os.getcwd(), path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # # Check if path is a file and serve
    # if os.path.isfile(abs_path):
    #     return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return str(files)


@route('/')
def index():
    return gfmize("index.md")


def main():
    run(host=ms_host,
        port=ms_port,
        debug=ms_debug,
        reloader=False)


if __name__ == '__main__':
    main()
