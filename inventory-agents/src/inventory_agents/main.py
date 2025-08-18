import asyncio
from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool, enable_verbose_stdout_logging
from pydantic import BaseModel

# Model set up
GEMINI_MODEL = "gemini/gemini-2.0-flash-exp"
GEMINI_API_KEY = "AIzaSyDsUcjDanHvDO6oeQTpfVrurFVPYMclMU4"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=GEMINI_BASE_URL
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

inventory = [
    {"id": 1, "name": "Laptop", "quantity": 10},
    {"id": 2, "name": "Mouse", "quantity": 50},
    {"id": 3, "name": "Keyboard", "quantity": 30}
]
@dataclass
class InventoryItemInput:
    operation: str
    id: int = None
    name: str = None
    quantity: int = None

class HelpfulAgentOutput(BaseModel):
    response_type: str #"inventory"
    inventory_data: str = None  # inventory responses

# inventory management 
@function_tool
async def manageInventory(item) -> str:
    """
    Manage inventory by adding, updating, or deleting items.
    Operations: 'add' (new item), 'update' (modify existing), 'delete' (remove item).
    For 'add', provide name and quantity. For 'update' or 'delete', provide id.
    """
    global inventory
    operation = (item.operation or "").lower()


    print("\n\n\n")
    print(f"Operation: {operation}, Item: {item}")
    if operation == "add":
        if not item.name or item.quantity is None:
            return "Error: Name and quantity are required for adding an item."
        new_id = max([item["id"] for item in inventory], default=0) + 1
        inventory.append({"id": new_id, "name": item.name, "quantity": item.quantity})
        return f"Added {item.name} with ID {new_id} and quantity {item.quantity}."

    elif operation == "update":
        if item.id is None or not item.name or item.quantity is None:
            return "Error: ID, name, and quantity are required for updating an item."
        for inv_item in inventory:
            if inv_item["id"] == item.id:
                inv_item["name"] = item.name
                inv_item["quantity"] = item.quantity
                return f"Updated item ID {item.id} to {item.name} with quantity {item.quantity}."
        return f"Error: Item with ID {item.id} not found."

    elif operation == "delete":
        if item.id is None:
            return "Error: ID is required for deleting an item."
        for i, inv_item in enumerate(inventory):
            if inv_item["id"] == item.id:
                deleted_item = inventory.pop(i)
                return f"Deleted item ID {item.id} ({deleted_item['name']})."
        return {"error": f"Unknown operation: {operation}"}

    else:
        return "Error: Invalid operation. Use 'add', 'update', or 'delete'."

# Define the agent 
agent = Agent(
    name="Helpful Assistant",
    instructions="You are a helpful Assistant capable of managing an inventory. For inventory tasks (add, update, delete),  YOU MUST use manageInventory tool and return the current inventory state.",
    model=model,
    tools=[manageInventory],
    output_type=HelpfulAgentOutput
)

async def main(kickOffMessage: str):
    print(f"RUN Initiated: {kickOffMessage}")
    
    result = await Runner.run(
        agent,
        input=kickOffMessage
    )
    # Print results 
    print(result.final_output)
    
    if result.final_output and result.final_output.response_type == "inventory":
        print("\nCurrent Inventory:")
        print(inventory)

def start():
    asyncio.run(main("Add a new item to the inventory: , quantity 25"))

if __name__ == "__main__":
    start()
