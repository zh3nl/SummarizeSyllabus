# **Syllabus Scanner**
- Team Members: Zhen Liu, Lucas Chin, Kabilan Vaikunthan, Sophia Ray



This project, designed for SBHacks, aims to help students plan out their courses. By uploading a PDF of their syllabus, they can get a comprehensive summary, add key dates to Google Calendar, and review any necessary prerequisites. 

## Deployment Instructions
To install dependencies:
```
pip install -r requirements.txt
```
```
cd summarizesyllabus
npm install
```
Run App and API Server
```
npm start
```
```
cd backend
python app.py
```
The app should be at `localhost:3000`
## Project Inspiration
Four years, ten classes a year: forty syllabi to memorize, schedule, and plan around. Wish there was a way to automate your class calendar? We, as students, understand the pain of trying to remember which quiz you have coming up next week, or where you class is on week one and wanted to design a solution. Syllabus Scanner allows students to upload a class syllabus to then quickly and neatly return all you will need to ace your class. Summaries, prerequisites, office hours, and class schedule. Also included is our flagship feature, the ability to add your midterms, exams, and class periods to your google calendar instantly. By authorizing your gmail you will have your class period, location, start and end date, and summary instantly added to your google calendar. 
## Tech Stack
* Frontend: React, Tailwind CSS, JavaScript
* Backend: Flask/Python
* API: Aryn DocParse and Claude

## Key Functionalities

### Document Scanning and Parsing
* Used Aryn DocParse to chunk and extract syllabus content from complex text documents
* Allow users to upload files to the web app to be analyzed by Claude
* Supports several file types, including PDF, DOC, DOCX, and TXT files

### Syllabus Summarization using Claude
* The Claude 3.5 Sonnet LLM is used to provide a detailed overview of uploaded class syllabus
* Utilized an instruction-based approach, combined with additional fine-tuning, to isolate core components and relevant information
* Responses generated by Claude are then formatted for convenient user viewing

### Calendar Assistant
* Uses GoogleOAUTH Credentials to access user accounts
* Formatted data pulled from syllabus documents are converted into event JSON formats
* Important events such as exam dates and class schedules are then conveniently pushed onto user calendars


