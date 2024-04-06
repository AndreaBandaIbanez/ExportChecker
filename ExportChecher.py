<?xml version="1.0" encoding="UTF-8"?>
<shelfDocument>
  <!-- This file contains definitions of shelves, toolbars, and tools.
 It should not be hand-edited when it is being used by the application.
 Note, that two definitions of the same element are not allowed in
 a single file. -->
</shelfDocument>
def set_node_color(node, color):
    """
    set the color of a node.
    
    :param node: Node to be changed
    :type node: hou.Node
    
    :param color: color to be applied
    :type color: tuple
    """
    node.setColor(hou.Color(color))
    
def get_asset_type():
    """
    get the asset type from the current node's parameter.
    
    :return: asset type as a string.
    :rtype: str
    """
    return hou.pwd().parm("assettype").evalAsString()

def check_attributes():
    """
    check attributes based on the asset type.
    """
    geo = hou.pwd().geometry()
    asset_type = get_asset_type()
    
    if asset_type == "Pyro":
        prims = geo.prims()

        prim_names = []
        for prim in prims:
            name = prim.attribValue("name")
            prim_names.append(name)

        if ("density" in prim_names and "temperature" in prim_names and
            all(f"vel.{axis}" in prim_names for axis in ["x", "y", "z"])): 
            set_node_color(hou.pwd(), (0, 1, 0))
            hou.ui.displayMessage("Everything correct, you can export.")
        else:
            set_node_color(hou.pwd(), (1, 0, 0))
            hou.ui.displayMessage("You are missing 'density', 'temperature', "
             "or 'vel' attributes.",
             severity=hou.severityType.Warning)

    elif asset_type == "Cloth": 
        
        if geo.findVertexAttrib("uv"):
            set_node_color(hou.pwd(), (0, 1, 0))
            hou.ui.displayMessage("Everything correct, you can export.")
        else:
            set_node_color(hou.pwd(), (1, 0, 0))
            hou.ui.displayMessage("You are missing the 'uv' attribute.", 
                                severity=hou.severityType.Warning)

    elif asset_type == "Particles":  
        
        if geo.findPointAttrib("P") and geo.findPointAttrib("id"):
            set_node_color(hou.pwd(), (0, 1, 0)) 
            hou.ui.displayMessage("Everything correct, you can export.")
        else:
            set_node_color(hou.pwd(), (1, 0, 0))
            hou.ui.displayMessage("You are missing the 'P' or 'id' attribute.", 
                                severity=hou.severityType.Warning)
