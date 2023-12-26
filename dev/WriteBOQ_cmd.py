import csv
import rhinoscriptsyntax as rs

__commandname__ = "WriteBOQ"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    #prompt the user for a file to import
    filter = "CSV file (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.OpenFileName("Open Wall Table File", filter)
    if not filename: return
 
    with open(filename) as csvfile:
        wall_list = []
        original = csv.DictReader(csvfile)
        for row in original:
            wall_list.append({
                "ID": row["\xef\xbb\xbfDescription"],
                "Style": row["Style"],
                "Length": row["Length"],
                "Area": float(row["Area"].split(" ")[0]),
                "Volume": float(row["Volume"].split(" ")[0]),
            })
    csvfile.close()
    print(wall_list)
    return 0
  
if __name__ == "__main__":
    RunCommand(True)
