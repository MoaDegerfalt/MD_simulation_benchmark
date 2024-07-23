# MD_simulation_benchmark
This is how to deploy models, perform MD simulations, save the performence of the simulation to the model in wandb.ai. 

The file "run_deploy" is a bash script that will deploy the model so it can be used for MD simulations. 

The file "run_MD_simulation" is then used to perform MD simulation and it will use in.lammps as a template and create_in_lammps.py to build one in.lammps file for each simulation.

Now "save_to_wandbAI.py" can be run and it will 
  1. Find the model name and performance from the slurmfile created by "run_MD_simulation".
  2. Find the run ID code neded to save tha project in wandb.ai from the project folder.
  3. Save the information from "Performance" as speed in wandb.ai so it can be compared and evaluated with other variables. 




```
sbatch --array=1-100 run_deploy
```

```
cd lammps
```

```
sbatch --array=1-100 run_MD_simulation
```

copy the slurm code given for this batch. 

```
cd ..
```

```
apptainer exec {container.sif} python3 save_to_wandbAI.py {slurm code} 1 100
```
