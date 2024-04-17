## Installation

Clone the repository:<br>
`git clone https://github.com/MuhammadaliAliyev/django_projects/` <br><br>
Create a virtual environment and activate it (recommended):<br>
`python -m venv venv  # Python 3`<br>
`source venv/bin/activate  # Linux/macOS`<br>
`venv\Scripts\activate.bat  # Windows`<br><br>
Install dependencies:<br>
`pip install -r requirements.txt`<br><br>
(Optional) Set environment variables:
Some settings might require environment variables like SECRET_KEY or database credentials. Refer to the settings.py file for details on how to set them up.

Run migrations:<br>
`python manage.py migrate`<br><br>
### Usage
Start the development server:<br>
`python manage.py runserver`<br>
This will typically run the server at http://127.0.0.1:8000/.
