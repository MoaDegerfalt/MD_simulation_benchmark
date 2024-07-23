import sys


# This script is used in "run_MD_simulation" to create "in.lammps_{index}" files for MD simulation. 
# Namn is the name of the specific run ex "sweep_2__" 
namn = sys.argv[1]
i = sys.argv[2]

with open(r'in.lammps', 'r') as f:
    lines = f.readlines()


for row in lines:
    name = "in.lammps_" + str(i)
    with open(name, 'a') as R:
        model = 'pair_coeff'
        dump = 'dump '
        if row.find(model) == -1 & row.find(dump) == -1:
            R.write(row)
        if row.find(model) != -1:
            R.write("pair_coeff              * * models/deployed_"+ namn + str(i) + ".pth Fe C")
        
        if row.find(dump) != -1:
            R.write("dump          1 all custom ${output} growth/growth_" + namn + str(i) + ".dump element x y z\n")
