# VisualARQ Survey
A VisualARQ Python plugin that generates a Bill of Quantities
## Installation
Clone the repository where your Rhinoceros Python plugins are, change the folder name so that it looks like a proper plugin folder (from `PluginName--Hash-` to `PluginName (Hash)`), restart Rhino. VisualARQ must be installed too.
## Usage
At the moment the plugin is not standing alone, it needs some VisualARQ tools to work, as you can see in the description below, I'll try to automate the process if possible.

* `AddWallParameters` script gets all wall styles and attaches "Physical" and "Construction work" parameters (numeric, boolean, percentage)
* `RenameWalls` script gets all walls and fills the "Description" parameter with the wall Id (used `SetObjectDescription` built in method)
* You have to prepare a custom Wall Table that outputs Description (wall Id), Style, Length, Area and Volume of selected walls. All these values are extracted to a CSV file (this is a standard VisualARQ procedure).
* `WriteBOQ` script picks up the CSV file generating a dictionary of all walls, then it loops through all wall objects in the document and adds parametric values to the dictionary. At the end of the process you will have a list of walls that looks like this: `[{"Wall-1":{"Style":"Wall style", "Length": length,...,"Parameter-1":value,...},{"Wall-2":{...}},...]`
* The script goes on building the Bill of Quantities, it loops in the wall list and pairs "Construction work" parameters with proper wall geometry, adding up quantities wall by wall. Results are extracted into a CSV file.

By now the plugin is limited to wall objects with several construction works.