import codecs
import os.path

import pdoc.render


class StaticError(Exception):
    pass


def module_file(path, m):
    mbase = os.path.join(path, *m.name.split("."))
    if m.is_package():
        return os.path.join(mbase, pdoc.render.html_package_name)
    else:
        return "%s%s" % (mbase, pdoc.render.html_module_suffix)


def quit_if_exists(args, m):
    def check_file(f):
        if os.access(f, os.R_OK):
            raise StaticError("%s already exists. Delete it or run with --overwrite" % f)
    if args.overwrite:
        return
    f = module_file(args, m)
    check_file(f)
    # If this is a package, make sure the package directory doesn't exist
    # either.
    if m.is_package():
        check_file(os.path.dirname(f))


def html_out(
    path,
    m,
    external_links = True,
    link_prefix = "",
    source = False,
):
    f = module_file(path, m)
    dirpath = os.path.dirname(f)
    if not os.access(dirpath, os.R_OK):
        os.makedirs(dirpath)
    with codecs.open(f, "w+", "utf-8") as w:
        out = pdoc.render.html_module(
            m,
            external_links=external_links,
            link_prefix=link_prefix,
            source=source,
        )
        print(out, file=w)
    for submodule in m.submodules():
        html_out(
            path,
            submodule,
            external_links=external_links,
            link_prefix=link_prefix,
            source=source,
        )
