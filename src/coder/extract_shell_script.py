import re

def extract_shell_script(response_text):
    match = re.search(r'```bash\n(.*?)\n```', response_text, re.DOTALL)

    if match:
        shell_script_content = match.group(1) # Extract the shell script content
        print(f'Shell script extracted successfully: {shell_script_content}')
        # Specify the path and name for the shell script file within your project directory
        shell_script_path = '/home/cosmos/Documents/coder-test/setup_project.sh'  # Update this path

        # Write the extracted shell script content to the specified file
        with open(shell_script_path, 'w') as file:
            file.write(shell_script_content)

        print(f"Shell script saved to: {shell_script_path}")
    else:
        print("Shell script not found in the response.")

if __name__ == "__main__":
    response = """
Here is a shell script to set up a new Python project named YellowCircleDrawer with the specified dependencies, programming language, project structure, and README.md content:

```bash
#!/bin/bash

# Create project directories
mkdir -p YellowCircleDrawer/src

# Create project files
touch YellowCircleDrawer/src/main.py
touch YellowCircleDrawer/README.md
touch YellowCircleDrawer/requirements.txt

# Add content to README.md
echo "# YellowCircleDrawer" >> YellowCircleDrawer/README.md
echo "## Purpose" >> YellowCircleDrawer/README.md
echo "A Python project to draw a yellow circle on the screen." >> YellowCircleDrawer/README.md

# Add project dependencies to requirements.txt
echo "pygame==2.0.1" >> YellowCircleDrawer/requirements.txt

# Implement main function in main.py
cat <<EOT >> YellowCircleDrawer/src/main.py
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    yellow = (255, 255, 0)
    pygame.draw.circle(screen, yellow, (400, 300), 50)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == "__main__":
    main()
EOT

echo "YellowCircleDrawer project setup complete."
```

You can run this shell script in your terminal to set up the YellowCircleDrawer project with the specified structure and content.
Here is a shell script that you can use to set up the YellowCircleDrawer project:

```bash
#!/bin/bash

# Create project directories
mkdir -p YellowCircleDrawer/src

# Create project files
touch YellowCircleDrawer/src/main.py
touch YellowCircleDrawer/README.md
touch YellowCircleDrawer/requirements.txt

# Add content to README.md
echo "# YellowCircleDrawer" >> YellowCircleDrawer/README.md
echo "## Purpose" >> YellowCircleDrawer/README.md
echo "A Python project to draw a yellow circle on the screen." >> YellowCircleDrawer/README.md

# Add project dependencies to requirements.txt
echo "pygame==2.0.1" >> YellowCircleDrawer/requirements.txt

# Implement main function in main.py
cat <<EOF >> YellowCircleDrawer/src/main.py
# User Prompt: Implement the main function to initialize pygame and draw a yellow circle.

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    yellow = (255, 255, 0)
    pygame.draw.circle(screen, yellow, (400, 300), 50)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == "__main__":
    main()
EOF

echo "YellowCircleDrawer project setup complete."
```

You can run this script in a terminal to create the project structure and files as specified. The script will also initialize the README.md with the project name and purpose, add the dependencies to requirements.txt, and implement the main function in main.py.
"""

    extract_shell_script(response_text=response)
