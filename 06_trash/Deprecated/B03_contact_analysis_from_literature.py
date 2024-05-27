import sys, os
import subprocess as sp
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from matplotlib import colors
from IPython.display import set_matplotlib_formats
from IPython.display import display

# matplotlib inline
set_matplotlib_formats('png')
plt.figure(figsize=(5, 7))
import ipywidgets as widgets

"""
这是从文献中获得的基于图论的有关碱基接触分析的代码，暂未研究
"""

# ————————  收集VMD的输入文件  ————————

class data_input():
    def __init__(self,
                 pwd="/../../../",
                 top="*.prmtop or *.psf",
                 dcd="*.dcd",
                 sele1="all and noh",
                 sele2="all and noh",
                 cutoff="4.5",
                 tcl_loc="o_path to tcl files (bigdcd.tcl and vmd_contact.tcl)",
                 vmd_path="full o_path to vmd executable"
                 ):
        layout = widgets.Layout(width='auto', height='40px')  # set width and height
        self.pwd = widgets.Text(description='Working Dir:', value=pwd, layout=layout)
        self.top = widgets.Text(description='Toppar file:', value=top, layout=layout)
        self.dcd = widgets.Text(description='Traj:', value=dcd, layout=layout)
        self.sele1 = widgets.Text(description='selection-1:', value=sele1, layout=layout)
        self.sele2 = widgets.Text(description='selection-2:', value=sele2, layout=layout)
        self.cutoff = widgets.Text(description='Cutoff (A):', value=cutoff, layout=layout)
        self.tcl_loc = widgets.Text(description='Tcl o_path:', value=tcl_loc, layout=layout)
        self.vmd_path = widgets.Text(description='VMD o_path:', value=vmd_path, layout=layout)
        self.pwd.on_submit(self.handle_submit)
        self.top.on_submit(self.handle_submit)
        self.dcd.on_submit(self.handle_submit)
        self.sele1.on_submit(self.handle_submit)
        self.sele2.on_submit(self.handle_submit)
        self.cutoff.on_submit(self.handle_submit)
        self.tcl_loc.on_submit(self.handle_submit)
        self.vmd_path.on_submit(self.handle_submit)
        display(self.pwd, self.top, self.dcd, self.sele1, self.sele2, self.cutoff, self.tcl_loc, self.vmd_path)

    def handle_submit(self, text):
        self.v = text.value
        return self.v


print("After input, press return in any field")
f = data_input()

tcl_files = os.path.join(f.tcl_loc.value, "*.tcl")
# print(tcl_files)
copy = 'cp ' + tcl_files + " " + f.pwd.value + "."
# print(copy)
sp.run(copy, shell=True)

print("Working Dir:", f.pwd.value)
print("toppar file:", f.top.value)
print("DCD file:", f.dcd.value)
print("Selection 1:", f.sele1.value)
print("Selection 2:", f.sele2.value)
print("Cutoff distance (Angstrom):", f.cutoff.value)
print("List of Content in the working directory", os.listdir(f.pwd.value))

# ————Change to Working Directory . . .————

print("Current directory:", os.getcwd())
if os.getcwd() + "/" != f.pwd.value:
    os.chdir(f.pwd.value)
    print("\nNow in working directory:", os.getcwd())
else:
    print("\nAlready in working directory ....")
sed = 'sed ' + '\"s/top_file/' + f.top.value + '/g; s/dcd_file/' + f.dcd.value + '/g; s/cutoff_dist/' + f.cutoff.value + '/g; s/selection1/' + f.sele1.value + '/g; s/selection2/' + f.sele2.value + '/g\" ' + 'vmd_contact.tcl >' + ' contact_final.tcl'
print(sed)
sp.run(sed, shell=True)

# ————Check for contact_all.dat (05_已得到且已处理的数据文件 of the VMD run) from Any Previous Run . . .————

if os.path.exists("contact_all.dat"):
    copy = 'cp ' + "contact_all.dat" + " " + "contact_all.bak.dat"
    sp.run(copy, shell=True)
    os.remove("contact_all.dat")
    print("Backup created and deleted contact_all.dat file from previous run ....\n")
