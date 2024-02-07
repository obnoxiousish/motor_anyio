# Author: obnoxious, fuck mongodb for not implementing AnyIO and making me do this
# I fucking hate you.

# Seriously, like a lot.


"""AnyIO support for Motor, an asynchronous driver for MongoDB."""
from . import core, motor_gridfs
from .frameworks import anyio as anyio_framework
from .metaprogramming import T, create_class_with_framework

__all__ = [
    "AnyIOMotorClient",
    "AnyIOMotorClientSession",
    "AnyIOMotorDatabase",
    "AnyIOMotorCollection",
    "AnyIOMotorCursor",
    "AnyIOMotorCommandCursor",
    "AnyIOMotorChangeStream",
    "AnyIOMotorGridFSBucket",
    "AnyIOMotorGridIn",
    "AnyIOMotorGridOut",
    "AnyIOMotorGridOutCursor",
    "AnyIOMotorClientEncryption",
]


def create_anyio_class(cls: T) -> T:
    return create_class_with_framework(
        cls=cls, framework=anyio_framework, module_name="motor.motor_anyio"
    )


AnyIOMotorClient = create_anyio_class(core.AgnosticClient)


AnyIOMotorClientSession = create_anyio_class(core.AgnosticClientSession)


AnyIOMotorDatabase = create_anyio_class(core.AgnosticDatabase)


AnyIOMotorCollection = create_anyio_class(core.AgnosticCollection)


AnyIOMotorCursor = create_anyio_class(core.AgnosticCursor)


AnyIOMotorCommandCursor = create_anyio_class(core.AgnosticCommandCursor)


AnyIOMotorLatentCommandCursor = create_anyio_class(core.AgnosticLatentCommandCursor)


AnyIOMotorChangeStream = create_anyio_class(core.AgnosticChangeStream)


AnyIOMotorGridFSBucket = create_anyio_class(motor_gridfs.AgnosticGridFSBucket)


AnyIOMotorGridIn = create_anyio_class(motor_gridfs.AgnosticGridIn)


AnyIOMotorGridOut = create_anyio_class(motor_gridfs.AgnosticGridOut)


AnyIOMotorGridOutCursor = create_anyio_class(motor_gridfs.AgnosticGridOutCursor)


AnyIOMotorClientEncryption = create_anyio_class(core.AgnosticClientEncryption)
