
mkdir -p output

printf "0\n0\n" | gmx_mpi trjconv -f 1cta.pdb -s 1cta.pdb -o output/1cta.gro -center -box 5 5 5
printf "1\n" | gmx_mpi pdb2gmx -f output/1cta.gro -water spce -ignh -o output/unsolvated.gro -v
gmx_mpi solvate -cs spc216.gro -cp output/unsolvated.gro -o output/solvated.gro -p topol.top
gmx_mpi grompp -f inputs/minimize.mdp -c output/solvated.gro -p topol.top -o output/min.tpr -pp output/min -po output/min -maxwarn 1
gmx_mpi mdrun -v -deffnm output/min -nb gpu
printf "10\n" | gmx_mpi energy -f output/min.edr -o output/potential-energy-minimization.xvg
printf "14\n" | gmx_mpi genion -s output/min.tpr -p topol.top -o output/salted.gro -conc 1 -neutral
gmx_mpi grompp -f inputs/minimize.mdp -c output/salted.gro -p topol.top -o output/min-s.tpr -pp output/min-s -po output/min-s
gmx_mpi mdrun -v -deffnm output/min-s -nb gpu
printf "10\n" | gmx_mpi energy -f output/min-s.edr -o output/potential-energy-minimization-s.xvg
gmx_mpi grompp -f inputs/nvt.mdp -c output/min-s.gro -p topol.top -o output/nvt.tpr -pp output/nvt -po output/nvt
gmx_mpi mdrun -v -deffnm output/nvt -nb gpu
gmx_mpi trjconv -s output/min-s.tpr -f output/nvt.xtc \
  -pbc mol -ur compact \
  -o output/nvt_nopbc.xtc