else:
    print("The file does not exist\n")

print("List of Content in the working directory", os.listdir(f.pwd.value))

# ————跑VMD————

outlogFile = open("Contact-out.log", "w")
errlogFile = open("Contact-err.log", "w")
# p = sp.Popen(['/Applications/VMD_1.9.4a51-x86_64-Rev9.app/Contents/Resources/VMD.app/Contents/MacOS/VMD', '-dispdev', 'none', '-e', 'contact_final.tcl'], stdout=outlogFile, stdin=sp.PIPE, stderr=errlogFile)
p = sp.Popen([f.vmd_path.value, '-dispdev', 'none', '-e', 'contact_final.tcl'], stdout=outlogFile, stdin=sp.PIPE,
             stderr=errlogFile)
# p.communicate()
p.wait()
if p.poll is None:
    print("VMD still running..")
else:
    print("Run finished.. check whether the 05_已得到且已处理的数据文件 contact_all.dat is okay")


# ————————计算接触图————————

# 收集输入

class req_inputs():
    def __init__(self,
                 pwd1="/../../../",
                 out="prefix of 05_已得到且已处理的数据文件 map",
                 res_range1="provide the range of residues from selection1 [e.g. 1 to 1200]",
                 res_range2="provide the range of residues from selection2 [e.g. 1 to 1200]"
                 ):
        layout = widgets.Layout(width='auto', height='40px')  # set width and height
        self.pwd1 = widgets.Text(description='Working Dir:', value=pwd1, layout=layout)
        self.out = widgets.Text(description='Outfile prefix:', value=out, layout=layout)
        self.res_range1 = widgets.Text(description='Res_range1:', value=res_range1, layout=layout)
        self.res_range2 = widgets.Text(description='Res_range2:', value=res_range2, layout=layout)
        self.pwd1.on_submit(self.handle_submit)
        self.out.on_submit(self.handle_submit)
        self.res_range1.on_submit(self.handle_submit)
        self.res_range2.on_submit(self.handle_submit)
        display(self.pwd1, self.out, self.res_range1, self.res_range2)

    def handle_submit(self, text):
        self.v = text.value
        return self.v


print("After input, press return in any field")
g = req_inputs()


# ————Function to Calculate the contact Matrix————

def save_contact_map(contact_file, res_range1, res_range2, frames, output_file, exclude=False):
    f2 = 1
    running_contact = np.zeros(shape=(res_range1, res_range2))
    t = np.zeros(shape=(res_range1, res_range2))

    with open(contact_file, "r") as input:
        for line in input:
            lines = line.split()
            f = int(lines[0])
            if exclude:
                if (lines[2] not in exclude_list) and (lines[5] not in exclude_list):
                    res1 = int(lines[1])
                    res2 = int(lines[4])
            else:
                res1 = int(lines[1])
                res2 = int(lines[4])

            f1 = f
            if f1 == f2:  # Avoid repeating same contacts from same frames
                running_contact[res1, res2] = 1
                if res_range1 == res_range2:
                    running_contact[res2, res1] = 1
            else:
                t = np.add(t, running_contact)  # Updating after each frame
                running_contact = np.zeros(shape=(res_range1, res_range2))
                running_contact[res1, res2] = 1
                if res_range1 == res_range2:
                    running_contact[res2, res1] = 1
            f2 = f1

    t = np.add(t, running_contact)

    contactMat = np.true_divide(t, frames)  # Getting the fraction

    if res_range1 == res_range2:
        for x in range(res_range1):
            contactMat[x, x] = 1  # Same residue contact
            for y in range(x, res_range1):
                contactMat[x, y] = contactMat[y, x]  # For the lower diagonal

    print("Saving the map in a tabular format...\n")
    print("Original residue IDs are maintained as provided in the selection....\n")

    with open(output_file + ".dat", "w+") as fo2:
        for i in range(res_range1):
            for j in range(res_range2):
                if contactMat[i, j] != 0:
                    fo2.write("%s %s %8.3f\n" % (
                        i + int(g.res_range1.value.split()[0]), j + (int(g.res_range2.value.split()[0])), contactMat[
                            i, j]))

            print("Done Saving.. check the *.dat file\n")

            print("Saving the map in *.npy format...\n")
            print("It's just the matrix, so only indexes for the provided range start from 0\n")
            print("Be careful if you are plotting the matrix directly, you have to change the indexes accordingly..\n")

            np.save(output_file + ".npy", contactMat)
            print("Done Saving..\n")

            print("Printing the contact map...")
            print(contactMat)  # Check cmap


