import blenderbim.bim.ifc
import ifcopenshell
import bpy

def get_task(element):
    task = None
    for reference in element.ReferencedBy:
        if reference.is_a('IfcRelAssignsToProduct'):
            for object in reference.RelatedObjects:
                if object.is_a('IfcTask'):
                    task = object
    return task

def get_next_task(task):
    next_task = None
    for predecessor_to in task.IsPredecessorTo:
        if predecessor_to.SequenceType == 'FINISH_START':
            next_task = predecessor_to.RelatedProcess
    return next_task

def get_next_object(object):
    rel_task = get_next_task(get_task(object))
    next_object = None
    for assignement in rel_task.HasAssignments:
        if assignement.is_a('IfcRelAssignsToProduct'):
            next_object = assignement.RelatingProduct
    return next_object
    
def get_sequence_from(object):
    sequence = {}
    count = 0
    sequence[object.Name] = object
    next_object = object
    trigger = True
    while trigger:
        try:
            next_object = get_next_object(next_object)
            sequence[next_object.Name] = next_object
        except:
            trigger = False
    return sequence

#Blender Animation
def select_object(input):
    for object in bpy.data.objects:
        if object.type == 'MESH' and (str(input) in object.name):
            object.select_set(True)
            return object
            
def set_animation(sequence):
    sequence_list = list(sequence.values()) 
    count = 0
    t = 0
    trigger = True
    while trigger:
        try:
            obj = select_object(sequence_list[count].Name)
            obj.hide_render = True
            obj.hide_viewport = True # or False to NOT hide.
            obj.keyframe_insert(data_path="hide_render", frame=t)
            obj.keyframe_insert(data_path="hide_viewport", frame=t)
            t += 30
            obj.hide_render = False
            obj.hide_viewport = False # or False to NOT hide.
            obj.keyframe_insert(data_path="hide_render", frame=t)
            obj.keyframe_insert(data_path="hide_viewport", frame=t)
            count += 1
        except:
            trigger = False

def get_all_elements():
    file = blenderbim.bim.ifc.IfcStore().get_file()
    elements = file.by_type('IfcElement')
    dict_elements = {}
    for element in elements:
        dict_elements[element.Name] = element
    return dict_elements
    

elements = get_all_elements()
sequence = get_sequence_from(elements['Slab-1'])
set_animation(sequence)