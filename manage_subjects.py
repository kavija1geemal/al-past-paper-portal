import os
import json
import shutil
from datetime import datetime

# Path to store subjects configuration
SUBJECTS_CONFIG_PATH = 'subjects_config.json'
# Directory to store past papers
PAST_PAPERS_DIR = 'past_papers'

def load_subjects():
    """Load subjects from configuration file"""
    if not os.path.exists(SUBJECTS_CONFIG_PATH):
        # Default subjects if no config exists
        default_subjects = {
            'grade12': ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
            'grade13': ['Computer Science', 'Economics', 'Accounting', 'Advanced Mathematics']
        }
        save_subjects(default_subjects)
        return default_subjects
    
    with open(SUBJECTS_CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_subjects(subjects):
    """Save subjects to configuration file"""
    with open(SUBJECTS_CONFIG_PATH, 'w') as f:
        json.dump(subjects, f, indent=4)

def list_subjects():
    """List all available subjects"""
    subjects = load_subjects()
    print("\n🏫 Current Subjects:")
    for grade, subject_list in subjects.items():
        print(f"\n{grade.upper()}:")
        for subject in subject_list:
            print(f"  - {subject}")

def list_years():
    """List available years for past papers"""
    print("\n📅 Available Years:")
    for grade in ['grade12', 'grade13']:
        print(f"\n{grade.upper()}:")
        subjects = load_subjects().get(grade, [])
        
        for subject in subjects:
            subject_path = os.path.join(PAST_PAPERS_DIR, grade, subject)
            
            if os.path.exists(subject_path):
                years = [d for d in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, d))]
                
                if years:
                    print(f"  {subject}:")
                    for year in sorted(years):
                        paper_count = len(os.listdir(os.path.join(subject_path, year)))
                        print(f"    - {year} ({paper_count} papers)")
                else:
                    print(f"  {subject}: No papers")

def add_subject():
    """Add a new subject"""
    subjects = load_subjects()
    
    # Grade selection
    print("\n📚 Add New Subject")
    while True:
        grade = input("Enter grade (12/13): ")
        if grade in ['12', '13']:
            grade = f'grade{grade}'
            break
        print("Invalid grade. Please enter 12 or 13.")
    
    # Subject name input
    while True:
        subject = input("Enter new subject name: ").strip()
        if not subject:
            print("Subject name cannot be empty.")
            continue
        
        # Check if subject already exists
        if subject in subjects[grade]:
            print(f"❌ {subject} already exists in {grade}!")
            continue
        
        # Confirm addition
        confirm = input(f"Add {subject} to {grade}? (y/n): ").lower()
        if confirm == 'y':
            subjects[grade].append(subject)
            save_subjects(subjects)
            print(f"✅ {subject} added to {grade} successfully!")
            break
        else:
            print("Subject addition cancelled.")
            break

def remove_subject():
    """Remove an existing subject"""
    subjects = load_subjects()
    
    # Grade selection
    print("\n🗑️ Remove Subject")
    while True:
        grade = input("Enter grade (12/13): ")
        if grade in ['12', '13']:
            grade = f'grade{grade}'
            break
        print("Invalid grade. Please enter 12 or 13.")
    
    # Display subjects for the grade
    print(f"\nSubjects in {grade}:")
    for i, subject in enumerate(subjects[grade], 1):
        print(f"{i}. {subject}")
    
    # Subject selection
    while True:
        try:
            choice = int(input("\nEnter the number of the subject to remove: ")) - 1
            
            if 0 <= choice < len(subjects[grade]):
                subject = subjects[grade][choice]
                
                # Check if subject has any papers
                papers_dir = os.path.join(PAST_PAPERS_DIR, grade, subject)
                if os.path.exists(papers_dir) and os.listdir(papers_dir):
                    print(f"❌ Cannot remove {subject}. Papers exist in this subject.")
                    confirm = input("Do you want to delete ALL papers in this subject? (y/n): ").lower()
                    if confirm == 'y':
                        shutil.rmtree(papers_dir)
                        print(f"🗑️ Deleted all papers in {subject}")
                    else:
                        continue
                
                # Confirm removal
                confirm = input(f"Remove {subject} from {grade}? (y/n): ").lower()
                if confirm == 'y':
                    subjects[grade].remove(subject)
                    save_subjects(subjects)
                    print(f"✅ {subject} removed from {grade} successfully!")
                    break
                else:
                    print("Subject removal cancelled.")
                    break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def remove_year():
    """Remove papers for a specific year"""
    print("\n🗓️ Remove Papers by Year")
    
    # Grade selection
    while True:
        grade = input("Enter grade (12/13): ")
        if grade in ['12', '13']:
            grade = f'grade{grade}'
            break
        print("Invalid grade. Please enter 12 or 13.")
    
    # Subject selection
    subjects = load_subjects()
    print(f"\nSubjects in {grade}:")
    for i, subject in enumerate(subjects[grade], 1):
        print(f"{i}. {subject}")
    
    while True:
        try:
            subject_choice = int(input("\nSelect subject: ")) - 1
            
            if 0 <= subject_choice < len(subjects[grade]):
                subject = subjects[grade][subject_choice]
                
                # List available years
                subject_path = os.path.join(PAST_PAPERS_DIR, grade, subject)
                if not os.path.exists(subject_path):
                    print(f"No papers found for {subject}")
                    break
                
                years = [d for d in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, d))]
                
                if not years:
                    print(f"No years found for {subject}")
                    break
                
                print(f"\nAvailable years for {subject}:")
                for i, year in enumerate(sorted(years), 1):
                    paper_count = len(os.listdir(os.path.join(subject_path, year)))
                    print(f"{i}. {year} ({paper_count} papers)")
                
                # Year selection
                year_choice = int(input("\nSelect year to remove: ")) - 1
                
                if 0 <= year_choice < len(years):
                    year = years[year_choice]
                    
                    # Confirm deletion
                    confirm = input(f"Delete ALL papers for {subject} in {year}? (y/n): ").lower()
                    if confirm == 'y':
                        year_path = os.path.join(subject_path, year)
                        shutil.rmtree(year_path)
                        print(f"🗑️ Deleted all papers for {subject} in {year}")
                        break
                    else:
                        print("Year deletion cancelled.")
                        break
                else:
                    print("Invalid year selection.")
            else:
                print("Invalid subject selection.")
        except ValueError:
            print("Please enter a valid number.")

def main_menu():
    """Main menu for subject and paper management"""
    while True:
        print("\n📝 AL Past Paper Portal - Management")
        print("1. List Subjects")
        print("2. Add Subject")
        print("3. Remove Subject")
        print("4. List Years")
        print("5. Remove Year")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            list_subjects()
        elif choice == '2':
            add_subject()
        elif choice == '3':
            remove_subject()
        elif choice == '4':
            list_years()
        elif choice == '5':
            remove_year()
        elif choice == '6':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