# Get Frame Id and Resid Pairs for Calculation of contact Map and Get Total Residues, Total Frames . . .

contact = os.path.join(g.pwd1.value, "contact_all.dat")
res_range1 = len(np.arange(int(g.res_range1.value.split()[0]), int(g.res_range1.value.split()[2]) + 1))
res_range2 = len(np.arange(int(g.res_range2.value.split()[0]), int(g.res_range2.value.split()[2]) + 1))
print("Selection-1 length:", res_range1, "\n", "Selection-2 length:", res_range2, "\n")

s4 = 'tail -n1 ' + contact + ' | awk \'{print $1}\''
frames = int(sp.getoutput(s4))  # Get total frames
print('No of frames:', frames)

exclude_list = ['ALA', 'GLY', 'VAL']
outfile = os.path.join(g.pwd1.value, g.out.value)

# A contact map without seleted resnames
save_contact_map(contact, res_range1, res_range2, frames, outfile, exclude=True)

# A contact map without any exclusion
save_contact_map(contact, res_range1, res_range2, frames, outfile)

# ————Read contact Data and Plot . . .————

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets

contact = np.loadtxt(outfile + ".dat")
df_contact = pd.DataFrame(contact, columns=['X', 'Y', 'Z'])


# % matplotlib inline
# % config InlineBackend.figure_format = 'retina'  # high resolution

def plot_contact_map(min_value=0.1, max_value=0.9, save=0, figsize_x=8, figsize_y=8):
    df_contact_A = df_contact[((df_contact['Z'] > min_value) & (df_contact['Z'] < max_value))][['X', 'Y', 'Z']]
    fig = plt.figure(figsize=(figsize_x, figsize_y))
    spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
    ax1 = fig.add_subplot(spec[0, 0])

    data = [df_contact_A]
    axss = [ax1]
    header = ['Contact Map']

    for ax in axss:
        ax.grid(which='both')

    for l, n, i in zip(data, axss, header):
        X = n.scatter(l.X, l.Y, s=2, c=l.Z, cmap='coolwarm')
        n.axis([df_contact["X"].min(), df_contact["X"].max() + 10, df_contact["Y"].min(), df_contact[
            "Y"].max() + 10])
        n.set_title(i, fontsize=16, fontweight='bold')
        n.set_xlabel('Selection 1 resids ->', fontsize=14, fontweight='bold')
        n.set_ylabel('Selection 2 resids ->', fontsize=14, fontweight='bold')

        # Setting up x- and y-ticks and tick labels
        if df_contact["X"].max() - df_contact["X"].min() > 500:
            n.set_xticks(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 100))
            n.set_xticklabels(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 100), fontsize=12)
        elif df_contact["X"].max() - df_contact["X"].min() < 50:
            n.set_xticks(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 5))
            n.set_xticklabels(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 5), fontsize=12)
        else:
            n.set_xticks(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 10))
            n.set_xticklabels(np.arange(df_contact["X"].min(), df_contact["X"].max() + 10, 10), fontsize=12)

        # TODO 不知道这里要不要取消缩进
        if df_contact["Y"].max() - df_contact["Y"].min() > 500:
            n.set_yticks(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 100))
            n.set_yticklabels(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 100), fontsize=12)
        elif df_contact["Y"].max() - df_contact["Y"].min() < 50:
            n.set_yticks(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 5))
            n.set_yticklabels(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 5), fontsize=12)
        else:
            n.set_yticks(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 10))
            n.set_yticklabels(np.arange(df_contact["Y"].min(), df_contact["Y"].max() + 10, 10), fontsize=12)

            plt.colorbar(X, ax=n)

        plt.show()
    # TODO 不知道下面这两块要不要缩进，粘贴过来缩进了2个Tab
    if save == 1:
        A = g.pwd1.value + g.out.value + ".png"
        fig.savefig(A, dpi=300)

    widgets.interact(
        plot_contact_map,
        min_value=(0, 1, 0.1),
        max_value=(0, 1, 0.1),
        save=(0, 1),
        figsize_x=(5, 15),
        figsize_y=(5, 15)
    )


