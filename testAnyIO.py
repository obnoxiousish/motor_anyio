import anyio

from motorAnyio.motor_anyio import AnyIOMotorClient


async def main():
    client = AnyIOMotorClient()

    db = client["anyio"]
    collection = db["testing"]

    await collection.insert_one({"test": "test"})
    count = await collection.count_documents({"test": "test"})

    await collection.update_one({"test": "test"}, {"$set": {"test": "testEdit"}})
    count2 = await collection.count_documents({"test": "testEdit"})

    print(count, count2)


anyio.run(main)
