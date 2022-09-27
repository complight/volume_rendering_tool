bl_info = {
    "name": "Volume Rendering Tool",
    "author": "Serhat Aksoy",
    "version": (1, 0),
    "blender": (3, 22, 0),
    "location": "View3D > Add > Mesh > VisLib",
    "description": "Volume Rendering Tool",
    "warning": "",
    "doc_url": "",
    "category": "Tool",
}
import bpy

#Cube = bpy.ops.mesh.primitive_cube_add(location = (0,0,0))

bpy.context.scene.render.engine = 'CYCLES'

def create_2d_3d_converter(image_path,color,number,default):
    new_color = [0,0,0,1]
    for i in range(len(color)):
         new_color[i] = color[i] 
    new_mat =  bpy.data.materials.new(name = 'VolumeMat')
    new_mat.use_nodes = True
    new_mat.node_tree.nodes.remove(new_mat.node_tree.nodes['Principled BSDF'])
    new_mat.node_tree.nodes.remove(new_mat.node_tree.nodes['Material Output'])
    image_num_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeValue')
    image_num_node.outputs[0].default_value = number
    image_num_node.location = (-600,-500)
    tex_coord_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeTexCoord')
    tex_coord_node.location = (-600,0)
    seperateXYZ_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeSeparateXYZ')
    seperateXYZ_node.location = (-600,-300)
    mult1_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    mult1_node.location = (-400,-300)
    mult1_node.operation = 'MULTIPLY'
    mult2_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    mult2_node.location = (300,300)
    mult2_node.operation = 'MULTIPLY'
    div1_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    div1_node.location = (-200,0)
    div1_node.operation = 'DIVIDE'
    div2_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    div2_node.location = (0,0)
    div2_node.operation = 'DIVIDE'
    add_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    add_node.location = (200,-300)
    add_node.operation = 'ADD'
    Round_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeMath')
    Round_node.location = (-200,-500)
    Round_node.operation = 'ROUND'
    texImage = new_mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(image_path)
    combineXYZ_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeCombineXYZ')
    combineXYZ_node.location = (100,200)
    Contrast_node = new_mat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
    Contrast_node.inputs[1].default_value = 0.1
    Contrast_node.inputs[2].default_value = 0.3
    Contrast_node.location = (300,0)
    Emission = new_mat.node_tree.nodes.new(type = 'ShaderNodeEmission')    
    new_mat.node_tree.nodes["Emission"].inputs[0].default_value = new_color
    if default == True:
        new_mat.node_tree.links.new(texImage.outputs[0], Emission.inputs[0])
    Emission.location = (500,0)
    ReRoute1 = new_mat.node_tree.nodes.new(type = 'NodeReroute')
    ReRoute1.location = (-500,-400)
    ReRoute2 = new_mat.node_tree.nodes.new(type = 'NodeReroute')
    ReRoute2.location = (-400,-100)
    Output = new_mat.node_tree.nodes.new(type = 'ShaderNodeOutputMaterial')
    Output.location = (700,0)
    
    new_mat.node_tree.links.new(image_num_node.outputs[0],ReRoute1.inputs[0])
    new_mat.node_tree.links.new(tex_coord_node.outputs[0],seperateXYZ_node.inputs[0])
    new_mat.node_tree.links.new(ReRoute1.outputs[0],mult1_node.inputs[1])
    new_mat.node_tree.links.new(seperateXYZ_node.outputs[2],mult1_node.inputs[0])
    new_mat.node_tree.links.new(ReRoute1.outputs[0],ReRoute2.inputs[0])
    new_mat.node_tree.links.new(ReRoute2.outputs[0],div1_node.inputs[1])
    new_mat.node_tree.links.new(seperateXYZ_node.outputs[0],div1_node.inputs[0])
    new_mat.node_tree.links.new(seperateXYZ_node.outputs[1],combineXYZ_node.inputs[1])
    new_mat.node_tree.links.new(mult1_node.outputs[0],Round_node.inputs[0])
    new_mat.node_tree.links.new(Round_node.outputs[0],div2_node.inputs[0])
    new_mat.node_tree.links.new(ReRoute1.outputs[0],div2_node.inputs[1])
    new_mat.node_tree.links.new(div1_node.outputs[0],add_node.inputs[0])
    new_mat.node_tree.links.new(div2_node.outputs[0],add_node.inputs[1])
    new_mat.node_tree.links.new(add_node.outputs[0],combineXYZ_node.inputs[0])
    new_mat.node_tree.links.new(Contrast_node.outputs[0],mult2_node.inputs[0])
    new_mat.node_tree.links.new(combineXYZ_node.outputs[0],texImage.inputs[0])
    new_mat.node_tree.links.new(texImage.outputs[0],Contrast_node.inputs[0])
    new_mat.node_tree.links.new(mult2_node.outputs[0],Emission.inputs[1])
    new_mat.node_tree.links.new(Emission.outputs[0],Output.inputs[1])
    
    return new_mat

