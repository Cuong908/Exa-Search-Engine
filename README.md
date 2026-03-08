# Exa-Search-Engine

This project is a web-based search engine powered by Exa API, built with FastAPI, Python, and JavaScript

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-teal?logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/JavaScript-yellow?logo=javascript" alt="JavaScript" />
    <a href="https://github.com/Cuong908/Exa-Search-Engine/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-red" alt="MIT License" /></a>
</p>

## Demo
<!-- ![Web Demo](demo.gif) -->

## How it Works
The frontend takes the user query and sends it to a FastAPI backend, which calls the Exa Search API and returns the 5 most relevant results, containing title, dates, and source links. These requests are then rendered and displayed on the page for users to view and use. Users can also input queries via voice using the built-in speech recognition feature

## Installing

### 1. Clone the repository

```
git clone https://github.com/Cuong908/Exa-Search-Engine.git
cd Exa-Search-Engine
```

### 2. Get API key

Go to https://dashboard.exa.ai/login and create an account to access your Exa API key. Initialize Exa using your Exa API key, shown by Option A or Option B

#### Option A
1. Create an `.env` file
2. Store your API key inside the `.env` file (for example: EXA_API_KEY="your_key")
3. Add your `.env` file into `.gitignore` (Optional - if you're planning to push your code to GitHub)
4. Load it in `main.py` with the python-dotenv library (shown in main.py)

#### Option B
Replace `"EXA_API_KEY"` in `main.py` with your key

Note: this hardcodes the Exa API key so when published, for example to GitHub, your key will be visible to others which is bad and should be avoided. Thus, it's recommended to go with option A if you're planning to share your code

### 3. Install dependencies

This installs exa_py, FastAPI, uvicorn, and python-dotenv
```
pip install -r requirements.txt
```

### 4. Run the program

```
python -m uvicorn main:app --reload
```

## Website Features
<table>
<tr>
<td>
<h3>Dark Mode</h3>
Turns the website from light to dark
</td>
<td>
<h3>Speech to Text</h3>
Use the mic to search up any query
</td>
<td>
<h3>Speech Commands</h3>
Use the mic to run different commands
</td>
</tr>
</table>

## Speech Commands

- **Refresh** - Refresh the page
- **Dark Mode** - Turn on dark Mode
- **Light Mode** - Turn on light mode
- **Clear History** - Clears the current search history
- **Search for (input query)** - Search your query by speech
    Note: You can also say your query alone and it'll help you search it up

### Note
- To ensure the program properly hears you, please speak in a moderate pace and volume.
- For best results, use in a quiet environment

## Browser Compatibility

Speech recognition requires a browser with Web Speech API support:

- Chrome (recommended)
- Edge
- Firefox (limited support)

## Technical Stacks

- **Exa API** - Retrieve the query results and returns it
- **FastAPI** - Web framework for handling API requests
- **Python** - Backend logic
- **JavaScript** - Controls behavior based on user's action (allows different features)
- **HTML/CSS** - Frontend structure and styling

## Troubleshooting

**API returning no results?**
- Double-check your API key is correctly set in `.env` or `main.py`

**Port already in use?**
- Run `python -m uvicorn main:app --reload --port 8001` to use a different port

**Speech recognition not working?**
- Make sure your browser has microphone permissions enabled
- Check Browser Compatibility section for supported browsers
- Try refreshing the page

## Performance Notes

- **Results load in ~1-2 seconds** - First search may take slightly longer but afterwards, searches load faster due to caching. Speed varies by internet connection.
- **Speech recognition** - Responds in real time

## File Structure

```
ExaSearchEngine/
├── main.py
├── templates/
│   ├── home.html
│   └── results.html
├── static/
│   ├── background.jpeg
│   ├── background_dark.jpeg
│   ├── infoBG.jpeg
│   ├── mic.png
│   ├── mic_dark.png
│   ├── speaking.png
│   └── speaking_dark.png
└── README.md
```

## Resources

- [Exa's API Documentation](https://exa.ai/docs/reference/getting-started)
- [Exa's Python Cheat Sheet](https://exa.ai/docs/sdks/cheat-sheet#python)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Light Mode Background and Dark Mode Background](https://www.canva.com/design/DAHAHT23Q-Y/9mdgpDibt6rswaE91IggTQ/view?utm_content=DAHAHT23Q-Y&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h02c07e89f9)

## Credits

- Built a starter Exa Search Engine by [Build a Custom Search Engine with Exa](https://www.codedex.io/projects/build-a-custom-search-engine-with-exa-ai)
- Background images created by Cuong Tran

## License

MIT License - Feel free to use this code for entertainment, learning, and teaching!