import os

base_dir = 'past_papers'
grades = ['grade12', 'grade13']
subjects = {
    'grade12': ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
    'grade13': ['Computer Science', 'Economics', 'Accounting', 'Advanced Mathematics']
}

# Create base directory
os.makedirs(base_dir, exist_ok=True)

# Create grade and subject directories
for grade in grades:
    grade_path = os.path.join(base_dir, grade)
    os.makedirs(grade_path, exist_ok=True)
    
    for subject in subjects[grade]:
        subject_path = os.path.join(grade_path, subject)
        os.makedirs(subject_path, exist_ok=True)
        
        # Create a dummy past paper file for demonstration
        dummy_paper_path = os.path.join(subject_path, f'{subject}_sample_paper.pdf')
        with open(dummy_paper_path, 'w') as f:
            f.write('This is a sample past paper for demonstration purposes.')

print("Directories and sample papers created successfully!")
