# First try to extract basic info from an IFC file and create an HTML file from this.
# This is focused on the use case of tall buildings
# The idea is that it can read the IFC and give a simple 2d representation
# This can then be used to provide feedback to the user.
# It can also be displayed on the users homepage and in their teams group.

# obviously we need to ...
import ifcopenshell
import HTMLBuild as hb
import os.path

def modelLoader(name):
    # get the IFC file
    # model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
    # model = ifcopenshell.open("model/Office_A_20110811_optimized.ifc")
    
    model_url = "model/"+name+".ifc"

    if (os.path.exists(model_url)):
        model = ifcopenshell.open(model_url)
        hb.writeHTML(model)
    else:
        print("\nERROR: please check your model folder : " +model_url+" does not exist")

modelLoader("duplex")