# ————————接触图对比————————

# ————收集输入————


class req_inputs2():
    def __init__(self,
                 pwd2="/../../../",
                 CMap1_path="/../../cmap1.npy (full o_path to the cmap1.npy)",
                 CMap2_path="/../../cmap2.npy (full o_path to the cmap1.npy)",
                 out_pref="crRNA-tgRNA",
                 res_range1="provide the range of residues from selection1 [e.g. 1 to 1153]",
                 res_range2="provide the range of residues from selection2 [e.g. 1154 to 1204]"
                 ):
        layout = widgets.Layout(width='auto', height='40px')  # set width and height
        self.pwd2 = widgets.Text(description='Working Dir:', value=pwd2, layout=layout)
        self.CMap1_path = widgets.Text(description='CMap1\n full o_path:', value=CMap1_path, layout=layout)
        self.CMap2_path = widgets.Text(description='CMap2 full o_path:', value=CMap2_path, layout=layout)
        self.out_pref = widgets.Text(description='Outfile prefix:', value=out_pref, layout=layout)
        self.res_range1 = widgets.Text(description='Res_range1:', value=res_range1, layout=layout)
        self.res_range2 = widgets.Text(description='Res_range2:', value=res_range2, layout=layout)
        self.pwd2.on_submit(self.handle_submit)
        self.CMap1_path.on_submit(self.handle_submit)
        self.CMap2_path.on_submit(self.handle_submit)
        self.out_pref.on_submit(self.handle_submit)
        self.res_range1.on_submit(self.handle_submit)
        self.res_range2.on_submit(self.handle_submit)
        display(self.pwd2, self.CMap1_path, self.CMap2_path, self.out_pref, self.res_range1, self.res_range2)

    def handle_submit(self, text):
        self.v = text.value
        return self.v


print("After input, press return in any field")
h = req_inputs2()

# ——Check Values of the given Inputs . . .————

print("Working Dir:", h.pwd2.value)
print("CMap1:", h.CMap1_path.value)
print("CMap2:", h.CMap2_path.value)
print("Out Prefix:", h.out_pref.value)
print("Selection 1:", h.res_range1.value)
print("Selection 2:", h.res_range2.value)


# ————Calculation of Differential and Unique contact Map————

