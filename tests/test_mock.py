from pymoq import Mock

from .interfaces import IWeb


def test__init_with_protocol__works():
    m = Mock(IWeb)
