import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "AddConstructionParameters"

physical_parameters = [
    ["Unit weight", va.ParameterType.Number, "Physical", "Unit weight of wall (kg/mc)"],
]
wall_demolition_parameters = [
    ["010-Demolizione", va.ParameterType.Boolean, "Demolizioni", "Demolizione totale muraria", True],
    ["020-Spicconatura", va.ParameterType.Percentage, "Demolizioni", "Spicconatura dell'intonaco murario", False],
    ["030-Raschiatura", va.ParameterType.Percentage, "Demolizioni", "Raschiatura della tinteggiatura muraria", False],
    ["040-Rimozione rivestimento", va.ParameterType.Percentage, "Demolizioni", "Rimozione del rivestimento murario", False],
]
transportation_parameters = [
    ["010-Scarriolatura", va.ParameterType.Boolean, "Trasporti", "Scarriolatura dei materiali demoliti"],
    ["020-Tiro", va.ParameterType.Boolean, "Trasporti", "Tiro in alto o calo in basso dei materiali demoliti"],
    ["030-Trasporto a discarica", va.ParameterType.Boolean, "Trasporti", "Carico e trasporto a discarica dei materiali demoliti"],
    ["040-Oneri di discarica", va.ParameterType.Boolean, "Trasporti", "Smaltimento in discarica dei materiali demoliti"],
]
wall_construction_parameters = [
    ["010-Ricostruzione", va.ParameterType.Boolean, "Ricostruzioni", "Costruzioni murarie", True],
    ["020-Intonacatura", va.ParameterType.Percentage, "Ricostruzioni", "Intonacatura muraria", False],
    ["030-Rasatura", va.ParameterType.Percentage, "Ricostruzioni", "Rasatura muraria", False],
    ["040-Imprimitura", va.ParameterType.Percentage, "Ricostruzioni", "Imprimitura muraria con aggrappante", False],
    ["050-Tinteggiatura", va.ParameterType.Percentage, "Ricostruzioni", "Tinteggiatura muraria con lavabile", False],
    ["060-Verniciatura", va.ParameterType.Percentage, "Ricostruzioni", "Verniciatura muraria a smalto", False],
    ["070-Rivestimento", va.ParameterType.Percentage, "Ricostruzioni", "Rivestimento murario", False],
]

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    wall_styles = va.GetAllWallStyleIds()
    for w_style in wall_styles:
        for p in physical_parameters:
            va.AddObjectParameter( w_style, p[0], p[1], p[2], p[3])
        for p in wall_demolition_parameters:
            va.AddObjectParameter( w_style, p[0], p[1], p[2], p[3])
        for p in transportation_parameters:
            va.AddObjectParameter( w_style, p[0], p[1], p[2], p[3])
        for p in wall_construction_parameters:
            va.AddObjectParameter( w_style, p[0], p[1], p[2], p[3])
    return 0
    
if __name__ == "__main__":
    RunCommand(True)
