import trio

from motor.motor_trio import AnyIOMotorClient


async def main():
    client = AnyIOMotorClient()

    db = client["scene"]
    collection = db["testing"]

    await collection.insert_one({"test": "test"})
    count = await collection.count_documents({"test": "test"})

    print(count)

trio.run(main)
