import os
import shutil

def upload_paper():
    # Ensure past_papers directory exists
    base_dir = 'past_papers'
    os.makedirs(base_dir, exist_ok=True)

    # Get paper details from user
    print("AL Past Paper Upload Utility")
    print("---------------------------")
    
    # Grade selection
    while True:
        grade = input("Enter grade (12/13): ")
        if grade in ['12', '13']:
            grade = f'grade{grade}'
            break
        print("Invalid grade. Please enter 12 or 13.")

    # Subject selection
    subjects = {
        'grade12': ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
        'grade13': ['Computer Science', 'Economics', 'Accounting', 'Advanced Mathematics']
    }
    
    print(f"\nAvailable subjects for {grade}:")
    for i, subject in enumerate(subjects[grade], 1):
        print(f"{i}. {subject}")
    
    while True:
        try:
            subject_index = int(input("\nSelect subject number: ")) - 1
            subject = subjects[grade][subject_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

    # File upload
    while True:
        file_path = input("\nEnter the full path to the paper file: ")
        if os.path.exists(file_path):
            break
        print("File not found. Please check the path and try again.")

    # Create subject directory if it doesn't exist
    subject_dir = os.path.join(base_dir, grade, subject)
    os.makedirs(subject_dir, exist_ok=True)

    # Copy file to destination
    file_name = os.path.basename(file_path)
    destination = os.path.join(subject_dir, file_name)
    
    try:
        shutil.copy2(file_path, destination)
        print(f"\n✅ Paper successfully uploaded to: {destination}")
    except Exception as e:
        print(f"❌ Error uploading paper: {e}")

if __name__ == '__main__':
    upload_paper()
