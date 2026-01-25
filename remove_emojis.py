"""
Remove emojis from all markdown files
"""

import re
from pathlib import Path

def remove_emojis(text):
    """Remove emoji characters from text"""
    # Emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def process_file(file_path):
    """Remove emojis from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        cleaned_content = remove_emojis(content)
        
        # Only write if content changed
        if cleaned_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"✓ Cleaned: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Process all markdown files"""
    print("Removing emojis from documentation files...\n")
    
    # Find all markdown files
    md_files = list(Path('.').rglob('*.md'))
    
    cleaned_count = 0
    for md_file in md_files:
        if process_file(md_file):
            cleaned_count += 1
    
    print(f"\n✅ Processed {len(md_files)} files, cleaned {cleaned_count} files")

if __name__ == "__main__":
    main()
