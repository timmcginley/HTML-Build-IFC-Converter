# First try to extract basic info from an IFC file and create an HTML file from this.
# This is focused on the use case of tall buildings
# The idea is that it can read the IFC and give a simple 2d representation
# This can then be used to provide feedback to the user.
# It can also be displayed on the users homepage and in their teams group.

# obviously we need to ...
import ifcopenshell

# get the IFC file
model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
# model = ifcopenshell.open("model/Office_A_20110811_optimized.ifc")
# model = ifcopenshell.open("model/F21_80_3W_Team01_Sub1.ifc")

# create an HTML file to write to
f = open("output/index.html", "w")
content=""

# variable for to store the elevation of the site
site_elevation = 0

# ---- start of standard HTML, this could probably just be read from a file.

# ADD HTML
content+="<html>\n"

# ADD HEAD
content+="\t<head>\n"
content+="\t\t<link rel='stylesheet' href='css/html-build.css'></link>\n"
content+="\t\t<!--- put some links in here...--->\n"
content+="\t</head>\n"

# ADD BODY
content+="\t<body>\n"

# ---- end of standard HTML

# ---- start of custom HTML entities

# ADD PROJECT
project = model.by_type('IfcProject')[0]
content+="\t\t<project- name=\"{d}\">\n".format(d=project.LongName)
# it looks like it would make sense to use the DOM here and append stuff to it...

# ADD SITE
site = model.by_type('IfcSite')[0]
site_elevation = site.RefElevation
content+="\t\t\t<site- lat=\"{}\" long=\"{}\" elev=\"{}\">\n".format(site.RefLatitude,site.RefLongitude,site_elevation )

# ADD BUILDING
content+="\t\t\t\t<building->\n"

# ADD CORE - I know its not normal,  but I think it might be useful...
content+="\t\t\t\t\t<core->\n"

# ADD FLOOR(S)
floors = model.by_type('IfcBuildingStorey')
floors.sort(key=lambda x: x.Elevation, reverse=True)

for floor in floors:
    # check if floor is lower than elevation...
    # TODO: we need to sort these, IFC doesn't do it automatically...
    
    

    if (site_elevation == floor.Elevation):
        content+="\t\t\t\t\t\t<floor- class=\"floor_ground\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)
    elif (site_elevation < floor.Elevation):
        content+="\t\t\t\t\t\t<floor- class=\"floor_upper\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)
    else:
        content+="\t\t\t\t\t\t<floor- class=\"floor_lower\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)


# CLOSE IT ALL
content+="\t\t\t\t\t</core->\n"
content+="\t\t\t\t</building->\n"
content+="\t\t\t</site->\n"
content+="\t\t</project->\n"
content+="\t</body>\n"
content+="</html>\n"

# WRITE IT OUT
f.write(content)
f.close()

# TELL EVERYONE ABOUT IT
print("html build complete")

