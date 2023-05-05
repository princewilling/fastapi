# Up to now, you have been using common data types, like:

#     int
#     float
#     str
#     bool

# But you can also use more complex data types.

# And you will still have the same features as seen up to now:

#     Great editor support.
#     Data conversion from incoming requests.
#     Data conversion for response data.
#     Data validation.
#     Automatic annotation and documentation.

# Other data types¶

# Here are some of the additional data types you can use:

#     UUID:
#         A standard "Universally Unique Identifier", common as an ID in many databases and systems.
#         In requests and responses will be represented as a str.

# frozenset:

#     In requests and responses, treated the same as a set:
#         In requests, a list will be read, eliminating duplicates and converting it to a set.
#         In responses, the set will be converted to a list.
#         The generated schema will specify that the set values are unique (using JSON Schema's uniqueItems).

# bytes:

#     Standard Python bytes.
#     In requests and responses will be treated as str.
#     The generated schema will specify that it's a str with binary "format".


from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    repeat_at: Annotated[time | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,        
    }
    
# Note that the parameters inside the function have their natural data type, and you can, for 
# example, perform normal date manipulations,