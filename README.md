# Spark_Math

Spark_Math is a web-based math quiz application designed for children. It features interactive math problems, voice input for answers, and a dashboard to track progress and statistics.

## Features
- Math problem generation by difficulty level (Easy, Medium, Hard)
- Voice recognition for answer input
- Real-time feedback and encouragement
- Dashboard with stats: solved problems, streak, accuracy
- Beautiful, kid-friendly UI

## Technologies Used
- Python (FastAPI backend)
- HTML, CSS, JavaScript (frontend)
- SQLAlchemy (database models)
- SpeechRecognition API (browser-based voice input)

## Getting Started
1. Clone the repository:
	```sh
	git clone <repo-url>
	```
2. Install dependencies:
	```sh
	pip install -r requirements.txt
	```
3. Run the application:
	```sh
	uvicorn main:app --reload
	```
4. Open your browser and go to `http://localhost:8000`

## File Structure
- `main.py` - FastAPI entry point
- `app/` - Application code
  - `models.py` - SQLAlchemy models for children and activities
  - `crud.py` - Database operations
  - `database.py` - DB connection setup
  - `routers/` - API and page routes
  - `services/` - AI and utility services
  - `static/` - Static files (images, CSS)
  - `templates/` - HTML templates
- `requirements.txt` - Python dependencies
- `database.db` - SQLite database

## Usage
- Select a difficulty level and start solving math problems.
- Use the microphone button to answer by voice.
- View your progress and stats on the dashboard.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License