#new_mat = create_2d_3d_converter(image_path)

#bpy.data.materials.append(new_mat)  

class MainPanel(bpy.types.Panel):
    
    bl_label = 'Volume Rendering Tool'
    bl_idname = 'AutonomCam_PT_MAINPANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Volume Rendering'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, 'my_path')
        row = layout.row()
        layout.prop(scene, 'my_color')
        row = layout.row()
        layout.prop(scene, 'my_def')
        row = layout.row()
        layout.prop(scene, 'my_int')
        row = layout.row()
        
        row.operator('camera.locked_operator', icon = 'CUBE')
        row = layout.row()
        row.operator('camera.follow_operator', icon = 'CUBE')
        row = layout.row()
        row.operator('create.material_operator', icon = 'CUBE')
        row = layout.row()
        
    
class CAMERA_OT_LOCKED(bpy.types.Operator):
    bl_label = 'CameraTrack'
    bl_idname = "camera.locked_operator"
    bl_parent_id = 'AutonomCam_PT_MAINPANEL'
    def execute(self, context):
        bpy.ops.object.add(type = 'EMPTY',location = (0,0,0))
        Selected = bpy.context.selected_objects[0]
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-4, 0, 0), rotation=(-2.25978, -5.56479e-08, -2.17453), scale=(1, 1, 1))    
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        bpy.context.object.constraints["Track To"].target = Selected
        
        return {'FINISHED'}
    
class CAMERA_OT_FOLLOW(bpy.types.Operator):
    bl_idname = 'camera.follow_operator'
    bl_label = 'FollowPath'
    bl_parent_id = 'AutonomCam_PT_MAINPANEL'
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
           
        return {'FINISHED'}
    
class CREATE_OT_MATERIAL(bpy.types.Operator):
    bl_idname = 'create.material_operator'
    bl_label = 'Change Material'
    bl_parent_id = 'AutonomCam_PT_MAINPANEL'
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        color = bpy.context.scene.my_color
        default = bpy.context.scene.my_def
        image_path = bpy.context.scene.my_path
        num =  bpy.context.scene.my_int
        new_mat = create_2d_3d_converter(image_path,color,num,default)
        mat = list(bpy.data.materials)[len(list(bpy.data.materials))-1]
        if len(list(bpy.data.objects['Cube'].data.materials)) > 0 :
            bpy.data.objects['Cube'].data.materials[0] = mat
        else:
            bpy.data.objects['Cube'].data.materials.append(mat)
        
        return {'FINISHED'}
    
def register():
    bpy.types.Scene.my_path = bpy.props.StringProperty(name="File", subtype='FILE_PATH')
    bpy.types.Scene.my_color = bpy.props.FloatVectorProperty(name ="Color",subtype = 'COLOR_GAMMA', default = (1,1,1))
    bpy.types.Scene.my_int = bpy.props.IntProperty(name = 'Image Number:')
    bpy.types.Scene.my_def = bpy.props.BoolProperty(name = 'Default Color')
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(CAMERA_OT_LOCKED)
    bpy.utils.register_class(CAMERA_OT_FOLLOW)
    bpy.utils.register_class(CREATE_OT_MATERIAL)
    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(CAMERA_OT_LOCKED)
    bpy.utils.unregister_class(CAMERA_OT_FOLLOW)
    bpy.utils.unregister_class(CREATE_OT_MATERIAL)
    
if __name__ == "__main__":
    register()