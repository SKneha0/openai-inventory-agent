# 📦 Inventory Management System 
***OpenAI Agents SDK***.

 

- An AI-powered **Inventory Management CLI Tool** built with Python and the **OpenAI Agents SDK**.

- This project allows you to **list, add, update, and delete inventory items** interactively.  
- All inventory data is stored in a local `inventory.json` file.


## 🚀 Features
- Interactive CLI for managing inventory
- Persistent storage with JSON
- Supports:
  - 📋 List items
  - ➕ Add items
  - ✏️ Update items
  - ❌ Delete items
- AI-powered command interpretation
- Modular design with `model.py` and `main.py`


## 📂 Project Structure
```inventory-agents/
│── pyproject.toml # Project configuration
│── README.md # Documentation
│── src/
│ └── inventory_agents/
│ ├── init.py
│ ├── main.py # CLI entrypoint
│ ├── model.py # Model + API setup
│ └── inventory.json # Data store
```

---

## ⚙️ Installation

1. Clone the repository:
   ```Link```
   git clone https://github.com/your-username/inventory-agents.git
   cd inventory-agents
Install dependencies with uv:
```
uv sync
```
# ▶️ Usage
Run the interactive inventory agent:

```
uv run start-inventory
```
## Example workflow:
Your action (list, add, update, delete, exit): list
→ Inventory is empty.

Your action (list, add, update, delete, exit): add
→ Added Mouse (qty: 10) with ID 1.

Your action (list, add, update, delete, exit): update
→ Updated Mouse (ID: 1) to qty 20.

Your action (list, add, update, delete, exit): delete
→ Deleted Mouse (ID: 1).
# 🛠️ Configuration
API keys and model details are stored in the ```.env file:```

```
GEMINI_MODEL=gemini-2.5-flash
```
```
GEMINI_API_KEY=your_api_key
```
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

👩‍💻 Author
Neha Shahzad
📧 shahzadnaha@gmail.com

📜 License
This project is licensed under the MIT License.


