import os

def scan_directory_and_prepare_prompt(directory):
    """
    Scans the specified directory recursively for files, reading their entire content.
    Builds a comprehensive prompt for the AI assistant based on the folder structure,
    full file contents, and specifically marked user prompts.
    """
    ai_prompt_parts = ["Project structure and full content including user prompts:"]

    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)

        # Optionally add directory structure to the AI prompt for context
        if relative_root != ".":
            ai_prompt_parts.append(f"Directory: {relative_root}/")

        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Include full file content in the AI prompt
            ai_prompt_parts.append(f"File: {os.path.join(relative_root, file_name)}")
            ai_prompt_parts.append(file_content)
            ai_prompt_parts.append("End of File\n")  # Marker for the end of the file content

    return "\n".join(ai_prompt_parts) + """
Based on the above project structure and content, please:
- Implement the functions or features described in 'User prompt' comments within the code.
- Suggest any potential improvements or optimizations to the existing code.
- Identify areas where additional documentation or comments could be beneficial.
"""

if __name__ == "__main__":
    # Specify the root directory of your project
    project_root_directory = '/home/cosmos/Documents/coder-test/YellowCircleDrawer/'  # Update this path

    # Generate the comprehensive prompt for the AI
    ai_prompt = scan_directory_and_prepare_prompt(project_root_directory)

    print(ai_prompt)  # Or process the prompt as needed for your AI assistant interaction
