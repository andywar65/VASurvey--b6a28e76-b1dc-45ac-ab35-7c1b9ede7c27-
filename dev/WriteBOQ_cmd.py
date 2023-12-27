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
        if "Scarriolatura" in values:
            activities["Scarriolature"] += weight
        if "Tiro" in values:
            activities["Tiro in alto/calo in basso"] += weight
        if "Trasporto a discarica" in values:
            activities["Trasporto a discarica"] += weight
        if "Oneri di discarica" in values:
            activities["Oneri di discarica"] += weight
    print(activities)
    print(wall_demolition)
    #Get the filename to create
    filter = "CSV File (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.SaveFileName("Save Bill of Quantities file as", filter)
    if( filename==None ): return
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile,  delimiter=',')
        csvwriter.writerow(["Num", "Descrizione", "u.m.", "Qt.", "p.u.", "Importo"])
        if activities["Demolizioni"]:
            csvwriter.writerow(["", "Demolizioni", "", "", "", ""])
        print("Bill of Quantities written sucessfully to file")
    csvfile.close()
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
