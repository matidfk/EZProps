bl_info = {
    "name": "EZ Props",
    "author": "matidfk",
    "version": (0, 1, 0),
    "blender": (4, 1, 0),
    "location": "Info",
    "description": "Quick access to global user-defined props",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Interface"
}


import bpy

def draw_props(self, context):
    layout = self.layout
    region = context.region   
    
    if region.alignment == 'RIGHT':
        obj = bpy.data.objects.get("_EZProps")
        if obj:
            for key, value in obj.items():
                layout.prop(obj, f'["{key}"]', text=key)
        layout.operator("ezprops.add_prop")
        layout.separator()

class EZPROPS_OT_add_prop(bpy.types.Operator):
    bl_idname = "ezprops.add_prop"
    bl_label = "Add prop"
    bl_options = {'REGISTER', 'UNDO_GROUPED'}

    
    prop_name: bpy.props.StringProperty(default="New Prop")
    prop_type: bpy.props.EnumProperty(
        items = [
            ('BOOL', "Bool", "Bool"),
            ('FLOAT', "Float", "Float"),
            ('INT', "Int", "Int"),
            ('STRING', "String", "String"),
        ]
    )
    
    def execute(self, context):
        obj = bpy.data.objects.get("_EZProps")
        if obj is None:
            obj = bpy.data.objects.new("_EZProps", None)
            obj.use_fake_user = True

        # collection = bpy.context.view_layer.active_layer_collection.collection
        # if obj.name not in collection.objects:
        #     collection.objects.link(obj)

        values = {
            'BOOL': False,
            'FLOAT': 0.0,
            'INT': 0,
            'STRING': "",
        }
        obj[self.prop_name] = values.get(self.prop_type)
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(EZPROPS_OT_add_prop)
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_props)


def unregister():
    bpy.utils.unregister_class(EZPROPS_OT_add_prop)
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_props)
    
if __name__ == "__main__":
    register()
