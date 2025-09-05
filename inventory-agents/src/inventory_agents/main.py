import asyncio
import json
import os
from inventory_agents.model import model
from agents import Agent, Runner, function_tool, set_tracing_disabled



# Disable tracing to reduce noise
# set_tracing_disabled(True)

# ---------------- INVENTORY FILE ----------------
FILE = "inventory.json"


def save_inventory():
    with open(FILE, "w") as f:
        json.dump(inventory, f, indent=2)


if os.path.exists(FILE):
    try:
        with open(FILE, "r") as f:
            inventory = json.load(f)
    except json.JSONDecodeError:
        inventory = []   # blank rakho
        save_inventory()
else:
    # Nayi file banegi blank inventory ke sath
    inventory = []
    save_inventory()


# ---------------- TOOLS ----------------

@function_tool
async def listInventory() -> str:
    """List all inventory items"""
    if not inventory:
        return "Inventory is empty."
    return "\n".join(f"ID {i['id']}: {i['name']} (qty: {i['quantity']})" for i in inventory)


@function_tool
async def addItem(name: str, quantity: int) -> str:
    """Add a new item to inventory"""
    new_id = max((i["id"] for i in inventory), default=0) + 1
    inventory.append({"id": new_id, "name": name, "quantity": quantity})
    save_inventory()
    return f"Added {name} with quantity {quantity} (ID: {new_id})"


@function_tool
async def updateItem(item_id: int, quantity: int) -> str:
    """Update quantity of an existing item"""
    for i in inventory:
        if i["id"] == item_id:
            i["quantity"] = quantity
            save_inventory()
            return f"Updated {i['name']} (ID: {item_id}) to qty {quantity}"
    return f"Item with ID {item_id} not found."


@function_tool
async def deleteItem(item_id: int) -> str:
    """Delete item from inventory"""
    global inventory
    for i in inventory:
        if i["id"] == item_id:
            inventory = [x for x in inventory if x["id"] != item_id]
            save_inventory()
            return f"Deleted {i['name']} (ID: {item_id})"
    return f"Item with ID {item_id} not found."


# ---------------- AGENT ----------------
agent = Agent(
    name="Inventory Agent",
    instructions="You can list, add, update, and delete inventory items using the provided tools.",
    model=model,
    tools=[listInventory, addItem, updateItem, deleteItem]
)

# ---------------- MAIN (Interactive Mode) ----------------
async def chat():
    print("=== Inventory Management System Started ===\n")
    while True:
        # user_input = input("Enter command (list, add, update, delete, exit): ")
        if user_input.lower() in ["exit", "quit"]:
            print("Session ended. Goodbye!")
            break

        result = await Runner.run(agent, input=user_input)
        print("Response:", result.final_output, "\n")


if __name__ == "__main__":
    asyncio.run(chat())

def start():
    asyncio.run(chat())
