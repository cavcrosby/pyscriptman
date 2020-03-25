from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
#TODO FIGURE OUT WHY WEBHOST/HOST ARE NOT EXCLUDED FROM NAMESPACE
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and f != "webhost.py"]