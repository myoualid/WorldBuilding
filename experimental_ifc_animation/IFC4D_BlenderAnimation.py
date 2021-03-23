import blenderbim.bim.ifc
import ifcopenshell

### Author BIM file ###
#Get File
file = blenderbim.bim.ifc.IfcStore().get_file()

#Create WorkSchedule Entity
ws_baseline = file.createIfcWorkPlan(ifcopenshell.guid.new(),Name='WorkSchedule Construction - Planned Baseline',PredefinedType ='BASELINE')

#Create Task Entities
task_slab_1 = file.createIfcTask(ifcopenshell.guid.new(),Name='Ground Floor: Concrete Slab Construction')
task_slab_2 = file.createIfcTask(ifcopenshell.guid.new(),Name='Roof Level: Concrete slab Consruction')
task_wall_1 = file.createIfcTask(ifcopenshell.guid.new(),Name='Ground Floor: Maconery Wall 1 consruction')
task_wall_2 = file.createIfcTask(ifcopenshell.guid.new(),Name='Ground Floor: Maconery Wall 2 consruction')
task_wall_3 = file.createIfcTask(ifcopenshell.guid.new(),Name='Ground Floor: Maconery Wall 3 consruction')
task_wall_4 = file.createIfcTask(ifcopenshell.guid.new(),Name='Ground Floor: Maconery Wall 4 consruction')

#Assign tasks to Workschedule: (Control Assignment Concept )
rac_baseline = file.createIfcRelAssignsToControl(ifcopenshell.guid.new(),Name='Baseline Control Relationship')
rac_baseline.RelatingControl = ws_baseline
rac_baseline.RelatedObjects = [task_slab_1,task_slab_2,task_wall_1,task_wall_2,task_wall_3,task_wall_4]

#create task sequencing: (Sequential Connectivity Concept)
rs_1 = file.createIfcRelSequence(ifcopenshell.guid.new(),Name='Process sequence 1',SequenceType= 'FINISH_START',RelatingProcess=task_slab_1, RelatedProcess=task_wall_1)
rs_2 = file.createIfcRelSequence(ifcopenshell.guid.new(),Name='Process sequence 2',SequenceType= 'FINISH_START',RelatingProcess=task_wall_1, RelatedProcess=task_wall_2)
rs_3 = file.createIfcRelSequence(ifcopenshell.guid.new(),Name='Process sequence 3',SequenceType= 'FINISH_START',RelatingProcess=task_wall_2, RelatedProcess=task_wall_3)
rs_4 = file.createIfcRelSequence(ifcopenshell.guid.new(),Name='Process sequence 4',SequenceType= 'FINISH_START',RelatingProcess=task_wall_3, RelatedProcess=task_wall_4)
rs_5 = file.createIfcRelSequence(ifcopenshell.guid.new(),Name='Process sequence 5',SequenceType= 'FINISH_START',RelatingProcess=task_wall_4, RelatedProcess=task_slab_2)


#Get current ifc model's elements:
elements = file.by_type('IfcElement')

#organise elements in dictionnary:
dict_elements = {}
for element in elements:
    dict_elements[element.Name] = element
    
#Assign Elements to Tasks
ratp_1 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Wall assignement 1',RelatedObjects=[task_wall_1],RelatingProduct=dict_elements['Wall-1'])
ratp_2 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Wall assignement 2',RelatedObjects=[task_wall_2],RelatingProduct=dict_elements['Wall-2'])
ratp_3 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Wall assignement 3',RelatedObjects=[task_wall_3],RelatingProduct=dict_elements['Wall-3'])
ratp_4 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Wall assignement 4',RelatedObjects=[task_wall_4],RelatingProduct=dict_elements['Wall-4'])
ratp_5 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Slab assignement 1',RelatedObjects=[task_slab_1],RelatingProduct=dict_elements['Slab-1'])
ratp_6 = file.createIfcRelAssignsToProduct(ifcopenshell.guid.new(),Name='Slab assignement 2',RelatedObjects=[task_slab_2],RelatingProduct=dict_elements['Slab-2'])