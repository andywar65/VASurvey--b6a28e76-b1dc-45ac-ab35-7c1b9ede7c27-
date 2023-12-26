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
    print(wall_dict)
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
