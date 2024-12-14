import sys
import os

# Add the directory containing your app to the Python path
path = '/home/yourusername/al-past-paper-portal'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application
