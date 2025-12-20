# dependence on filedialpy
import warnings

filedialpy_is_available = False
try:
    import filedialpy

    filedialpy_is_available = True
except ImportError:
    pass


def warn_filedialpy_not_available():
    warnings.warn("filedialpy is not available, cannot ask for filename")


def ask_open_filename(*args, **kwargs) -> str | None:
    """Ask for a filename to open"""

    if filedialpy_is_available:
        return filedialpy.openFile(*args, **kwargs)
    else:
        warn_filedialpy_not_available()
        return None


def ask_save_as_filename(*args, **kwargs) -> str | None:
    if filedialpy_is_available:
        return filedialpy.saveFile(*args, **kwargs)
    else:
        warn_filedialpy_not_available()
        return None


def ask_open_filenames(*args, **kwargs) -> list[str] | None:
    """Ask for a filenames to open"""
    if filedialpy_is_available:
        return filedialpy.openFiles(*args, **kwargs)
    else:
        warn_filedialpy_not_available()
        return None


def ask_open_dir(*args, **kwargs) -> str | None:
    if filedialpy_is_available:
        return filedialpy.openDir(*args, **kwargs)
    else:
        warn_filedialpy_not_available()
        return None


def ask_open_dirs(*args, **kwargs) -> list[str] | None:
    if filedialpy_is_available:
        return filedialpy.openDirs(*args, **kwargs)
    else:
        warn_filedialpy_not_available()
        return None
