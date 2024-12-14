# AL Past Paper Portal

## Project Overview
A web application for downloading Advanced Level (AL) past papers for Grade 12 and 13 students.

## Setup Instructions
1. Clone the repository
2. Install dependencies
3. Run the application

## Features
- Browse past papers by grade and subject
- Download past papers
- Search functionality

## Subject and Paper Management

### Managing Subjects

You can manage subjects using the `manage_subjects.py` script. This script allows you to:
- List existing subjects
- Add new subjects
- Remove existing subjects
- List available years for papers
- Remove papers by year

#### How to Add a Subject

1. Run the script:
```bash
python manage_subjects.py
```

2. Choose option `2` to add a subject

3. Select the grade:
   - Enter `12` for Grade 12
   - Enter `13` for Grade 13

4. Enter the name of the new subject (e.g., "Computer Science")

5. Confirm by typing `y`

#### Example of Adding a Subject
```
📝 AL Past Paper Portal - Management
1. List Subjects
2. Add Subject
3. Remove Subject
4. List Years
5. Remove Year
6. Exit

Enter your choice (1-6): 2

📚 Add New Subject
Enter grade (12/13): 12
Enter new subject name: Computer Science
Add Computer Science to grade12? (y/n): y
✅ Computer Science added to grade12 successfully!
```

#### How to Remove a Subject

1. Run the script:
```bash
python manage_subjects.py
```

2. Choose option `3` to remove a subject

3. Select the grade:
   - Enter `12` for Grade 12
   - Enter `13` for Grade 13

4. Choose the subject number from the list

5. Confirm by typing `y`

#### Example of Removing a Subject
```
🗑️ Remove Subject
Enter grade (12/13): 12

Subjects in grade12:
1. Mathematics
2. Physics
3. Chemistry
4. Biology
5. Computer Science

Enter the number of the subject to remove: 5
Remove Computer Science from grade12? (y/n): y
✅ Computer Science removed from grade12 successfully!
```

### Additional Features

- Option `1`: List all current subjects
- Option `4`: List available years for papers
- Option `5`: Remove papers for a specific year and subject

## Important Notes
- You cannot remove a subject if it has existing papers
- If you want to remove a subject with papers, first delete all papers for that subject

## Technology Stack
- Frontend: React.js
- Backend: Python Flask
- Database: SQLite