def process_contact_maps(cmap1, cmap2, output_prefix=h.out_pref.value, res_range1=h.res_range1.value,
                         res_range2=h.res_range2.value):
    ncols1 = a1.shape[0]
    ncols2 = a1.shape[1]

    t1 = np.zeros(shape=(ncols1, ncols2))
    t2 = np.zeros(shape=(ncols1, ncols2))

    for i in range(ncols1):
        for j in range(ncols2):
            if a1[i, j] != 0 and a2[i, j] != 0:
                t1[i, j] = a1[i, j] - a2[i, j]  # differential contact map
            else:
                t2[i, j] = a1[i, j] - a2[i, j]  # unique contact map

    np.save(os.path.join(h.pwd2.value, output_prefix) + "_diff.npy", t1)
    np.save(os.path.join(h.pwd2.value, output_prefix) + "_uniq.npy", t2)

    fo2 = open(os.path.join(h.pwd2.value, output_prefix) + "_diff.dat", "w+")
    fo3 = open(os.path.join(h.pwd2.value, output_prefix) + "_uniq.dat", "w+")

    if ncols1 == ncols2:
        print("We have a symmetric map (same number of residues in rows and columns)...")
        print(
            "With a symmetric map, we are going to 05_已得到且已处理的数据文件 the tabular data in a way that plotting would show stable 1st input contacts in the upper diagonal and stable 2nd input contact in the lower diagonal...")
        for i in range(ncols1):
            for j in range(ncols2):
                if t1[i, j] != 0:
                    fo2.write(
                        "%s %s %8.3f\n" % (i + int(res_range1.split()[0]), j + int(res_range2.split()[0]), t1[i, j]))
                    fo2.write(
                        "%s %s %8.3f\n" % (j + int(res_range2.split()[0]), i + int(res_range1.split()[0]), t1[i, j]))

                if t2[i, j] != 0:
                    fo3.write(
                        "%s %s %8.3f\n" % (i + int(res_range1.split()[0]), j + int(res_range2.split()[0]), t2[i, j]))
                    fo3.write(
                        "%s %s %8.3f\n" % (j + int(res_range2.split()[0]), i + int(res_range1.split()[0]), t2[i, j]))
    else:
        for i in range(ncols1):
            for j in range(ncols2):
                if t1[i, j] != 0:
                    fo2.write(
                        "%s %s %8.3f\n" % (i + int(res_range1.split()[0]), j + int(res_range2.split()[0]), t1[i, j]))

                if t2[i, j] != 0:
                    fo3.write(
                        "%s %s %8.3f\n" % (i + int(res_range1.split()[0]), j + int(res_range2.split()[0]), t2[i, j]))

    fo2.close()
    fo3.close()


a1 = np.load(h.CMap1_path.value)
a2 = np.load(h.CMap2_path.value)

# Get the differential and unique contact maps
process_contact_maps(a1, a2)


# ————Plotting of Differential and Unique contact Maps————

class req_inputs3():
    def __init__(self,
                 pwd3="/../../../",
                 dMap_path="/../../differential_cmap.dat (o_path to the differential contact map)",
                 uMap_path="/../../uniq_cmap.dat (o_path to the uniq contact map)",
                 out_pref="crRNA-tgRNA-5us-cl0-2",
                 res_range1="provide the range of residues from selection1 [e.g. 1 to 1153]",
                 res_range2="provide the range of residues from selection2 [e.g. 1154 to 1204]"
                 ):
        layout = widgets.Layout(width='auto', height='40px')  # set width and height
        self.pwd3 = widgets.Text(description='Working Dir:', value=pwd3, layout=layout)
        self.dMap_path = widgets.Text(description='Diff. map:', value=dMap_path, layout=layout)
        self.uMap_path = widgets.Text(description='Uniq. map:', value=uMap_path, layout=layout)
        self.out_pref = widgets.Text(description='Outfile prefix:', value=out_pref, layout=layout)
        self.res_range1 = widgets.Text(description='Res_range1:', value=res_range1, layout=layout)
        self.res_range2 = widgets.Text(description='Res_range2:', value=res_range2, layout=layout)
        self.pwd3.on_submit(self.handle_submit)
        self.dMap_path.on_submit(self.handle_submit)
        self.uMap_path.on_submit(self.handle_submit)
        self.out_pref.on_submit(self.handle_submit)
        self.res_range1.on_submit(self.handle_submit)
        self.res_range2.on_submit(self.handle_submit)
        display(self.pwd3, self.dMap_path, self.uMap_path, self.out_pref, self.res_range1, self.res_range2)

    def handle_submit(self, text):
        self.v = text.value
        return self.v


print("After input, press return in any field")
i = req_inputs3()

# ————Plot the Differential and Unique contact Maps as Grid Maps:————

Diff = np.loadtxt(i.dMap_path.value)
uniq = np.loadtxt(i.uMap_path.value)
df_diff = pd.DataFrame(Diff, columns=['X', 'Y', 'Z'])
df_uniq = pd.DataFrame(uniq, columns=['X', 'Y', 'Z'])

import matplotlib.gridspec as gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'  # high resolution

