import yaml
from advanced_logging_setup import logger
import traceback

def compose_first_prompt(yaml_file_path) -> str:
    # Read and parse the YAML file
    try:
        with open(yaml_file_path, 'r') as file:
            project_description_yaml_content = yaml.safe_load(file)
    except Exception as e:
        logger.error(traceback.format_exc())

    logger.debug(f'project_description_yaml_content: {project_description_yaml_content}')

    # Convert the parsed YAML back to a string format for inclusion in the prompt
    project_description_yaml_str = yaml.dump(project_description_yaml_content)
    logger.debug(f'project_description_yaml_str: {project_description_yaml_str}')

    # Compose the full prompt using f-string and multiple lines for clarity
    full_prompt = (f"Generate a shell script to set up a new Python project based on the following description:\n"
                f"{project_description_yaml_str}"
                f"\nInclude commands to create the specified directories, files, "
                f"and a basic README.md content that includes the project name and purpose.")

    logger.debug(f'full_prompt: {full_prompt}')
    return full_prompt

if __name__ == "__main__":
    prompt = compose_first_prompt('/home/cosmos/Documents/coder-test/project_description.yaml')
    print(prompt)
