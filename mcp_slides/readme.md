

# 📽️ Google Slides MCP Server

This MCP (Model Context Protocol) server enables AI agents to interact with Google Slides through a token-based authentication system using Google APIs. It supports dynamic slide creation, editing, and sharing operations.

---

## 🚀 Features / Tools Supported

| Tool Name                 | Description |
|--------------------------|-------------|
| `create_presentation`    | Create a new presentation |
| `get_presentation_metadata` | Get metadata including title, slide count, and timestamps |
| `add_blank_slide`        | Add a blank slide to a presentation |
| `insert_text`            | Insert styled text into a slide |
| `insert_image`           | Add an image to a slide |
| `list_slides`            | List all slides and their IDs |
| `move_slide`             | Move a slide to a different position |
| `replace_all_text`       | Find and replace text in the presentation |
| `delete_text_range`      | Delete part of the text in a text box |
| `share_presentation`     | Share the presentation with other users |

---

## ⚙️ Setup Instructions

### 1. 📁 Clone the Repository

```bash
git clone https://github.com/Sidhartht1607/mcp-servers-repo.git
cd mcp-servers-repo/slides_mcp


⸻

2. 🧪 Install Dependencies

pip install -r requirements.txt

If you’re using a virtual environment:

python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt


⸻

3. 🔐 How to Set Up Credentials

A. Required Scopes

These scopes are required:

ALL_SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive"
]

B. Create OAuth Credentials (client ID and secret)
	1.	Go to the Google Cloud Console
	2.	Create a project (or use an existing one)
	3.	Enable APIs:
	•	Google Slides API
	•	Google Drive API
	4.	Create OAuth 2.0 Client ID:
	•	Choose “Desktop App”
	•	Download the credentials.json file
	5.	Place credentials.json inside the slides_mcp/ folder

⸻

4. 🔁 First-Time Authentication

On the first run, the script will:
	•	Launch a browser for Google OAuth login
	•	Store the tokens in tokens.csv (includes access_token, refresh_token, etc.)
	•	These tokens will be reused automatically

⸻

5. ⚡ Run the MCP Server

mcp dev serverv2.py

This will:
	•	Start the server at http://localhost:8000/sse
	•	Launch MCP Inspector at http://localhost:6274

You can now use any of the defined tools.

⸻

📄 Example Tool Usage

Get presentation metadata:

{
  "presentation_name": "Team Update"
}

Insert text:

{
  "text": "**Quarterly Report**\\nRevenue increased by 20%",
  "slide_index": 0,
  "font_size": 24,
  "align": "center",
  "bullet": true,
  "presentation_name": "Team Update"
}


⸻

🛡️ Security Notes
	•	Do NOT commit tokens.csv, .env, or credentials.json to GitHub.
	•	Add them to your .gitignore.

⸻

📦 requirements.txt

google-api-python-client
google-auth
google-auth-oauthlib
python-dotenv
mcp


⸻

🧠 MCP Integration

This server is compatible with MCP agents and mcp-client. Each function is exposed via @mcp.tool() and can be called by AI agents or LLMs through a compatible inspector or autonomous system.

⸻

📬 Contact

Maintainer: Your Name or GitHub
Feel free to open issues or contribute tools!

Let me know if you want a `.gitignore` template or want to generate this file programmatically as well.