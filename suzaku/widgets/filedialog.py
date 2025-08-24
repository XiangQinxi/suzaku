# dependence on filedialpy

import filedialpy


def ask_open_filename(**options):
    """Ask for a filename to open"""
    cfd.open_file(**options)


def ask_save_as_filename(**options):
    cfd.save_file(**options)


def ask_open_filenames(**options):
    """Ask for a filenames to open"""
    cfd.open_multiple(**options)
    cfd.open_file()
