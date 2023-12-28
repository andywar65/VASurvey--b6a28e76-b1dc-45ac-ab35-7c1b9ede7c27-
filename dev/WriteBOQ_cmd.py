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
        if "Spicconatura" in values:
            activities["Demolizioni"] = True
            if "Spicconature" in activities:
                activities["Spicconature"] += values["Area"] * values["Spicconatura"]
            else:
                activities["Spicconature"] = values["Area"] * values["Spicconatura"]
        if "Raschiatura" in values:
            activities["Demolizioni"] = True
            if "Raschiature" in activities:
                activities["Raschiature"] += values["Area"] * values["Raschiatura"]
            else:
                activities["Raschiature"] = values["Area"] * values["Raschiatura"]
        if "Rimozione rivestimento" in values:
            activities["Demolizioni"] = True
            if "Rimozioni rivestimento" in activities:
                activities["Rimozioni rivestimento"] += values["Area"] * values["Rimozione rivestimento"]
            else:
                activities["Rimozioni rivestimento"] = values["Area"] * values["Rimozione rivestimento"]
        if "Scarriolatura" in values:
            activities["Trasporti"] = True
            if "Scarriolature" in activities:
                activities["Scarriolature"] += weight
            else:
                activities["Scarriolature"] = weight
        if "Tiro" in values:
            if "Tiri" in activities:
                activities["Tiri"] += weight
            else:
                activities["Tiri"] = weight
        if "Trasporto a discarica" in values:
            if "Trasporti a discarica" in activities:
                activities["Trasporti a discarica"] += weight
            else:
                activities["Trasporti a discarica"] = weight
        if "Oneri di discarica" in values:
            if "Oneri di discarica" in activities:
                activities["Oneri di discarica"] += weight
            else:
                activities["Oneri di discarica"] = weight
        if "Ricostruzione" in values:
            activities["Ricostruzioni"] = True
            if values["Style"] in wall_construction:
                wall_construction[values["Style"]] += values["Area"]
            else:
                wall_construction[values["Style"]] = values["Area"]
        if "Intonacatura" in values:
            activities["Ricostruzioni"] = True
            if "Intonacature" in activities:
                activities["Intonacature"] += values["Area"] * values["Intonacatura"]
            else:
                activities["Intonacature"] = values["Area"] * values["Intonacatura"]
        if "Rasatura" in values:
            activities["Ricostruzioni"] = True
            if "Rasature" in activities:
                activities["Rasature"] += values["Area"] * values["Rasatura"]
            else:
                activities["Rasature"] = values["Area"] * values["Rasatura"]
        if "Imprimitura" in values:
            activities["Ricostruzioni"] = True
            if "Imprimiture" in activities:
                activities["Imprimiture"] += values["Area"] * values["Imprimitura"]
            else:
                activities["Imprimiture"] = values["Area"] * values["Imprimitura"]
        if "Tinteggiatura" in values:
            activities["Ricostruzioni"] = True
            if "Tinteggiature" in activities:
                activities["Tinteggiature"] += values["Area"] * values["Tinteggiatura"]
            else:
                activities["Tinteggiature"] = values["Area"] * values["Tinteggiatura"]
        if "Verniciatura" in values:
            activities["Ricostruzioni"] = True
            if "Verniciature" in activities:
                activities["Verniciature"] += values["Area"] * values["Verniciatura"]
            else:
                activities["Verniciature"] = values["Area"] * values["Verniciatura"]
        if "Rivestimento" in values:
            activities["Ricostruzioni"] = True
            if "Rivestimenti" in activities:
                activities["Rivestimenti"] += values["Area"] * values["Rivestimento"]
            else:
                activities["Rivestimenti"] = values["Area"] * values["Rivestimento"]
    print(activities)
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
        if "Spicconature" in activities:
            csvwriter.writerow(["", "Spicconature intonaco", "mq", activities["Spicconature"]])
        if "Raschiature" in activities:
            csvwriter.writerow(["", "Raschiature tinta", "mq", activities["Raschiature"]])
        if "Rimozioni rivestimento" in activities:
            csvwriter.writerow(["", "Rimozioni rivestimento", "mq", activities["Rimozioni rivestimento"]])
        if "Trasporti" in activities:
            csvwriter.writerow(["", "Trasporti"])
        if "Scarriolature" in activities:
            csvwriter.writerow(["", "Scarriolature", "kg", activities["Scarriolature"]])
        if "Tiri" in activities:
            csvwriter.writerow(["", "Tiri in alto/cali in basso", "kg", activities["Tiri"]])
        if "Trasporti a discarica" in activities:
            csvwriter.writerow(["", "Trasporti a discarica", "kg", activities["Trasporti a discarica"]])
        if "Oneri di discarica" in activities:
            csvwriter.writerow(["", "Oneri di discarica", "kg", activities["Oneri di discarica"]])
        if "Ricostruzioni" in activities:
            csvwriter.writerow(["", "Ricostruzioni"])
        if wall_construction:
            csvwriter.writerow(["", "Ricostruzioni murarie"])
        for wall, area in wall_construction.items():
            csvwriter.writerow(["", wall, "mq", area])
        if "Intonacature" in activities:
            csvwriter.writerow(["", "Intonacature", "mq", activities["Intonacature"]])
        if "Rasature" in activities:
            csvwriter.writerow(["", "Rasature", "mq", activities["Rasature"]])
        if "Imprimiture" in activities:
            csvwriter.writerow(["", "Imprimiture", "mq", activities["Imprimiture"]])
        if "Tinteggiature" in activities:
            csvwriter.writerow(["", "Tinteggiature", "mq", activities["Tinteggiature"]])
        if "Verniciature" in activities:
            csvwriter.writerow(["", "Verniciature", "mq", activities["Verniciature"]])
        if "Rivestimenti" in activities:
            csvwriter.writerow(["", "Rivestimenti murari", "mq", activities["Rivestimenti"]])
        print("Bill of Quantities written sucessfully to file")
    csvfile.close()
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
