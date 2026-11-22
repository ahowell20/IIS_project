# IIS_project
**Project Status:** 
I have developed a simulated email assistant with some use of API (if key provided) allowing for greated implementation. This is a simulated environment where you click to receive a new email, but actions such as drafting responses are implemented with API calls or simulation only.

Implemented / Simulated:
- email labelling/categorisation
- response drafting
- auto-filing
- proposing meetings (based on simulated calendar)
- to-do list task creation
- Flagging
- Manually dragging emails into folders
- Creating new folders

Planned / unfinished:
- detecting and reporting spam
- proposed meeting feedback loop - allowing for user to manually set time or AI to suggest another time that fits in the calendar
- UI/UX fully updating when clicking onto a new tab (e.g moving from to-do lists back to inbox, the to-do list stays on the right hand side of the screen until the usr clicks onto an email)
- Slight time delay between clicking and receiving an email


**Technology Stack:**
Uses Python and html to run the simualtion and potential API calls locally.
Uses LLM model gemini-3.8-flash to get responses if API key supplied. This would ideally be a better model that is not affected by traffic volume.
In real world, this would be a plugin for email clients such as Outlook of Gmail.


**Running or inspecting the work:**
If you have an API key, create a .env file and add it in there: 

GEMINI_API_KEY=(your API key here)

Set up a virtual environment for it to run on:

pip install python-dotenv
python -m venv venv
.\venv\Scripts\activate.bat

Then in your terminal, run the app and open localhost:
python app.py

To start the simulation, click on 'Simulate Incoming Email'. If an API connection has been established, a green dot will show in the top right, else it will be orange for complete simulation.


**Development record:**
Added inital AI generated code for index.html based off of my design choices(Commit: 5af61a3) and a backend (app.py) to allow for API calls as I learnt I could get a free API key from Google AI (Commit: a0da351)
These had the basic funcationality but lacked feedback loops and some features (e.g spam reporting). This was then tested for functionality and appearance. Updates were made and committed as the first draft. 
A feedback loop was then added for drafting, although not for proposed meetings as the functionality here is very similar. This was tested and works well with an API although in the simulation, user prompts cannot be adhered to - instead there are 2 suggested prompts which show the functionality. (Commit: 176f2f8)


**AI assistance:**
Gemini used to vibe code the simulation. This was proof-read and then run to test. I made tweaks based on the UI/UX and functionality to ensure it works as expected. 
This included changing how meeting and the to-do list were shown - originally it kept the same layout as the inbox but this felt like a waste of screen space and made it hard to read. 
AI was also used to generate the storyboards after being given the frame by frame notes in the prompt. AI was used purely for visuals.
AI was not used to generate the systems diagram. This was done manually in LucidChart.


**Additional Files:**
In the repo under the 'Additional_Files' folder is a pdf of the systems diagram as it cannot be clearly see in the image in my report. 
