"""Command-line interface (CLI) entry point."""

# Print first to welcome the user while it waits to load the modules
print("\n.---------------------------.")
print("| WELCOME TO THE PYQMMM CLI |")
print(".---------------------------.")
print("Default programmed actions for the pyQMMM package.")
print("GitHub: https://github.com/davidkastner/pyqmmm")
print("Documenation: https://pyqmmm.readthedocs.io\n")
print("""
    The overall command-line interface (CLI) entry point.
    The CLI interacts with the rest of the package.
    The CLI is advantagous as it summarizes the scope of the package,
    and improves long-term maintainability and readability.\n
    """)

import os
import click

@click.command()
@click.option("--gbsa_submit", "-gs", is_flag=True, help="Prepares and submits a mmGBSA job.")
@click.option("--gbsa_analysis", "-ga", is_flag=True, help="Extract results from GBSA analysis.")
@click.option("--compute_hbond", "-hc", is_flag=True, help="Calculates hbonds with cpptraj.")
@click.option("--hbond_analysis", "-ha", is_flag=True, help="Extract Hbonding patterns from MD.")
@click.option("--last_frame", "-lf", is_flag=True, help="Get last frame from an AMBER trajectory.")
@click.option("--residue_list", "-lr", is_flag=True, help="Get a list of all residues in a PDB.")
@click.option("--colored_rmsd", "-cr", is_flag=True, help="Color RMSD by clusters.")
@click.option("--restraint_plot", "-rp", is_flag=True, help="Restraint plot KDE's on one plot.")
@click.option("--strip_all", "-sa", is_flag=True, help="Strip waters and metals.")
@click.option("--dssp_plot", "-dp", is_flag=True, help="Generate a DSSP plot.")
@click.help_option('--help', '-h', is_flag=True, help='Exiting pyQMMM.')
def md(
    gbsa_submit,
    gbsa_analysis,
    compute_hbond,
    hbond_analysis,
    last_frame,
    residue_list,
    colored_rmsd,
    restraint_plot,
    strip_all,
    dssp_plot,
    ):
    """
    Functions for molecular dynamics (MD) simulations.

    """
    if gbsa_submit:
        click.echo("> Submit a mmGBSA job:")
        click.echo("> Loading...")
        import pyqmmm.md.amber_toolkit
        protein_id = input("What is the id of your protein (e.g., taud, mc6)? ")
        ligand_id = input("What is the id of your ligand (e.g., hm1, tau)? ")
        ligand_index = input("What is the index of your ligand minus 1 if after the stripped metal? ")
        start = 100000
        stride = 50
        cpus = 8
        pyqmmm.md.amber_toolkit.gbsa_script(protein_id, ligand_id, ligand_index, start, stride, cpus)

    elif gbsa_analysis:
        click.echo("> Analyze a GBSA calculation output:")
        click.echo("> Loading...")
        import pyqmmm.md.gbsa_analyzer
        pyqmmm.md.gbsa_analyzer.analyze()

    elif compute_hbond:
        click.echo("> Compute all hbonds between the protein and the substrate using CPPTraj:")
        click.echo("> Loading...")
        import pyqmmm.md.hbond_analyzer
        import pyqmmm.md.amber_toolkit
        protein_id = input("What is the name of your protein (e.g., DAH)? ")
        substrate_index = input("What is the index of your substrate (e.g., 355)? ")
        residue_range = input("What is the range of residues in your protein (e.g., 1-351)? ")
        hbonds_script = pyqmmm.md.amber_toolkit.calculate_hbonds_script(protein_id, substrate_index, residue_range)
        submit_script = pyqmmm.md.amber_toolkit.submit_script(protein_id, "hbonds.in")
        pyqmmm.md.hbond_analyzer.compute_hbonds(hbonds_script, submit_script, "hbonds.in")

    elif hbond_analysis:
        click.echo("> Extract and plot hbonding patterns from an MD simulation:")
        click.echo("> Loading...")
        import pyqmmm.md.hbond_analyzer
        # Include more than one path in the list to perform multiple analyses
        file_paths = ["./"]
        names = ["unrestrained"]
        substrate = input("   > What is the resid of your substrate? (e.g., DCA) ")
        pyqmmm.md.hbond_analyzer.analyze_hbonds(file_paths, names, substrate)

    elif last_frame:
        click.echo("> Extracting the last frame from a MD simulation:")
        click.echo("> Loading...")
        import pyqmmm.md.amber_toolkit
        prmtop = input("What is the path of your prmtop file? ")
        mdcrd = input("What is the path of your trajectory file? ")
        pyqmmm.md.amber_toolkit.get_last_frame(prmtop, mdcrd, "final_frame.pdb")
        
    elif residue_list:
        click.echo("> Extract the residues from a PDB:")
        click.echo("> Loading...")
        import pyqmmm.md.residue_lister
        pyqmmm.md.residue_lister.list_residues()

    elif colored_rmsd:
        click.echo("> Color a MD trajectory by clusters:")
        click.echo("> Loading...")
        import pyqmmm.md.rmsd_clusters_colorcoder
        yaxis_title = "RMSD (Å)"
        pyqmmm.md.rmsd_clusters_colorcoder.rmsd_clusters_colorcoder(yaxis_title, layout='wide')

    elif restraint_plot:
        click.echo("> Generate single KDE plot with hyscore measurements:")
        click.echo("> Loading...")
        import pyqmmm.md.kde_restraint_plotter
        pyqmmm.md.kde_restraint_plotter.restraint_plot()

    elif strip_all:
        click.echo("> Strip waters and metals and create new traj and prmtop file:")
        click.echo("> Loading...")
        import pyqmmm.md.amber_toolkit
        protein_id = input("What is the id of your protein (e.g., taud, mc6)? ")
        cpus = 8
        pyqmmm.md.amber_toolkit.strip_all_script(protein_id)
        pyqmmm.md.amber_toolkit.submit_script(protein_id, "strip.in", cpus)

    elif dssp_plot:
        click.echo("> Create a DSSP plot from CPPTraj data:")
        click.echo("> Loading...")
        import pyqmmm.md.dssp_plotter
        pyqmmm.md.dssp_plotter.combine_dssp_files()


