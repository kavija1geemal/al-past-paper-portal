from flask import Flask, send_file, jsonify, request, send_from_directory, redirect, url_for
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# Disable CORS for local development
CORS(app)

# Directory to store past papers
PAST_PAPERS_DIR = 'past_papers'

# Subjects configuration path
SUBJECTS_CONFIG_PATH = 'subjects_config.json'

# Ensure past papers directory exists
os.makedirs(PAST_PAPERS_DIR, exist_ok=True)

def load_subjects():
    """Load subjects from configuration file"""
    if not os.path.exists(SUBJECTS_CONFIG_PATH):
        # Default subjects if no config exists
        default_subjects = {
            'grade12': ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
            'grade13': ['Computer Science', 'Economics', 'Accounting', 'Advanced Mathematics']
        }
        with open(SUBJECTS_CONFIG_PATH, 'w') as f:
            json.dump(default_subjects, f, indent=4)
        return default_subjects
    
    with open(SUBJECTS_CONFIG_PATH, 'r') as f:
        return json.load(f)

@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_paper():
    """Upload a past paper"""
    subjects = load_subjects()
    
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Get form data
        grade = request.form.get('grade', '')
        subject = request.form.get('subject', '')
        year = request.form.get('year', str(datetime.now().year))
        
        # Validate inputs
        if not grade or not subject:
            return jsonify({'error': 'Grade and subject are required'}), 400
        
        # Validate subject exists
        if subject not in subjects.get(grade, []):
            return jsonify({'error': 'Invalid subject for selected grade'}), 400
        
        # Validate year (must be a 4-digit number)
        try:
            year = int(year)
            if year < 1900 or year > datetime.now().year:
                return jsonify({'error': 'Invalid year'}), 400
        except ValueError:
            return jsonify({'error': 'Year must be a valid number'}), 400
        
        # Create subject directory if it doesn't exist
        subject_dir = os.path.join(PAST_PAPERS_DIR, grade, subject, str(year))
        os.makedirs(subject_dir, exist_ok=True)
        
        # Generate unique filename
        filename = f"{subject}_{year}_{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = os.path.join(subject_dir, filename)
        
        # Save file
        file.save(file_path)
        
        return jsonify({
            'message': 'File uploaded successfully', 
            'filename': filename
        }), 200
    
    # GET request - serve upload page
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Past Paper</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            input, select { width: 100%; padding: 10px; margin: 10px 0; }
            input[type="submit"] { background: #3498db; color: white; border: none; cursor: pointer; }
        </style>
        <script>
            function updateSubjects() {
                const grade = document.getElementById('grade').value;
                const subjectSelect = document.getElementById('subject');
                subjectSelect.innerHTML = '';
                
                const subjects = ''' + json.dumps(subjects) + ''';
                
                subjects[grade].forEach(subject => {
                    const option = document.createElement('option');
                    option.value = subject;
                    option.textContent = subject;
                    subjectSelect.appendChild(option);
                });
            }
        </script>
    </head>
    <body>
        <h1>Upload Past Paper</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <select id="grade" name="grade" required onchange="updateSubjects()">
                <option value="">Select Grade</option>
                <option value="grade12">Grade 12</option>
                <option value="grade13">Grade 13</option>
            </select>
            
            <select id="subject" name="subject" required>
                <option value="">Select Subject</option>
            </select>
            
            <input type="number" name="year" id="year" min="1900" max="''' + str(datetime.now().year) + '''" 
                   value="''' + str(datetime.now().year) + '''" required placeholder="Enter Year">
            
            <input type="file" name="file" accept=".pdf" required>
            <input type="submit" value="Upload Paper">
        </form>
    </body>
    </html>
    '''

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Retrieve list of available subjects for Grade 12 and 13"""
    return jsonify(load_subjects())

@app.route('/api/papers', methods=['GET'])
def list_papers():
    """List available past papers"""
    grade = request.args.get('grade', 'grade12')
    subject = request.args.get('subject')
    year = request.args.get('year')
    
    # Validate subject exists
    subjects = load_subjects()
    if subject not in subjects.get(grade, []):
        return jsonify({'error': 'Invalid subject'}), 404
    
    # Determine papers path
    if year:
        papers_path = os.path.join(PAST_PAPERS_DIR, grade, subject, str(year))
    else:
        papers_path = os.path.join(PAST_PAPERS_DIR, grade, subject)
    
    if not os.path.exists(papers_path):
        return jsonify({'error': 'No papers found'}), 404
    
    # If no year specified, list all years
    if not year:
        years = [d for d in os.listdir(papers_path) if os.path.isdir(os.path.join(papers_path, d))]
        return jsonify(years)
    
    # List papers for specific year
    papers = os.listdir(papers_path)
    return jsonify(papers)

@app.route('/download', methods=['GET'])
def download_paper():
    """Download a specific past paper"""
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    year = request.args.get('year')
    filename = request.args.get('filename')
    
    file_path = os.path.join(PAST_PAPERS_DIR, grade, subject, str(year), filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
