import csv
import rhinoscriptsyntax as rs
import Rhino
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "WriteSurvey"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    #Get the filename to create
    filter = "CSV File (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.SaveFileName("Save Survey file as", filter)
    if( filename==None ): return
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile,  delimiter=',')
        for rObj in Rhino.RhinoDoc.ActiveDoc.Objects:
            if rObj.IsNormal and va.IsWall(rObj.Id):
                csvwriter.writerow([rObj.Id])
        print("Wall Ids written sucessfully to file")
    return 0
    
RunCommand(True)
