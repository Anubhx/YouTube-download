import sys
import os
from app import app as application  # Assuming your Flask app is named "app" and located in "app.py"

# Add your project directory to the PYTHONPATH
sys.path.insert(0, '/home/yourusername/yourprojectdirectory')

# Activate the virtual environment (if used)
# activate_this = '/home/yourusername/yourprojectdirectory/venv/bin/activate_this.py'
# exec(open(activate_this).read(), {'__name__': '__main__'})
