import Rhino
import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "AddIdToDescription"

# This command adds object.Id to Description parameter
# Works with Walls and Slabs
def RunCommand( is_interactive ):
    for obj in Rhino.RhinoDoc.ActiveDoc.Objects:
        if obj.IsNormal:
            if va.IsWall(obj.Id) or va.IsSlab(obj.Id):
                va.SetObjectDescription(obj.Id, str(obj.Id))
    return 0
    
if __name__ == "__main__":
    RunCommand(True)
