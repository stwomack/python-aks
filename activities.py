from temporalio import activity

@activity.defn
async def your_first_activity(name: str) -> str:
    return f"Hello, {name}!"

@activity.defn
async def your_second_activity(data: str) -> str:
    return f"Processing: {data}"

@activity.defn
async def your_third_activity(result: str) -> str:
    return f"Final result: {result}"