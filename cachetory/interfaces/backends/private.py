"""
I could define these type variables in each protocol's module,
but it's easier for a reader to come by a central place and find the additional comments.
"""

from typing import TypeVar

# Value type as accepted and returned by backend read operations (as in «data on wire»).
# Why not just `bytes`? The generic type would allow implementing e.g. a memory backend
# which doesn't necessarily need a serializer and is able to store the values directly.
# See, for example, `SyncMemoryBackend` and `NoopSerializer`.
WireT_co = TypeVar("WireT_co", covariant=True)

# The contravariance ensures that given A > B: SyncBackendWrite[A] < SyncBackendWrite[B],
# meaning that user can safely pass SyncBackendWrite[A] in place of SyncBackendWrite[B].
# And this is needed because SyncBackendWrite[B] accepts B as a parameter,
# and so should SyncBackendWrite[A].
WireT_contra = TypeVar("WireT_contra", contravariant=True)

WireT = TypeVar("WireT")
