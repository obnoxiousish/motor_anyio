# Copyright 2013-2015 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import test
import unittest
from abc import ABC
from asyncio import new_event_loop, set_event_loop
from multiprocessing import Pipe
from test.asyncio_tests import AsyncIOTestCase, asyncio_test
from test.utils import ignore_deprecations

import pymongo
from pymongo import WriteConcern
from pymongo.read_preferences import Nearest, ReadPreference, Secondary

from motor import motor_asyncio


class AIOMotorTestBasic(AsyncIOTestCase):
    def test_repr(self):
        self.assertTrue(repr(self.cx).startswith("AsyncIOMotorClient"))
        self.assertTrue(repr(self.db).startswith("AsyncIOMotorDatabase"))
        self.assertTrue(repr(self.collection).startswith("AsyncIOMotorCollection"))

        cursor = self.collection.find()
        self.assertTrue(repr(cursor).startswith("AsyncIOMotorCursor"))

    @asyncio_test
    async def test_write_concern(self):
        # Default empty dict means "w=1"
        self.assertEqual(WriteConcern(), self.cx.write_concern)

        await self.collection.delete_many({})
        await self.collection.insert_one({"_id": 0})

        for wc_opts in [
            {},
            {"w": 0},
            {"w": 1},
            {"wTimeoutMS": 1000},
        ]:
            cx = self.asyncio_client(test.env.uri, **wc_opts)
            wtimeout = wc_opts.pop("wTimeoutMS", None)
            if wtimeout:
                wc_opts["wtimeout"] = wtimeout
            wc = WriteConcern(**wc_opts)
            self.assertEqual(wc, cx.write_concern)

            db = cx.motor_test
            self.assertEqual(wc, db.write_concern)

            collection = db.test_collection
            self.assertEqual(wc, collection.write_concern)

            if wc.acknowledged:
                with self.assertRaises(pymongo.errors.DuplicateKeyError):
                    await collection.insert_one({"_id": 0})
            else:
                await collection.insert_one({"_id": 0})  # No error

            # No error
            c = collection.with_options(write_concern=WriteConcern(w=0))
            await c.insert_one({"_id": 0})
            cx.close()

    @ignore_deprecations
    @asyncio_test
    async def test_read_preference(self):
        # Check the default
        cx = motor_asyncio.AsyncIOMotorClient(test.env.uri, io_loop=self.loop)
        self.assertEqual(ReadPreference.PRIMARY, cx.read_preference)

        # We can set mode, tags, and latency.
        cx = self.asyncio_client(
            read_preference=Secondary(tag_sets=[{"foo": "bar"}]), localThresholdMS=42
        )

        self.assertEqual(ReadPreference.SECONDARY.mode, cx.read_preference.mode)
        self.assertEqual([{"foo": "bar"}], cx.read_preference.tag_sets)
        self.assertEqual(42, cx.options.local_threshold_ms)

        # Make a MotorCursor and get its PyMongo Cursor
        collection = cx.motor_test.test_collection.with_options(
            read_preference=Nearest(tag_sets=[{"yay": "jesse"}])
        )

        motor_cursor = collection.find()
        cursor = motor_cursor.delegate

        self.assertEqual(Nearest(tag_sets=[{"yay": "jesse"}]), cursor._read_preference())

        cx.close()

    def test_underscore(self):
        self.assertIsInstance(self.cx["_db"], motor_asyncio.AsyncIOMotorDatabase)
        self.assertIsInstance(self.db["_collection"], motor_asyncio.AsyncIOMotorCollection)
        self.assertIsInstance(self.collection["_collection"], motor_asyncio.AsyncIOMotorCollection)

        with self.assertRaises(AttributeError):
            self.cx._db

        with self.assertRaises(AttributeError):
            self.db._collection

        with self.assertRaises(AttributeError):
            self.collection._collection

    def test_abc(self):
        class C(ABC):
            db = self.db
            collection = self.collection
            subcollection = self.collection.subcollection

        # MOTOR-104, TypeError: Can't instantiate abstract class C with abstract
        # methods collection, db, subcollection.
        C()

    @asyncio_test
    async def test_inheritance(self):
        class CollectionSubclass(motor_asyncio.AsyncIOMotorCollection):
            pass

        class DatabaseSubclass(motor_asyncio.AsyncIOMotorDatabase):
            def __getitem__(self, name):
                return CollectionSubclass(self, name)

        class ClientSubclass(motor_asyncio.AsyncIOMotorClient):
            def __getitem__(self, name):
                return DatabaseSubclass(self, name)

        cx = ClientSubclass(test.env.uri, **self.get_client_kwargs())
        self.assertIsInstance(cx, ClientSubclass)

        db = cx["testdb"]
        self.assertIsInstance(db, DatabaseSubclass)

        coll = db["testcoll"]
        self.assertIsInstance(coll, CollectionSubclass)
        self.assertIsNotNone(await coll.insert_one({}))


class ExecutorForkTest(AsyncIOTestCase):
    @unittest.skipUnless(hasattr(os, "fork"), "This test requires fork")
    @asyncio_test()
    async def test_executor_reset(self):
        parent_conn, child_conn = Pipe()
        lock_pid = os.fork()
        if lock_pid == 0:  # Child
            set_event_loop(None)
            self.loop = new_event_loop()
            client = self.asyncio_client()
            try:
                self.loop.run_until_complete(client.db.command("ping"))
            except Exception:
                child_conn.send(False)
            child_conn.send(True)
            os._exit(0)
        else:  # Parent
            self.assertTrue(parent_conn.recv(), "Child process did not complete.")
