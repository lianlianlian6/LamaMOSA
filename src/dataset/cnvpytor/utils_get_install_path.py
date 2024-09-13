from __future__ import absolute_import, print_function, division

from pathlib import Path

def get_install_path():
    """
    Retrieve the installation path of the 'cnvpytor' package.

    This function attempts to locate the installation path of the 'cnvpytor' package.
    It first uses the `importlib.resources` module, available in Python 3.9 and later.
    If `importlib.resources` is not available or an error occurs, the function falls
    back to using the `pkg_resources` module, which is compatible with older Python versions.

    Returns:
        PosixPath: The installation path of the 'cnvpytor' package.
    """
    try:
        from importlib import resources
        data_path = resources.files('cnvpytor')
    except Exception as e:
        import pkg_resources
        data_path = Path(pkg_resources.resource_filename('cnvpytor', ''))
    return data_path
