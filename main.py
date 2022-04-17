import ifcopenshell

model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
f = open("output/index.html", "w")
content=""
# this just gets you the entity, defined here as wall
# feel free to change this to your needs

# ADD HTML
content+="<html>\n"
# ADD HEAD
content+="\t<head>\n"
content+="\t\t<link rel='stylesheet' href='css/html-build.css'></link>\n"
content+="\t\tput some links in here...\n"
content+="\t</head>\n"
# ADD BODY
content+="\t<body>\n"
# ADD PROJECT
project = model.by_type('IfcProject')[0]
content+="\t\t<project- name=\"{d}\">\n".format(d=project.LongName)
# it looks like it would make sense to use the dom here and append stuff to it...
# ADD SITE
content+="\t\t\t<site->\n"
# ADD BUILDING
content+="\t\t\t\t<building->\n"
# ADD CORE
content+="\t\t\t\t\t<core->\n"

# ADD FLOOR(S)
floors = model.by_type('IfcBuildingStorey')
for floor in floors:
    content+="\t\t\t\t\t\t<floor->{}</floor->\n".format(floor.Name)
    
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
# ###################### end of example ###########################
