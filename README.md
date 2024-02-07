# Motor

This is a fork of a really poorly made pymongo async wrapper.

# Why does it suck?

This sucks because of instead of taking the time to actually implement the MongoDB protocol async, they just imported PyMongo
and then put the functions into what is essentially a ThreadPoolExecutor and instead of taking the 5 seconds
to use anyio instead of asyncio they just use asyncio

# Why does this exist as a fork

They are lazy as fuck.