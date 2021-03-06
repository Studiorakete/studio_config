# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.
import shutil
import maya.cmds as cmds

import os
import maya.cmds as cmds

import tank
from tank import Hook
from tank import TankError

class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """
	
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       A list of any items that were found to be published.  
                        Each item in the list should be a dictionary containing 
                        the following keys:
                        {
                            type:   String
                                    This should match a scene_item_type defined in
                                    one of the outputs in the configuration and is 
                                    used to determine the outputs that should be 
                                    published for the item
                                    
                            name:   String
                                    Name to use for the item in the UI
                            
                            description:    String
                                            Description of the item to use in the UI
                                            
                            selected:       Bool
                                            Initial selected state of item in the UI.  
                                            Items are selected by default.
                                            
                            required:       Bool
                                            Required state of item in the UI.  If True then
                                            item will not be deselectable.  Items are not
                                            required by default.
                                            
                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """
                
        items = []
        
        # get the main scene:
        scene_name = cmds.file(query=True, sn=True)
        if not scene_name:
            print "hello"
            #cmds.confirmDialog(t="test",m="hello",b="okdoki")
            #raise TankError("Please Save your file before Publishing")
        
        scene_path = os.path.abspath(scene_name)
        name = os.path.basename(scene_path)
        
        # create the primary item - this will match the primary output 'scene_item_type':            
        items.append({"type": "work_file", "name": name})
        
        # Deselect all
        cmds.select(deselect=True)
        # look for root level groups that have meshes as children:
        #for grp in cmds.ls("*:alembic", long=True):
            # Use selection to get all the children of "Alembic" objectset
        locators = cmds.ls(type='locator', l=False)
        #cmds.select(grp, hierarchy=True, add=True)
            # Get only the selected items. (if necessary take only certain types to export!)
        sel=cmds.ls(selection=True, showType=True)
            
        for loc in locators:
            #if cmds.ls(s, type="mesh"):
            if 'PRP' in loc:
                #items.append({"type":"mesh_group", "name":grp})
                items.append(loc[:-5])
                print loc
                break
        
        cmds.select(deselect=True)			
        
        return items
        
        