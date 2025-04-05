import sys

def replace_non_digits():
    # Read all lines from standard input
    content = sys.stdin.read()
    
    # Create an output string with characters replaced
    replaced_content = ''
    for char in content:
        if char.isdigit():
            replaced_content += char
        elif char == '\n':
            replaced_content += char  # retain newline characters
        else:
            replaced_content += ' '  # replace non-digit with a space

    # Print the modified content
    print(replaced_content)

# Call the function to process standard input
replace_non_digits()