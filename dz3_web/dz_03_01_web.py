import os
import sys
import shutil
import re
import threading

def normalize(name):
    normalized_name = re.sub(r'\W+', '', name)
    normalized_name = normalized_name.replace(' ', '_')
    return normalized_name

KNOWN_EXTENSIONS = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1][1:].upper()
            normalized_file_name = normalize(file)
            
            destination = None
            for category, extensions in KNOWN_EXTENSIONS.items():
                if file_extension in extensions:
                    destination = os.path.join(folder_path, category)
                    break
            
            if destination is None:
                # Unknown extension, leave the file unchanged
                continue
            
            os.makedirs(destination, exist_ok=True)
            destination_file = os.path.join(destination, normalized_file_name + '.' + file_extension)
            shutil.move(file_path, destination_file)
            
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir in KNOWN_EXTENSIONS or dir == 'archives':
                # Ignore folders with known categories or the archives folder
                continue
            else:
                # Recursively process nested folders
                process_folder(dir_path)
                if not os.listdir(dir_path):
                    # If the folder is empty after processing, remove it
                    os.rmdir(dir_path)

def main():
    if len(sys.argv) < 2:
        print('Usage: python sort.py <folder_path>')
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f'Error: Folder "{folder_path}" does not exist.')
        sys.exit(1)

    # Create a list to store threads
    threads = []

    # Process each subfolder in a separate thread
    for root, dirs, _ in os.walk(folder_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            thread = threading.Thread(target=process_folder, args=(dir_path,))
            threads.append(thread)
            thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Print the list of files in each category
    for category, extensions in KNOWN_EXTENSIONS.items():
        category_path = os.path.join(folder_path, category)
        files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
        print(f'Files in {category}:')
        for file in files:
            print(file)

    # Print the known and unknown extensions
    known_extensions = set(extension for extensions in KNOWN_EXTENSIONS.values() for extension in extensions)
    unknown_extensions = set()

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1][1:].upper()
            if file_extension not in known_extensions:
                unknown_extensions.add(file_extension)

    print('Known extensions:')
    print(known_extensions)

    print('Unknown extensions:')
    print(unknown_extensions)

if __name__ == '__main__':
    main()
