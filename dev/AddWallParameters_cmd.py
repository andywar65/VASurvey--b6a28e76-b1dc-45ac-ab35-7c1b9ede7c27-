import clr
clr.AddReference("VisualARQ.Script")
import VisualARQ.Script as va

__commandname__ = "AddWallParameters"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    wall_styles = va.GetAllWallStyleIds()
    parameters = [
            ["Unit weight", va.ParameterType.Number, "Physical", "Unit weight of wall (kg/mc)"],
            ["Demolizione", va.ParameterType.Boolean, "Demolizioni", "Demolizione totale del muro, al mq"],
            ["Spicconatura", va.ParameterType.Percentage, "Demolizioni", "Spicconatura dell'intonaco al mq (100% = una faccia)"],
            ["Raschiatura", va.ParameterType.Percentage, "Demolizioni", "Raschiatura della tinteggiatura al mq (100% = una faccia)"],
            ["Rimozione rivestimento", va.ParameterType.Percentage, "Demolizioni", "Rimozione del rivestimento al mq (100% = una faccia)"],
            ["Scarriolatura", va.ParameterType.Boolean, "Trasporti", "Scarriolatura del muro demolito, al kg"],
            ["Tiro", va.ParameterType.Boolean, "Trasporti", "Tiro in alto o calo in basso del muro demolito, al kg"],
            ["Trasporto a discarica", va.ParameterType.Boolean, "Trasporti", "Carico e trasporto a discarica del muro demolito, al kg"],
            ["Oneri di discarica", va.ParameterType.Boolean, "Trasporti", "Smaltimento in discarica del muro demolito, al kg"],
            ["Ricostruzione", va.ParameterType.Boolean, "Ricostruzioni", "Costruzione da zero del muro, al mq"],
            ["Intonacatura", va.ParameterType.Percentage, "Ricostruzioni", "Intonacatura del muro al mq (100% = una faccia)"],
            ["Rasatura", va.ParameterType.Percentage, "Ricostruzioni", "Rasatura del muro al mq (100% = una faccia)"],
            ["Imprimitura", va.ParameterType.Percentage, "Ricostruzioni", "Imprimitura del muro al mq (100%=una faccia)"],
            ["Tinteggiatura", va.ParameterType.Percentage, "Ricostruzioni", "Tinteggiatura del muro al mq (100%=una faccia)"],
            ["Verniciatura", va.ParameterType.Percentage, "Ricostruzioni", "Verniciatura a smalto del muro al mq (100%=una faccia)"],
            ["Rivestimento", va.ParameterType.Percentage, "Ricostruzioni", "Rivestimento del muro al mq (100%=una faccia)"],
		]
    for w_style in wall_styles:
        for p in parameters:
			va.AddObjectParameter( w_style, p[0], p[1], p[2], p[3])
    return 0
    
if __name__ == "__main__":
    RunCommand(True)
