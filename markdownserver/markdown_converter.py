from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import markdown as md
import codecs
import sys
import os
from pathlib import Path
from .env import css_path, ms_encoding, markdown_type, \
    html_dir, html_extension


class MarkdownConverter(object):
    def __init__(self):
        css = codecs.open(css_path, encoding=ms_encoding, mode="r")
        self.html_header = (
            """
            <html>
            <head>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js"></script>
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
              config: ["MMLorHTML.js"],
              jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
              extensions: ["MathMenu.js", "MathZoom.js"]
            });
            </script>
            <style type='text/css'>
            <!--
            """
            + css.read()
            + """
            //-->
            </style>
            </head>
            <body>
            <div class='markdown-body'>
            """
        )
        self.page_listing = "<ul>" + \
                            "\n".join(
                                ['<li><a href="{}">{}</li>'.format(f, f)
                                 for f in self.get_child_files(os.getcwd())]) \
                            + "</ul>"

        self.html_footer = """
            <h1>Pages</h1>
            {}
            </div>
            </body>
            </html>
            """.format(self.page_listing)

    def convert(self, src, dst=""):
        code = md.markdown(self.read_md(src), extensions=[markdown_type,
                                                          'mdx_math'])
        return self.write_html(code, src, dst)

    def get_child_files(self, dir):
        all_md_files = sorted([
            f.relative_to(dir) for f in Path(dir).rglob('*.md')],
                          key=lambda x: x.parent)
        return all_md_files

    def read_md(self, file_name):
        workingdir = os.getcwd()
        md_file = codecs.open(
            os.path.join(workingdir, file_name),
            encoding=ms_encoding,
            mode="r"
        )
        return md_file.read()

    def write_html(self, body, file_name, dst):
        html_path = os.path.join(html_dir, file_name + html_extension)

        if dst != "":
            html_path = dst
        try:
            os.makedirs("/".join(html_path.replace("\\", "/").split("/")[:-1]))
        except OSError:
            pass

        html_file = codecs.open(html_path, encoding=ms_encoding, mode="w")
        html_file.write(self.html_header + body + self.html_footer)
        return html_path

    def dir_listing(self, path):
        html = self.html_header
        return


def main():
    args = sys.argv
    if len(args) != 3:
        print("usage: convert source_md_file target_html_file")
    else:
        converter = MarkdownConverter()
        converter.convert(args[1], args[2])


if __name__ == "__main__":
    main()
