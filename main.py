# First try to extract basic info from an IFC file and create an HTML file from this.
# This is focused on the use case of tall buildings
# The idea is that it can read the IFC and give a simple 2d representation
# This can then be used to provide feedback to the user.
# It can also be displayed on the users homepage and in their teams group.

# obviously we need to ...
import ifcopenshell
import HTMLBuild as hb

# get the IFC file
# model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
# model = ifcopenshell.open("model/Office_A_20110811_optimized.ifc")
model = ifcopenshell.open("model/21_03_01.ifc")

hb.writeHTML(model)

