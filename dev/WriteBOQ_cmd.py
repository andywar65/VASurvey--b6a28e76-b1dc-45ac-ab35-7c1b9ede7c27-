import csv
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va
import Rhino
import rhinoscriptsyntax as rs
from AddConstructionParameters_cmd import (
    physical_parameters,
    wall_demolition_parameters,
    transportation_parameters,
    wall_construction_parameters,
    slab_demolition_parameters,
    slab_construction_parameters,
    finish_demolition_parameters,
    finish_construction_parameters,
)

__commandname__ = "WriteBOQ"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    #prompt the user for the Wall csv to import
    filter = "CSV file (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.OpenFileName("Open Wall Table File", filter)
    if not filename: return
    # extract a wall list with clean values
    with open(filename) as csvfile:
        wall_dict = {}
        original = csv.DictReader(csvfile)
        for row in original:
            wall_dict[row["\xef\xbb\xbfDescription"]]={
                "Style": row["Style"],
                "Length": float(row["Length"]),
                "Area": float(row["Area"].split(" ")[0]),
                "Volume": float(row["Volume"].split(" ")[0]),
            }
    csvfile.close()
    wall_params = (
        physical_parameters + 
        wall_demolition_parameters +
        transportation_parameters +
        wall_construction_parameters +
        finish_demolition_parameters +
        finish_construction_parameters
    )
    # get all objects in file
    objects = Rhino.RhinoDoc.ActiveDoc.Objects
    for obj in objects:
        # filter walls
        if obj.IsNormal and va.IsWall(obj.Id):
            # add parameters to wall dictionary
            for param in wall_params:
                param_id = va.GetObjectParameterId(param[0], obj.Id,1)
                value = va.GetParameterValue(param_id, obj.Id)
                type = va.GetParameterType(param_id)
                if value:
                    wall_dict[str(obj.Id)][param[0]] = value
    #prompt the user for the Slab csv to import
    filename = rs.OpenFileName("Open Slab Table File", filter)
    if not filename: return
    # extract a slab list with clean values
    with open(filename) as csvfile:
        slab_dict = {}
        original = csv.DictReader(csvfile)
        for row in original:
            slab_dict[row["\xef\xbb\xbfDescription"]]={
                "Style": row["Style"],
                "Area": float(row["Area"].split(" ")[0]),
                "Volume": float(row["Volume"].split(" ")[0]),
            }
    csvfile.close()
    slab_params = (
        physical_parameters + 
        slab_demolition_parameters +
        transportation_parameters +
        slab_construction_parameters +
        finish_demolition_parameters +
        finish_construction_parameters
    )
    for obj in objects:
        # filter slabs
        if obj.IsNormal and va.IsSlab(obj.Id):
            # add parameters to wall dictionary
            for param in slab_params:
                param_id = va.GetObjectParameterId(param[0], obj.Id,1)
                value = va.GetParameterValue(param_id, obj.Id)
                type = va.GetParameterType(param_id)
                if value:
                    slab_dict[str(obj.Id)][param[0]] = value
    print(wall_dict, slab_dict)
    # write BOQ dictionary
    # activity dictionaries
    activities = {}
    wall_demolition = {}
    wall_construction = {}
    slab_demolition = {}
    slab_construction = {}
    # activity lists
    wall_demolition_activities = []
    transportation_activities = []
    wall_construction_activities = []
    slab_demolition_activities = []
    slab_construction_activities = []
    for p in wall_demolition_parameters:
        wall_demolition_activities.append((p[0], p[0], p[3], p[4], p[5]))
    for p in transportation_parameters:
        transportation_activities.append((p[0], p[0], p[3]))
    for p in wall_construction_parameters:
        wall_construction_activities.append((p[0], p[0], p[3], p[4], p[5]))
    for p in slab_demolition_parameters:
        slab_demolition_activities.append((p[0], p[0], p[3], p[4], p[5]))
    for p in slab_construction_parameters:
        slab_construction_activities.append((p[0], p[0], p[3], p[4], p[5]))
    for p in finish_demolition_parameters:
        wall_demolition_activities.append((p[0], p[0], p[3], p[4], p[5]))
        slab_demolition_activities.append((p[0], p[0], p[3], p[4], p[5]))
    for p in finish_construction_parameters:
        wall_construction_activities.append((p[0], p[0], p[3], p[4], p[5]))
        slab_construction_activities.append((p[0], p[0], p[3], p[4], p[5]))
    # fill the activity dictionaries for walls
    for id, values in wall_dict.items():
        weight = 0
        if "Unit weight" in values and "Volume" in values:
            weight = values["Unit weight"] * values["Volume"]
        for act in wall_demolition_activities:
            if act[0] in values:
                activities["Demolizioni"] = True
                # [3] selects style mode, [4] selects parameter
                if act[3]:
                    if values["Style"] in wall_demolition:
                        wall_demolition[values["Style"]] += values[act[4]]
                    else:
                        wall_demolition[values["Style"]] = values[act[4]]
                else:
                    if act[1] in activities:
                        activities[act[1]] += values[act[4]] * values[act[0]]
                    else:
                        activities[act[1]] = values[act[4]] * values[act[0]]
        for act in transportation_activities:
            if act[0] in values:
                activities["Trasporti"] = True
                if act[1] in activities:
                    activities[act[1]] += weight
                else:
                    activities[act[1]] = weight
        for act in wall_construction_activities:
            if act[0] in values:
                activities["Ricostruzioni"] = True
                # [3] selects style mode, [4] selects parameter
                if act[3]:
                    if values["Style"] in wall_construction:
                        wall_construction[values["Style"]] += values[act[4]]
                    else:
                        wall_construction[values["Style"]] = values[act[4]]
                else:
                    if act[1] in activities:
                        activities[act[1]] += values[act[4]] * values[act[0]]
                    else:
                        activities[act[1]] = values[act[4]] * values[act[0]]
    # fill the activity dictionaries for slabs
    for id, values in slab_dict.items():
        weight = 0
        if "Unit weight" in values and "Volume" in values:
            weight = values["Unit weight"] * values["Volume"]
        for act in slab_demolition_activities:
            if act[0] in values:
                activities["Demolizioni"] = True
                # [3] selects style mode, [4] selects parameter
                if act[3]:
                    if values["Style"] in slab_demolition:
                        slab_demolition[values["Style"]] += values[act[4]]
                    else:
                        slab_demolition[values["Style"]] = values[act[4]]
                else:
                    if act[1] in activities:
                        activities[act[1]] += values[act[4]] * values[act[0]]
                    else:
                        activities[act[1]] = values[act[4]] * values[act[0]]
        for act in transportation_activities:
            if act[0] in values:
                activities["Trasporti"] = True
                if act[1] in activities:
                    activities[act[1]] += weight
                else:
                    activities[act[1]] = weight
        for act in slab_construction_activities:
            if act[0] in values:
                activities["Ricostruzioni"] = True
                # [3] selects style mode, [4] selects parameter
                if act[3]:
                    if values["Style"] in slab_construction:
                        slab_construction[values["Style"]] += values[act[4]]
                    else:
                        slab_construction[values["Style"]] = values[act[4]]
                else:
                    if act[1] in activities:
                        activities[act[1]] += values[act[4]] * values[act[0]]
                    else:
                        activities[act[1]] = values[act[4]] * values[act[0]]
    #Get the filename to create
    filename = rs.SaveFileName("Save Bill of Quantities file as", filter)
    if( filename==None ): return
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile,  delimiter=',')
        csvwriter.writerow(["Num", "Descrizione", "u.m.", "Qt.", "p.u.", "Importo"])
        if "Demolizioni" in activities:
            csvwriter.writerow(["", "Demolizioni"])
        if wall_demolition:
            csvwriter.writerow(["", "Demolizioni murarie"])
        for wall, area in wall_demolition.items():
            csvwriter.writerow(["", wall, "mq", area])
        for act in wall_demolition_activities:
            if act[1] in activities:
                csvwriter.writerow(["", act[2], "mq", activities[act[1]]])
        if slab_demolition:
            csvwriter.writerow(["", "Demolizioni solai"])
        for slab, area in slab_demolition.items():
            csvwriter.writerow(["", slab, "mq", area])
        for act in slab_demolition_activities:
            if act[1] in activities:
                csvwriter.writerow(["", act[2], "mq", activities[act[1]]])
        if "Trasporti" in activities:
            csvwriter.writerow(["", "Trasporti"])
        for act in transportation_activities:
            if act[1] in activities:
                csvwriter.writerow(["", act[2], "kg", activities[act[1]]])
        if "Ricostruzioni" in activities:
            csvwriter.writerow(["", "Ricostruzioni"])
        if wall_construction:
            csvwriter.writerow(["", "Ricostruzioni murarie"])
        for wall, area in wall_construction.items():
            csvwriter.writerow(["", wall, "mq", area])
        for act in wall_construction_activities:
            if act[1] in activities:
                csvwriter.writerow(["", act[2], "mq", activities[act[1]]])
        if slab_construction:
            csvwriter.writerow(["", "Ricostruzioni solai"])
        for slab, area in slab_construction.items():
            csvwriter.writerow(["", slab, "mq", area])
        for act in slab_construction_activities:
            if act[1] in activities:
                csvwriter.writerow(["", act[2], "mq", activities[act[1]]])
        print("Bill of Quantities written sucessfully to file")
    csvfile.close()
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
