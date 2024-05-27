from common_tools import *

paths=get_PDB_paths(origin_PDB_path)
objects=get_object_names(origin_PDB_path)

target_objects_n=[6,26]

pymol.finish_launching()

# def get_distance(the_object,flag=0):
#     A_3=f"{the_object}_A_3"
#     A_4=f"{the_object}_A_4"
#     R963=f"{the_object}_R963"
#     Y967=f"{the_object}_Y967"
#     A_3_selected=f"{the_object}_A_-3_selected"
#     A_4_selected=f"{the_object}_A_-4_selected"
#     A_3_behalf=f"{the_object}_A_-3_behalf"
#     A_4_behalf=f"{the_object}_A_-4_behalf"
#     R963_CA=f"{the_object}_R963_CA"
#     Y967_CA=f"{the_object}_Y967_CA"
#     dis_A_3_to_963=f"{the_object}_dis_A_3_to_963"
#     dis_A_4_to_967=f"{the_object}_dis_A_4_to_967"
#
#     pymol_cmd.select(A_3,f"object {the_object} and chain B and resi 28")
#     pymol_cmd.select(A_4,f"object {the_object} and chain B and resi 27")
#     pymol_cmd.select(R963,f"object {the_object} and chain A and resi 963")
#     pymol_cmd.select(Y967,f"object {the_object} and chain A and resi 967")
#
#     pymol_cmd.show_as("sticks",A_3)
#     pymol_cmd.show_as("sticks",A_4)
#     pymol_cmd.show("sticks",R963)
#     pymol_cmd.show("sticks",Y967)
#
#     pymol_cmd.select(A_3_selected,f"object {the_object} and chain B and resi 28 and name N1+C6")
#     pymol_cmd.select(A_4_selected, f"object {the_object} and chain B and resi 27 and name N1+C6")
#     pymol_cmd.select(R963_CA,f"object {the_object} and chain A and resi 963 and name CA")
#     pymol_cmd.select(Y967_CA,f"object {the_object} and chain A and resi 967 and name CA")
#     pymol_cmd.pseudoatom(A_3_behalf,A_3_selected)
#     pymol_cmd.pseudoatom(A_4_behalf,A_4_selected)
#     dis_v_A_3_to_963=pymol_cmd.distance(dis_A_3_to_963,A_3_behalf,R963_CA)
#     dis_v_A_4_to_967=pymol_cmd.distance(dis_A_4_to_967,A_4_behalf,Y967_CA)
#
#     pymol_cmd.set("label_size",30,dis_A_3_to_963)
#     pymol_cmd.set("label_size",30,dis_A_4_to_967)
#     pymol_cmd.set("label_position",[1,1,1],dis_A_3_to_963)
#     pymol_cmd.set("label_position",[1,1,1],dis_A_4_to_967)
#     pymol_cmd.set("cartoon_ring_mode", 3, A_3)
#     pymol_cmd.set("cartoon_ring_mode", 3, A_4)
#     pymol_cmd.refresh()
#     return dis_v_A_3_to_963,dis_v_A_4_to_967

def get_distance(obj,flag=0):
    A_3=f"{obj}_A_3"
    A_4=f"{obj}_A_4"
    R963=f"{obj}_R963"
    Y967=f"{obj}_Y967"
    A_3_selected=f"{obj}_A_-3_selected"
    A_4_selected=f"{obj}_A_-4_selected"
    A_3_behalf=f"{obj}_A_-3_behalf"
    A_4_behalf=f"{obj}_A_-4_behalf"
    R963_CA=f"{obj}_R963_CA"
    Y967_CA=f"{obj}_Y967_CA"
    dis_A_3_to_963=f"{obj}_dis_A_3_to_963"
    dis_A_4_to_967=f"{obj}_dis_A_4_to_967"

    pymol_cmd.select(A_3,f"object {obj} and chain B and resi 28")
    pymol_cmd.select(A_4,f"object {obj} and chain B and resi 27")
    pymol_cmd.select(R963,f"object {obj} and chain A and resi 963 and not name N+CA+C+O")
    pymol_cmd.select(Y967,f"object {obj} and chain A and resi 967 and not name N+CA+C+O")

    # pymol_cmd.show_as("sticks",A_3)
    # pymol_cmd.show_as("sticks",A_4)
    pymol_cmd.show("sticks",R963)
    pymol_cmd.show("sticks",Y967)

    pymol_cmd.select(A_3_selected,f"object {obj} and chain B and resi 28 and name N1+C6")
    pymol_cmd.select(A_4_selected, f"object {obj} and chain B and resi 27 and name N1+C6")
    pymol_cmd.select(R963_CA,f"object {obj} and chain A and resi 963 and name CA")
    pymol_cmd.select(Y967_CA,f"object {obj} and chain A and resi 967 and name CA")
    pymol_cmd.pseudoatom(A_3_behalf,A_3_selected)
    pymol_cmd.pseudoatom(A_4_behalf,A_4_selected)
    dis_v_A_3_to_963=pymol_cmd.distance(dis_A_3_to_963,A_3_behalf,R963_CA)
    dis_v_A_4_to_967=pymol_cmd.distance(dis_A_4_to_967,A_4_behalf,Y967_CA)

    pymol_cmd.set("label_size",30,dis_A_3_to_963)
    pymol_cmd.set("label_size",30,dis_A_4_to_967)
    pymol_cmd.set("label_position",[1,1,1],dis_A_3_to_963)
    pymol_cmd.set("label_position",[1,1,1],dis_A_4_to_967)
    # 将碱基的环设置为实心的
    pymol_cmd.set("cartoon_ring_mode", 3, A_3)
    pymol_cmd.set("cartoon_ring_mode", 3, A_4)
    pymol_cmd.label()
    pymol_cmd.label2()
    pymol_cmd.refresh()
    return dis_v_A_3_to_963,dis_v_A_4_to_967


for n in target_objects_n:
    obj_name=objects[n]
    # 加载对象
    pymol_cmd.load(paths[n], obj_name)
    remove_solvent()
    get_distance(obj_name)

pymol_cmd.disable()







