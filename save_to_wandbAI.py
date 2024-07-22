import sys
import os
import re
import wandb

# This function extracts information about the MD simulation from a resulting slurm- file. 
# When performing MD simulations on Alvis the --array=1-10 method is used. This will result one file named "slurm-{slurm_number}_{index}.out" where inte index will be a number between 1-10 in this case.
def MD_slurm(slurm_number, index):
    input_file = f'slurm-{slurm_number}_{index}.out'  # Path to the input file
    config_path = os.path.join("lammps", input_file)
    print(f"Looking for file: {config_path}")  # Debug path issues

    try:
        with open(config_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {config_path} does not exist.")

    # Use regex to find the sequence after "deployed_" MAKE SURE! to name the deployed model file "deployed_{model_name}.pth" 
    name_match = re.search(r'deployed_(\w+)', content)
    try:
        if name_match:
            run_name = name_match.group(1)
        else:
            raise ValueError("Could not find the sequence after 'deployed_'")
    except ValueError as e:
        print(e)

    # Use regex to find the float number following "Performance:"
    speed_match = re.search(r'Performance: ([\d]+\.[\d]+)', content)
    try:
        if speed_match:
            performance = speed_match.group(1)
        else:
            raise ValueError("Could not find the name following 'Performance:'")
    except ValueError as e:
        print(e)

    return performance, run_name


# This function extracts information regarding the run_id needed to uppdate a specific run in wnadb.ai. 
# The information can be found in a file called "config.yaml" it is created when the model is first initiated for training and logged to wandb.ai. It is stored togeter with "best_model.pth", latest_model.pth" osv in a folder. 
# The name of the folder is the run name. 
def extract_runID(model, project):
    input_file = os.path.join("results", str(project), str(model))
    config_path = os.path.join(input_file, "config.yaml")
    try:
        with open(config_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {config_path} does not exist.")

    # Use regex to find the sequence after "run_id:"
    sequence_match = re.search(r'run_id:\s*(\w+)', content)
    try:
        if sequence_match:
            sequence = sequence_match.group(1)
        else:
            raise ValueError("Could not find the sequence after 'run_id:'")
    except ValueError as e:
        print(e)

    return sequence


# This function will update wandb.ai
def save_wandbAI(project, runID, speed, model):
    api = wandb.Api()
    name = f"e3_equivariant/{project}/{runID}"

    try:
        run = api.run(name)
        run.config["speed [ns/day]"] = float(speed)  # Convert speed to float
        run.update()
        print(f"Updated run: {model} with speed: {speed}")
    except Exception as e:
        print(f"Error updating run {model}: {e}")


if __name__ == '__main__':

    # Example how to run on Alvis using a container:
    # apptainer exec Allegro.sif python3 save_all.py NequIP_size_sweep 2539032 2000 3000
    project = sys.argv[1] # name of project in wandb.ai
    slurm_number = sys.argv[2] # Slurm number from MD simulation ex 2539032
    first = sys.argv[3] # The first in the loop ex if --array=1000-2000 first = 1000
    last = sys.argv[4]  # last is then 2000 to match the range to the slurm numbers. 

    for i in range(int(first), int(last)):
      try:  
        speed, model = MD_slurm(slurm_number, i)
        runID = extract_runID(model, project)
        save_wandbAI(project, runID, speed, model)
      except (ValueError, FileNotFoundError) as e:
            print(f"Error processing index {i}: {e}")
      except Exception as e:
            print(f"An unexpected error occurred at index {i}: {e}")
        
