import bpy
import os

def decimate(input_path, output_path, decimateRatio):
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath=input_path)


    modifierName='DecimateMod'
    try:
        objectList=bpy.data.objects
        for obj in objectList:
            if obj.type=="MESH": 
                
                    modifier=obj.modifiers.new(modifierName,'DECIMATE')
                    modifier.ratio=decimateRatio
                    modifier.use_collapse_triangulate=True
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier=modifierName)
    except Exception as e:
        print(f"Error processing object {obj.name}: {e}")

    file_name = os.path.basename(input_path)
    output_file_path = os.path.join(output_path, file_name)

    try:

        bpy.ops.export_scene.obj(filepath=output_file_path, use_materials=False) 
    except Exception as e:
        print(f"Error exporting file: {e}")
