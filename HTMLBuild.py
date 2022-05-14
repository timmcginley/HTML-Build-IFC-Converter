import ifcopenshell
import os.path

def modelLoader(name):
    # get the IFC file
    # model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
    # model = ifcopenshell.open("model/Office_A_20110811_optimized.ifc")
    
    model_url = "model/"+name+".ifc"

    if (os.path.exists(model_url)):
        model = ifcopenshell.open(model_url)
        writeHTML(model)
    else:
        print("\nERROR: please check your model folder : " +model_url+" does not exist")

def writeHTML(model):
    ''' write the IFC file '''
    
    # create an HTML file to write to
    f = open("output/index.html", "w")
    
    cont=""

    # ---- START OF STANDARD HTML
    cont+=0*"\t"+"<html>\n"

    # ---- ADD HEAD
    cont+=1*"\t"+"<head>\n"
    
    # ---- ADD HTMLBUILD CSS - COULD ADD OTHERS HERE :)
    cont+=2*"\t"+"<link rel='stylesheet' href='css/html-build.css'></link>\n"
    
    # ---- CLOSE HEAD
    cont+=1*"\t"+"</head>\n"

    # ---- ADD BODY
    cont+=1*"\t"+"<body>\n"

    # ---- ADD CUSTOM HTML FOR THE BUILDING HERE
    cont+=writeCustomHTML(model)
    
    # ---- CLOSE BODY AND HTML ENTITIES
    cont+=1*"\t"+"</body>\n"
    cont+=0*"\t"+"</html>\n"

    # ---- WRITE IT OUT
    f.write(cont)
    f.close()

    # ---- TELL EVERYONE ABOUT IT
    print("\n\t--- html build file created in [location]")

def writeCustomHTML(model):

    custom=""
    site_elev = 0 # variable for to store the elevation of the site
    
    # ---- ADD PROJECT CUSTOM ENTITY
    project = model.by_type('IfcProject')[0]
    custom+=2*"\t"+"<project- name=\"{d}\">\n".format(d=project.LongName)
    # it looks like it would make sense to use the DOM here and append stuff to it...

    # ---- ADD SITE CUSTOM ENTITY
    site = model.by_type('IfcSite')[0]
    site_elev = site.RefElevation
    custom+=3*"\t"+"<site- lat=\"{}\" long=\"{}\" elev=\"{}\">\n".format(site.RefLatitude,site.RefLongitude,site_elev )

    # ---- ADD BUILDING CUSTOM ENTITY
    custom+=4*"\t"+"<building->\n"

    # ---- ADD CORE - I know its not normal,  but I think it might be useful... SO KILL IT!!!
    custom+=5*"\t"+"<core->\n"

    # ---- ADD FLOOR CUSTOM ENTITIES
    floors = model.by_type('IfcBuildingStorey')
    floors.sort(key=lambda x: x.Elevation, reverse=True)

    for floor in floors:
        # check if floor is lower than elevation...
        type = "floor_upper"
        if (site_elev == floor.Elevation):
            type = "floor_ground"
        elif (site_elev < floor.Elevation):
            type = "floor_upper"
        else:
            type = "floor_lower"
        
        custom+=6*"\t"+"<floor- class=\""+type+"\" elev=\"{}\" >{}<span class=\"floor_stats\">{}</span> </floor->\n".format(floor.Elevation,floor.Name, round(float(floor.Elevation),3))     

    # ---- CLOSE IT ALL
    custom+=5*"\t"+"</core->\n"
    custom+=4*"\t"+"</building->\n"
    custom+=3*"\t"+"</site->\n"
    custom+=2*"\t"+"</project->\n"
    
    # ---- RETURN THE CUSTOM HTML
    return custom



