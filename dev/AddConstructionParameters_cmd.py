import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "AddConstructionParameters"

# Name, Type, Category, Description, select style, measuring parameter
physical_parameters = [
    ["Unit weight", va.ParameterType.Number, "Physical", "Unit weight of wall (kg/mc)"],
]
wall_demolition_parameters = [
    ["010-Demolizione", va.ParameterType.Boolean, "Demolizioni", "Demolizione totale muraria", True, "Area"],
    ["020-Spicconatura", va.ParameterType.Percentage, "Demolizioni", "Spicconatura dell'intonaco murario", False, "Area"],
    ["030-Raschiatura", va.ParameterType.Percentage, "Demolizioni", "Raschiatura della tinteggiatura muraria", False, "Area"],
    ["040-Rimozione rivestimento", va.ParameterType.Percentage, "Demolizioni", "Rimozione del rivestimento murario", False, "Area"],
    ["050-Rimozione battiscopa", va.ParameterType.Percentage, "Demolizioni", "Rimozione del battiscopa", False, "Length"],
]
transportation_parameters = [
    ["010-Scarriolatura", va.ParameterType.Boolean, "Trasporti", "Scarriolatura dei materiali demoliti"],
    ["020-Tiro", va.ParameterType.Boolean, "Trasporti", "Tiro in alto o calo in basso dei materiali demoliti"],
    ["030-Trasporto a discarica", va.ParameterType.Boolean, "Trasporti", "Carico e trasporto a discarica dei materiali demoliti"],
    ["040-Oneri di discarica", va.ParameterType.Boolean, "Trasporti", "Smaltimento in discarica dei materiali demoliti"],
]
wall_construction_parameters = [
    ["010-Ricostruzione", va.ParameterType.Boolean, "Ricostruzioni", "Costruzioni murarie", True, "Area"],
    ["020-Intonacatura", va.ParameterType.Percentage, "Ricostruzioni", "Intonacatura muraria", False, "Area"],
    ["030-Rasatura", va.ParameterType.Percentage, "Ricostruzioni", "Rasatura muraria", False, "Area"],
    ["040-Imprimitura", va.ParameterType.Percentage, "Ricostruzioni", "Imprimitura muraria con aggrappante", False, "Area"],
    ["050-Tinteggiatura", va.ParameterType.Percentage, "Ricostruzioni", "Tinteggiatura muraria con lavabile", False, "Area"],
    ["060-Verniciatura", va.ParameterType.Percentage, "Ricostruzioni", "Verniciatura muraria a smalto", False, "Area"],
    ["070-Rivestimento", va.ParameterType.Percentage, "Ricostruzioni", "Rivestimento murario", False, "Area"],
    ["080-Battiscopa", va.ParameterType.Percentage, "Ricostruzioni", "Posa del battiscopa", False, "Length"],
]
slab_demolition_parameters = [
    ["010-Rimozione pavimento", va.ParameterType.Boolean, "Demolizioni", "Rimozione della pavimentazione", True, "Area"],
    ["020-Demolizione massetto", va.ParameterType.Boolean, "Demolizioni", "Demolizione del massetto fino a 6 cm", False, "Area"],
]
slab_construction_parameters = [
    ["010-Massetto", va.ParameterType.Boolean, "Ricostruzioni", "Massetto sabbia e cemento", False, "Area"],
    ["020-Massetto premiscelato", va.ParameterType.Boolean, "Ricostruzioni", "Massetto premiscelato", False, "Area"],
    ["030-Autolivellante", va.ParameterType.Boolean, "Ricostruzioni", "Autolivellante", False, "Area"],
    ["040-Pavimentazione", va.ParameterType.Boolean, "Ricostruzioni", "Posa della pavimentazione", True, "Area"],
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
    slab_styles = va.GetAllSlabStyleIds()
    for s_style in slab_styles:
        for p in physical_parameters:
            va.AddObjectParameter( s_style, p[0], p[1], p[2], p[3])
        for p in slab_demolition_parameters:
            va.AddObjectParameter( s_style, p[0], p[1], p[2], p[3])
        for p in transportation_parameters:
            va.AddObjectParameter( s_style, p[0], p[1], p[2], p[3])
        for p in slab_construction_parameters:
            va.AddObjectParameter( s_style, p[0], p[1], p[2], p[3])
    return 0
    
if __name__ == "__main__":
    RunCommand(True)
