import trio

from motor.motor_trio import TrioMotorClient


async def main():
    client = TrioMotorClient("mongodb://asshole:cockButt123!@lucy.obnoxious.lol:27017")

    db = client["scene"]
    collection = db["testing"]

    #await collection.insert_one({"test": "test"})
    count = await collection.count_documents({"test": "test"})

    print(count)

trio.run(main)