def update(min1=0.1, max1=1, min2=-1, max2=-0.1, vmin1=-1, vmax1=1, save=0, figsize_x=8, figsize_y=8, df_diff=None,
           df_uniq=None):
    fig = plt.figure(figsize=(figsize_x, figsize_y))
    spec = gridspec.GridSpec(ncols=1, nrows=2, hspace=0.5, figure=fig)
    axes = [fig.add_subplot(spec[i, 0]) for i in range(2)]

    for ax in axes:
        ax.grid(which='both')
    data = [df_diff, df_uniq]
    headers = ['Differential Map', 'Unique Map']

    for ax, data, header in zip(axes, data, headers):
        filtered_data = data[((data['Z'] >= min1) & (data['Z'] <= max1)) | ((data['Z'] <= max2) & (data['Z'] >= min2))][
            ['X', 'Y', 'Z']]
        X = ax.scatter(filtered_data['X'], filtered_data['Y'], s=30, c=filtered_data['Z'], cmap='coolwarm',
                       edgecolor='black', linewidth=0.2, vmin=vmin1, vmax=vmax1)

        ##-- This is customized selection based on what range of interaction needs to be visualized --##
        ax.axis([370, 382, 1178, 1184])
        ax.set_xticks(np.arange(370, 383, 1))
        ax.set_xticklabels(np.arange(370, 383, 1), fontsize=12, rotation=90)
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.set_yticks(np.arange(1178, 1185, 1))
        ax.set_yticklabels(np.arange(1178, 1185, 1), fontsize=12)
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ## -------------------------------------------------------------------------------------####
        ax.set_title(header, fontsize=16, fontweight='bold')
        ax.set_xlabel('Residues', fontsize=14, fontweight='bold')
        ax.set_ylabel('Residues', fontsize=14, fontweight='bold')
        ax.grid(which='both', linewidth=0.3)
        plt.colorbar(X, ax=ax)

    plt.show()

    if save == 1:
        A = os.path.join(i.pwd3.value, i.out_pref.value + ".png")
        fig.savefig(A, dpi=300)


# Example usage with widgets.interact
widgets.interact(update, min1=(0, 1, 0.1), max1=(0, 1, 0.1), min2=(-1, 0, 0.1), max2=(-1, 0, 0.1),
                 vmin1=(-1, 0, 0.1), vmax1=(0, 1, 0.1), save=(0, 1), figsize_x=(5, 15), figsize_y=(5, 15),
                 df_diff=widgets.fixed(df_diff), df_uniq=widgets.fixed(df_uniq))

# ————Plot Differential contact Maps as Sankey Plots:————

diff = np.load("/Path/to/differential_map.npy")
uniq = np.load("/Path/to/unique_map.npy")
tot = diff + uniq
print(diff.shape, uniq.shape, tot.shape)

#### --- we need a tabular data form -- ####
fo = open("/Path/to/total_diff.dat", "w+")

for i in range(diff.shape[0]):
    for j in range(diff.shape[0]):  ## no diagonal separation
        if (tot[i, j] != 0):
            fo.write("%s %s %8.3f\n" % (i + 1, j + 1, tot[i, j]))
            fo.write("%s %s %8.3f\n" % (j + 1, i + 1, tot[i, j]))
fo.close()

import plotly.graph_objects as go
import matplotlib.gridspec as gridspec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'  # high resolution


Diff = np.loadtxt(
    "/Users/souviksinha/Desktop/Palermo_Lab/LabWork/Project_Cas13a/LbuCas13a-crRNA-target/run/contact-map/tgWT-R963_test_total_diff.dat")
df_diff = pd.DataFrame(Diff, columns=['X', 'Y', 'Z'])


