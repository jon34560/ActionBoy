#!BPY

import struct
import bpy
import Blender

def newFileName(ext):
    return '.'.join(Blender.Get('filename').split('.')[:-1] + [ext])

def saveAllMeshes(filename):
    for object in Blender.Object.Get():
        if object.getType() == 'Mesh':
            mesh = object.getData()
            if (len(mesh.verts) > 0):
                saveMesh(filename, mesh)
                return

def saveMesh(filename, mesh):
    file = open(filename, "w")
    file.write(struct.pack("<I", len(mesh.verts)))
    file.write(struct.pack("<H", len(mesh.faces)))
    
    # Write an interleaved array containing vertex co-ordinate, normal, and UV co-ord
    for face in mesh.faces:
        for i in range(0, 3):
            file.write(struct.pack("fff", *face.v[i].co))
            file.write(struct.pack("fff", *face.v[i].no))
            file.write(struct.pack("ff", *face.uv[i]))

    # Write the vertex index array. Currently not used but still here for the moment
    for face in mesh.faces:
        assert len(face.v) == 3
        for vertex in face.v:
            file.write(struct.pack("<H", vertex.index))

inEditMode = Blender.Window.EditMode()
if inEditMode:
    Blender.Window.EditMode(0)            
Blender.Window.FileSelector(saveAllMeshes, "Export for iPhone", newFileName("gldata"))
if inEditMode:
    Blender.Window.EditMode(1)
