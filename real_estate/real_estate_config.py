import os
import json

real_estate_config_path = os.path.expanduser('~/local_projects/config/real_estate.json')


# Function to ensure all configuration data is loaded
def ensure_config():
    ensure_env_vars_loaded()


def ensure_env_vars_loaded():
    if os.getenv("RE_CONFIG_LOADED") != "true":
        # Load the JSON configuration from the file
        with open(real_estate_config_path, 'r') as file:
            json_data = file.read()
            set_env_vars_from_json(json_data)

def set_env_vars_from_json(json_content):
    """
    Parses a JSON string and sets environment variables, using a flag
    that is dynamically created from the prefix.
    """
    try:
        # Load the JSON data from the string
        data = json.loads(json_content)

        if 'environment' not in data or not isinstance(data['environment'], dict):
            print("Error: JSON data is missing the 'environment' key or it is not a dictionary.")
            return

        environment_data = data['environment']

        # This line fetches the prefix from the JSON data!
        prefix = environment_data.get('prefix', '').upper()
        # Dynamically create the config flag name from the prefix
        config_flag = f"{prefix}_CONFIG_LOADED"

        # Check if the configurations have already been loaded using the dynamic flag
        if os.getenv(config_flag) == "true":
            print(f"Configurations are already loaded. Exiting.")
            return
        
        print("Populating environment variables from JSON...")

        for top_key, inner_data in environment_data.items():
            # Skip the 'prefix' key as it's not a folder and the dynamically created config_flag
            if top_key == 'prefix' or not isinstance(inner_data, dict):
                continue
            
            parent_key_upper = top_key.upper()

            for child_key, value in inner_data.items():
                env_var_name_parts = []
                if prefix:
                    env_var_name_parts.append(prefix)
                env_var_name_parts.append(parent_key_upper)
                env_var_name_parts.append(child_key.upper())
                
                env_var_name = "_".join(env_var_name_parts)

                os.environ[env_var_name] = value
                print(f"Set environment variable: {env_var_name} = '{os.environ[env_var_name]}'")

        # Set the flag to indicate that configurations are loaded
        os.environ[config_flag] = "true"
        print(f"\nSuccessfully set all environment variables and the flag: {config_flag}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    ensure_config()