@click.command()
@click.option("--plot_energy", "-pe", is_flag=True, help="Plot the energy of a xyz traj.")
@click.option("--flip_xyz", "-f", is_flag=True, help="Reverse and xyz trajectory.")
@click.option("--plot_mechanism", "-pm", is_flag=True, help="Plot energies for all steps of a mechanism.")
@click.option("--residue_decomp", "-rd", is_flag=True, help="Analyze residue decomposition analysis.")
@click.help_option('--help', '-h', is_flag=True, help='Exiting pyQMMM.')
def qm(
    plot_energy,
    flip_xyz,
    plot_mechanism,
    residue_decomp,
    ):
    """
    Functions for quantum mechanics (QM) simulations.

    """
    if plot_energy:
        click.echo("> Plot xyz trajectory energies:")
        click.echo("> Loading...")
        import pyqmmm.qm.energy_plotter
        pyqmmm.qm.energy_plotter.plot_energies()

    if flip_xyz:
        click.echo("> Reverse an xyz trajectory:")
        click.echo("> Loading...")
        import pyqmmm.qm.xyz_flipper
        in_file = input("What is the name of the xyz trajectory to reverse (omit extenstion)? ")
        pyqmmm.qm.xyz_flipper.xyz_flipper(in_file)

    if plot_mechanism:
        click.echo("> Combine all mechanism energetics and plot:")
        click.echo("> Loading...")
        import pyqmmm.qm.mechanism_plotter
        color_scheme = input("What color scheme would you like (e.g., tab20, viridis)? ")
        pyqmmm.qm.mechanism_plotter.generate_plot(color_scheme)

    if residue_decomp:
        click.echo("> Analyze residue decomposition jobs:")
        click.echo("> Loading...")
        import pyqmmm.qm.residue_decomposition
        pyqmmm.qm.residue_decomposition.residue_decomposition()

if __name__ == "__main__":
    # Run the command-line interface when this script is executed
    job = input("Would you like to run an MD or QM task? (md/qm) ")
    if job == "md":
        md()
    elif job == "qm":
        qm()
    else:
        print(f"{job} is not a valid response.")