@widgets.interact(min1=(0, 1, 0.05), max1=(0, 1, 0.05), min2=(-1, 0, 0.05), max2=(-1, 0, 0.05))
def update(min1=0.1, max1=1, min2=-1, max2=-0.1):
    df_diff_A = \
    df_diff[((df_diff['Z'] >= min1) & (df_diff['Z'] <= max1)) | ((df_diff['Z'] <= max2) & (df_diff['Z'] >= min2))][
        ['X', 'Y', 'Z']]

    ## ---------------- selection of residues ---------------- ##
    # Say, 1st selection: resid 1177 - 1185; 2nd selection: resid 369 - 382; 3rd selection: resid 959 - 976

    range1_min, range1_max, range2_min, range2_max, range3_min, range3_max = 1177, 1185, 369, 383, 959, 976

    ### ------ Section for 2 selection sankey (i.e. contacts between 2 selections) ----- ###
    #      df_diff_A_dom = df_diff_A[((df_diff_A['X']>range2_min) & (df_diff_A['X']<range2_max)) & ((df_diff_A['Y']< range3_max) & (df_diff_A['Y'] > range3_min)) ][['X','Y','Z']]

    ### ------ Section for 3 selection sankey (i.e. contacts between 3 selections) ----- ###
    df_diff_A_dom3 = df_diff_A[((df_diff_A['X'] > range1_min) & (df_diff_A['X'] < range1_max)) & (
                (df_diff_A['Y'] < range2_max) & (df_diff_A['Y'] > range2_min))][['X', 'Y', 'Z']]
    df_diff_A_dom2 = df_diff_A[((df_diff_A['Y'] > range1_min) & (df_diff_A['Y'] < range1_max)) & (
                (df_diff_A['X'] < range3_max) & (df_diff_A['X'] > range3_min))][['X', 'Y', 'Z']]
    df_diff_A_dom = pd.concat([df_diff_A_dom2, df_diff_A_dom3], axis=0, ignore_index=True)

    ## ------------------------------------------------------------------- ##
    sources = []
    targets = []
    values = []
    labels = [i for i in list(set(df_diff_A_dom.X.tolist())) + list(set(df_diff_A_dom.Y.tolist()))]
    labels_sort = sorted(labels)

    ### ------ Section for 2 selection sankey (i.e. contacts between 2 selections) ----- ###
    #     X = [0.8 if ((i > range3_min) & (i < range3_max)) else 0.1 for i in labels_sort]
    #     c1, c2 = 0, 0

    ### ------ Section for 3 selection sankey (i.e. contacts between 3 selections) ----- ###
    X = [0.9 if ((i > range3_min) & (i < range3_max)) else 0.5 if ((i > range1_min) & (i < range1_max)) else 0.1 for i
         in labels_sort]
    c1, c2, c3 = 0, 0, 0

    Y = []

    ### --- 2 selection sankey --- ###
    #     for j in X:
    #         if j == 0.8:
    #             c1+=1
    #             Y.append(0.06*c1)
    #         else:
    #             c2+=1
    #             Y.append(0.06*c2)

    ### --- 3 selection sankey --- ###
    for j in X:
        if j == 0.1:
            c1 += 1
            Y.append(0.06 * c1)
        elif j == 0.5:
            c2 += 1
            Y.append(0.06 * c2)
        else:
            c3 += 1
            Y.append(0.06 * c3)

    ### -------------------------------------------- #########

    for index, row in df_diff_A_dom.iterrows():
        m = labels_sort.index(row['X'])
        n = labels_sort.index(row['Y'])
        sources.append(m)
        targets.append(n)
        values.append(abs(row['Z']))
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=40,
            thickness=40,
            line=dict(color="black", width=1),
            label=[str(i) for i in labels_sort],  ## for label on-and-off
            x=X,
            y=Y,
            color=["#EB7B36" if ((i > range1_min) & (i < range1_max)) else "#E2BEE5" if (
                        (i > range2_min) & (i < range2_max)) else "#7BE6BE" if (
                        (i > range3_min) & (i < range3_max)) else "#F7EFDB" for i in labels_sort]
        ),
        link=dict(
            source=sources,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=targets,
            value=values,
            color=['rgba(211,45,61, 0.5)' if i > 0 else 'rgba(47, 108, 188, 0.5)' for i in df_diff_A_dom.Z]
            # for differential map
        ))])

    fig.update_layout(title_text="Put_a_title", font_size=14)

    fig.show()
