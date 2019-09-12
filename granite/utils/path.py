from .functional import boost_fn
from path import Path

@boost_fn
def filename(path):
    return Path(path).name

@boost_fn
def extension(path):
    return Path(path).ext