''' written by Tim McGinley 2022 '''

import ifcopenshell
import os.path
import time

def modelLoader(name):

    ''' 
        load the IFC file 
    '''
    
    model_url = "model/"+name+".ifc"
    start_time = time.time()

    if (os.path.exists(model_url)):
        model = ifcopenshell.open(model_url)
        print("\n\tFile    : {}.ifc".format(name))
        print("\tLoad    : {:.2f}s".format(float(time.time() - start_time)))
        
        start_time = time.time()
        writeHTML(model,name)
        print("\tConvert : {:.4f}s".format(float(time.time() - start_time)))
        
    else:
        print("\nERROR: please check your model folder : " +model_url+" does not exist")

def writeHTML(model,name):

    ''' 
        write the HTML entities 
    '''
    
    # parent directory - put in setting file?
    parent_dir = "output/"
    # create an HTML file to write to
    if (os.path.exists("output/"+name))==False:
        path = os.path.join(parent_dir, name)
        os.mkdir(path)
    
    f_loc="output/"+name+"/index.html"
    f = open(f_loc, "w")
    cont=""
    
    # ---- start of standard HTML
    cont+=0*"\t"+"<HTML>\n"
    # ---- add HEAD
    cont+=1*"\t"+"<HEAD>\n"
    # ---- add HTMLBUILD CSS - could add others here :)
    cont+=2*"\t"+"<LINK rel='stylesheet' href='../css/html-build.css'></LINK>\n"
    # ---- add HTMLBUILD JS
    cont+=2*"\t"+"<SCRIPT src='../js/html-build.js'></SCRIPT>\n"
    # ---- JQUERY - it would be crazy not to
    cont+=2*"\t"+"<SCRIPT src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.js'></SCRIPT>\n"
    # ---- close HEAD
    cont+=1*"\t"+"</HEAD>\n"
    # ---- add BODY
    cont+=1*"\t"+"<BODY onload=\"main()\">\n"  
    
    # ---- add CUSTOM HTML for the BUILDING here
    cont+=writeCustomHTML(model)
    
    # ---- close BODY AND HTML ENTITIES
    cont+=1*"\t"+"</BODY>\n"   
    cont+=0*"\t"+"</HTML>\n"

    # ---- write it out
    f.write(cont)
    f.close()

    # ---- tell everyone about it
    print("\tSave    : "+f_loc)

def writeCustomHTML(model):

    ''' 
        write the custom HTML entities 
    '''
    
    custom=""
    site_elev = 0 # variable to store the elevation of the site
    
    # ---- define the MODEL
    
    custom+=2*"\t"+"<model->\n"
    
    # ---- add PROJECT custom entity
    project = model.by_type('IfcProject')[0]
    custom+=3*"\t"+"<project- name=\"{d}\">\n".format(d=project.LongName)
    # it looks like it would make sense to use the DOM here and append stuff to it...
    
    # ---- add SITE custom entity
    site = model.by_type('IfcSite')[0]
    site_elev = site.RefElevation
    custom+=4*"\t"+"<site- lat=\"{}\" long=\"{}\" elev=\"{}\">\n".format(site.RefLatitude,site.RefLongitude,site_elev )

    # ---- add BUILDING custom entity
    custom+=5*"\t"+"<building->\n"
    
    # ---- add FLOOR custom entity
    floors = model.by_type('IfcBuildingStorey')
    floors.sort(key=lambda x: x.Elevation, reverse=True)
   
    # ---- classify FLOOR as LOWER, GROUND OR UPPER and write to custom entities
    custom+= classifyFloors(floors,site_elev)
    
    # ---- close BUILDING, SITE and PROJECT
    custom+=5*"\t"+"</building->\n"
    custom+=4*"\t"+"</site->\n"
    custom+=3*"\t"+"</project->\n"
    
    # ---- close MODEL custom entity
    custom+=2*"\t"+"</model->\n"
    
    # ---- add VIEW
    custom+=2*"\t"+"<view->\n"
    
    # ---- add PLAN.
    custom+=3*"\t"+"<plan-></plan->\n"
    
    # ---- add PROPERTIES etc..
    custom+=3*"\t"+"<props-></props->\n"
    
    # ---- close VIEW
    custom+=2*"\t"+"</view->\n"
    
    # ---- return the CUSTOM HTML
    return custom

def classifyFloors(floors,site_elev):

    '''
    another way after arranging them would be to split them into above and below ground floor sets.
    '''
    
    floor_entities = ''
    
    # these are interesting and probably should be output somwhere - maybe to the building data?
    lower_floors = sum(f.Elevation < 0.1 for f in floors)
    level = len(floors)-lower_floors
    
    for floor in floors:
        # check if floor is lower than elevation...
        type = "floor_upper"
        if ( site_elev-.1 <= floor.Elevation <= site_elev+.1):
            type = "floor_ground"
        elif (site_elev < floor.Elevation):
            type = "floor_upper"
        else:
            type = "floor_lower"
           
        # Tthe span stuff should be dealt with in JS...
        
        floor_entities+=6*"\t"+"<floor- class=\""+type+"\" name='{}'  level='{}' elev=\"{}\" >{}<span class=\"floor_stats\">{}</span> </floor->\n".format(floor.Name, level, floor.Elevation,floor.Name, round(float(floor.Elevation),3))     
        level-=1
        if (type == "floor_ground"):
            floor_entities+=6*"\t"+"<ground-></ground->\n"
            
    return floor_entities
