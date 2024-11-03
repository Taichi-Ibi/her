import re
import pyperclip

def copy_code_to_clipboard(text: str) -> None:
    """
    Finds all code blocks in the given text and copies them to the clipboard.
    
    Args:
        text (str): The input text containing code blocks.
    
    Returns:
        None
    """
    # Regular expression to match code blocks (```language ... ```)
    pattern = r'```[\w]*\n([\s\S]*?)\n```'
    
    # Find all code blocks
    code_blocks = re.findall(pattern, text)
    
    if code_blocks:
        # Join all code blocks with newlines between them
        all_code = '\n\n'.join(code_blocks)
        
        # Copy to clipboard
        pyperclip.copy(all_code)
        print("**All code blocks have been copied to the clipboard.**")
    else:
        print("**No code blocks found in the text.**")
