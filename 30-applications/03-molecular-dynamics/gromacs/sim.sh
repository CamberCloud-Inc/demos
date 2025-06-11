# Modified Tutorial – GPL v3.0

# This work is a derivative of the original https://github.com/gromacstutorials/gromacstutorials-inputs.git
# released under GNU GPL v3.0. Significant modifications—including syntax rewrites, code extraction,
# and reorganization—have been applied.

# You may copy, modify, and distribute this work under the terms of GPL v3.0. The complete source
# for all code, data, and scripts is provided. Original copyright and license notices are retained,
# and a full copy of GPL v3.0 accompanies this distribution.

# =======================

#be careful with hardcoded choice of parameters, e.g. "printf "0\n0\n"" 
#correct parameter id is gromacs version dependent!

mkdir -p output

#Convert PDB to GRO
printf "0\n0\n" | gmx_mpi trjconv -f 1cta.pdb -s 1cta.pdb -o output/1cta.gro -center -box 5 5 5
# Choose group "System" for centering and output

# Generate topology and force field files
printf "1\n" | gmx_mpi pdb2gmx -f output/1cta.gro -water spce -ignh -o output/unsolvated.gro -v
# Choose AMBER03 protein force field and AMBER94 nucleic

# Solvate the protein
gmx_mpi solvate -cs spc216.gro -cp output/unsolvated.gro -o output/solvated.gro -p topol.top

# Prepare energy minimization input (using your inputs/minimize.mdp)
gmx_mpi grompp -f inputs/minimize.mdp -c output/solvated.gro -p topol.top -o output/min.tpr -pp output/min -po output/min -maxwarn 1

# Run energy minimization on GPU
gmx_mpi mdrun -v -deffnm output/min -nb gpu

# Extract potential energy
printf "10\n" | gmx_mpi energy -f output/min.edr -o output/potential-energy-minimization.xvg
# Select "Potential"

# Add salt (neutralize and set 1 M concentration)
printf "14\n" | gmx_mpi genion -s output/min.tpr -p topol.top -o output/salted.gro -conc 1 -neutral
# Select group "SOL"

# Prepare second energy minimization input after adding ions
gmx_mpi grompp -f inputs/minimize.mdp -c output/salted.gro -p topol.top -o output/min-s.tpr -pp output/min-s -po output/min-s

# Run second energy minimization on GPU
gmx_mpi mdrun -v -deffnm output/min-s -nb gpu

# Extract potential energy for second minimization
printf "10\n" | gmx_mpi energy -f output/min-s.edr -o output/potential-energy-minimization-s.xvg
# Select "Potential"

# Prepare NVT simulation input
gmx_mpi grompp -f inputs/nvt.mdp -c output/min-s.gro -p topol.top -o output/nvt.tpr -pp output/nvt -po output/nvt

# Run NVT simulation on GPU
gmx_mpi mdrun -v -deffnm output/nvt -nb gpu

# Coords formatting
printf "0\n" | gmx_mpi trjconv -s output/min-s.tpr -f output/nvt.xtc \
  -pbc mol -ur compact \
  -o output/nvt_nopbc.xtc