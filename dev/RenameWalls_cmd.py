import Rhino
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "RenameWalls"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    for obj in Rhino.RhinoDoc.ActiveDoc.Objects:
        if obj.IsNormal:
            if va.IsWall(obj.Id) or va.IsSlab(obj.Id):
                va.SetObjectDescription(obj.Id, str(obj.Id))
    return 0
    
if __name__ == "__main__":
    RunCommand(True)
