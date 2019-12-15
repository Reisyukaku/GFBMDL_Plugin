# Copyright (c) 2019 Reisyukaku
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name":         "GFMDL Import/Export",
    "author":       "Rei",
    "blender":      (2,80,0),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Import-Export GFMDL data",
    "category":     "Import-Export",
    "wiki_url":     "",
    "tracker_url":  "",
}

import bpy
from bpy.props import *

# ################################################################
# Import/Export
# ################################################################
class ImportGfmdl( bpy.types.Operator ):
    bl_idname = "import.gfmdl"
    bl_label = "Import GFMDL"
    
    filepath : StringProperty(
            subtype = 'FILE_PATH',
            )
    filter_glob : StringProperty(
            default = "*.gfbmdl",
            options = {'HIDDEN'},
            )
    files : bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    directory : bpy.props.StringProperty(subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    
    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".gfbmdl")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute( self, context ):
        from .import_model import ImportModel
        return ImportModel.load( self, context )

class ExportGfmdl( bpy.types.Operator ):
    bl_idname = "export.gfmdl"
    bl_label = "Export GFMDL"
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    def invoke(self, context, event):            
        if not self.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".gfbmdl")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute( self, context ):
        print("Selected: " + context.active_object.name )
        
        from .export_model import ExportModel
        return ExportModel.save( self, context )


# ################################################################
# Common
# ################################################################

def menu_func_import( self, context ):
    self.layout.operator( ImportGfmdl.bl_idname, text="GFMDL (.gfbmdl)")
    
def menu_func_export( self, context ):
    self.layout.operator( ExportGfmdl.bl_idname, text="GFMDL (.gfbmdl)")

def register():
    print("Registering GFMDL\n")
    bpy.utils.register_class(ImportGfmdl)
    bpy.utils.register_class(ExportGfmdl)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
def unregister():
    print("Unregistering GFMDL\n")
    bpy.utils.unregister_class(ImportGfmdl)
    bpy.utils.unregister_class(ExportGfmdl)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    
if __name__ == "__main__":
    register()