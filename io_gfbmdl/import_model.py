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

import bpy
import mathutils
from mathutils import Matrix, Euler, Vector

import os
import os.path
import math
import operator
import numpy
import struct
import bmesh

import flatbuffers
from .Gfbmdl.Model import Model
from .Gfbmdl.BoundingBox import BoundingBox
from .Gfbmdl.Material import Material
from .Gfbmdl.Mesh import Mesh
from .Gfbmdl.MeshAttribute import MeshAttribute
from .Gfbmdl.MeshPolygon import MeshPolygon
from .Gfbmdl.Bone import Bone

# #####################################################
# Utils
# #####################################################

def CalcStride(type, cnt):
    ret = 0
    if type == 0: #float
        ret = 4 * cnt
    if type == 1: #halffloat
        ret = 2 * cnt
    if type == 3: #byte
        ret = cnt
    if type == 5: #short
        ret = 2 * cnt
    if type == 8: #byteAsFloat
        ret = 1 * cnt
    return ret

def LoadModel(buf):
    mon = Model.GetRootAsModel(buf, 0)
    
    # Add materials
    mats = []
    matLen = mon.MaterialsLength()
    for i in range(matLen):
        mat = bpy.data.materials.new(name=mon.Materials(i).Name().decode("utf-8"))
        mat.use_nodes = True
        mats.append(mat)
    
    # Add meshes
    meshLen = mon.MeshesLength()
    for i in range(meshLen):
        # Get mesh
        mesh = mon.Meshes(i)
        
        alignType = []
        alignStride = []
        totalStride = 0
        for t in range(mesh.AttributesLength()):
            attrib = mesh.Attributes(t)
            alignType.append(attrib.TypeID())
            stride = int(CalcStride(attrib.FormatID(), attrib.ElementCount()))
            alignStride.append(stride)
            totalStride += stride
        

        rawData = mesh.DataAsNumpy()
        print("Total bytes (mesh %d): %d" % (i, len(rawData)))
        print("Total stride (mesh %d): %d" % (i, totalStride))
        
        nmesh = bpy.data.meshes.new("Mesh_%d" % i)
        
        # Create new bmesh
        bm = bmesh.new()
        bm.from_mesh(nmesh)
        
        # Parse raw buffer
        uv_map = []
        vc = bm.loops.layers.color.new("color")
        for v in range(int(len(rawData)/totalStride)):
            baseOff = int(v*totalStride)
            [posx,posy,posz] = struct.unpack_from('3f', rawData, baseOff)
            [normx,normy,normz,normw] = struct.unpack_from('4e', rawData, baseOff+12)
            [bnormx,bnormy,bnormz,bnormw] = struct.unpack_from('4e', rawData, baseOff+20)
            [u_coord, v_coord] = struct.unpack_from('2f', rawData, baseOff+28)
            [rgba1, rgba2] = struct.unpack_from('4p4p', rawData, baseOff+36)
            [boneId, boneWeight] = struct.unpack_from('If', rawData, baseOff+44)
            vert = bm.verts.new((posx,posy,posz))
            vert.normal = ((normx,normy,normz))
            uv_map.append((u_coord,v_coord))
            #vc.data[v].color = (rgba1[0] / 255, rgba1[1] / 255, rgba1[2] / 255, rgba1[3] / 255)
            bm.verts.index_update()
        
        # Set faces and cooresponding material ids
        for poly in range(mesh.PolygonsLength()):
            polygon = mesh.Polygons(poly)
            matIdx = polygon.MaterialIndex()
            pdata = polygon.FacesAsNumpy()
            bm.verts.ensure_lookup_table()
            d=0
            bm.faces.ensure_lookup_table()
            while d < int(len(pdata)-2):
                face = bm.faces.new((bm.verts[pdata[d]], bm.verts[pdata[d+1]], bm.verts[pdata[d+2]]))
                face.material_index = matIdx
                face.normal_update()
                d+=3
            
        # Assign bmesh to new created mesh and link to scene
        bm.to_mesh(nmesh)
        bm.free()
        obj = bpy.data.objects.new(nmesh.name, nmesh)            
        bpy.context.collection.objects.link(obj)

        
        # Assign all materials to each mesh (maybe do this smarter later?)
        for mt in mats:
            obj.data.materials.append(mt)
            
    # Add skeleton
    armature = bpy.data.armatures.new("Armature")
    obj = bpy.data.objects.new(armature.name, armature)            
    bpy.context.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    boneLen = mon.BonesLength()
    bpy.ops.object.mode_set(mode='EDIT')
    global_matrix = (Matrix.Scale(1, 4))
    for i in range(boneLen):
        bone = mon.Bones(i)
        bname = bone.Name().decode("utf-8")
        btype = bone.Type()
        transVec = bone.Translation()
        rotVec = bone.Rotation()
        parent = bone.Parent()
        vis = bone.Visible()
        eb = armature.edit_bones.new(bname)
        eb.head = (transVec.X(),transVec.Y(),transVec.Z())
        if parent >= 0:
            eb.parent = bpy.data.armatures[armature.name].edit_bones[parent]
            eb.tail = eb.parent.head
            eb.matrix = eb.parent.matrix @ global_matrix
        else:
            eb.tail = (0,0,1)
            eb.matrix = global_matrix
        #eb.use_connect = True
        
        print(eb.head)
        print(eb.tail)
        print("-----")
        
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    print("Bone count: %d" % len(armature.bones))
     
# #####################################################
# Main
# #####################################################
class ImportModel():
    def load( operator, context ):
        for f in enumerate(operator.files):
            fpath = operator.directory + f[1].name
            print("Loading " + fpath)
            
            buf = open(fpath, 'rb').read()
            buf = bytearray(buf)
            LoadModel(buf)
            bpy.ops.object.delete()
            
            return {"FINISHED"}