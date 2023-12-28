import csv
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va
import Rhino
import rhinoscriptsyntax as rs

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
    wall_params = [
        "Unit weight",
        "Demolizione",
        "Spicconatura",
        "Raschiatura",
        "Rimozione rivestimento",
        "Scarriolatura",
        "Tiro",
        "Trasporto a discarica",
        "Oneri di discarica",
        "Ricostruzione",
        "Intonacatura",
        "Rasatura",
        "Imprimitura",
        "Tinteggiatura",
        "Verniciatura",
        "Rivestimento",
    ]
    # get all objects in file
    objects = Rhino.RhinoDoc.ActiveDoc.Objects
    for obj in objects:
        # filter walls
        if obj.IsNormal and va.IsWall(obj.Id):
            # add parameters to wall dictionary
            for param in wall_params:
                param_id = va.GetObjectParameterId(param, obj.Id,1)
                value = va.GetParameterValue(param_id, obj.Id)
                type = va.GetParameterType(param_id)
                if value:
                    wall_dict[str(obj.Id)][param] = value
    # write BOQ dictionary
    activities = {}
    wall_demolition = {}
    wall_construction = {}
    wall_demolition_activities = [
        ("Spicconatura", "Spicconatura", "Spicconatura intonaco"),
        ("Raschiatura", "Raschiatura", "Raschiatura tinta"),
        ("Rimozione rivestimento", "Rimozione rivestimento", "Rimozione rivestimento"),
    ]
    transportation_activities = [
        ("Scarriolatura", "Scarriolatura", "Scarriolatura nell'ambito del cantiere"),
        ("Tiro", "Tiri", "Tiro in alto/calo in basso"),
        ("Trasporto a discarica", "Trasporto a discarica", "Trasporto a discarica"),
        ("Oneri di discarica", "Oneri di discarica", "Oneri di discarica"),
    ]
    wall_construction_activities = [
        ("Intonacatura", "Intonacatura", "Intonacatura"),
        ("Rasatura", "Rasatura", "Rasatura"),
        ("Imprimitura", "Imprimitura", "Imprimitura"),
        ("Tinteggiatura", "Tinteggiatura", "Tinteggiatura"),
        ("Verniciatura", "Verniciatura", "Verniciatura"),
        ("Rivestimento", "Rivestimento", "Rivestimento murario"),
    ]
    for id, values in wall_dict.items():
        weight = 0
        if "Unit weight" in values and "Volume" in values:
            weight = values["Unit weight"] * values["Volume"]
        if "Demolizione" in values:
            activities["Demolizioni"] = True
            if values["Style"] in wall_demolition:
                wall_demolition[values["Style"]] += values["Area"]
            else:
                wall_demolition[values["Style"]] = values["Area"]
        for act in wall_demolition_activities:
            if act[0] in values:
                activities["Demolizioni"] = True
                if act[1] in activities:
                    activities[act[1]] += values["Area"] * values[act[0]]
                else:
                    activities[act[1]] = values["Area"] * values[act[0]]
        for act in transportation_activities:
            if act[0] in values:
                activities["Trasporti"] = True
                if act[1] in activities:
                    activities[act[1]] += weight
                else:
                    activities[act[1]] = weight
        if "Ricostruzione" in values:
            activities["Ricostruzioni"] = True
            if values["Style"] in wall_construction:
                wall_construction[values["Style"]] += values["Area"]
            else:
                wall_construction[values["Style"]] = values["Area"]
        for act in wall_construction_activities:
            if act[0] in values:
                activities["Ricostruzioni"] = True
                if act[1] in activities:
                    activities[act[1]] += values["Area"] * values[act[0]]
                else:
                    activities[act[1]] = values["Area"] * values[act[0]]
    #Get the filename to create
    filter = "CSV File (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
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
        print("Bill of Quantities written sucessfully to file")
    csvfile.close()
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
