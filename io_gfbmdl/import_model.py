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
from math import radians

import os
import os.path
import sys
import math
import operator
import numpy
import struct
import bmesh
from enum import IntEnum
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import flatbuffers
import Gfbmdl.Bone
import Gfbmdl.BoneRigidData
import Gfbmdl.BoundingBox
import Gfbmdl.Model
import Gfbmdl.Material
import Gfbmdl.Mesh
import Gfbmdl.MeshAttribute
import Gfbmdl.MeshPolygon
import Gfbmdl.Group
import Gfbmdl.MaterialCommon
import Gfbmdl.MatFloat
import Gfbmdl.MatInt
import Gfbmdl.MatSwitch
import Gfbmdl.MatColor
import Gfbmdl.ColorRGB32
import Gfbmdl.TextureMap
import Gfbmdl.TextureMapping
import Gfbmdl.CollisionGroup
import Gfbmdl.Vector3

class BufferFormat(IntEnum):
    Float = 0
    HalfFloat = 1
    Byte = 3
    Short = 5
    BytesAsFloat = 8

# #####################################################
# Utils
# #####################################################
def CalcStride(type, cnt):
    ret = 0
    if type == BufferFormat.Float:
        ret = 4 * cnt
    if type == BufferFormat.HalfFloat:
        ret = 2 * cnt
    if type == BufferFormat.Byte:
        ret = cnt
    if type == BufferFormat.Short:
        ret = 2 * cnt
    if type == BufferFormat.BytesAsFloat:
        ret = 1 * cnt
    return ret
    
def RotateObj(obj, angle, axis):
    rot_mat = Matrix.Rotation(radians(angle), 4, axis)

    orig_loc, orig_rot, orig_scale = obj.matrix_world.decompose()
    orig_loc_mat = Matrix.Translation(orig_loc)
    orig_rot_mat = orig_rot.to_matrix().to_4x4()
    orig_scale_mat = Matrix.Scale(orig_scale[0],4,(1,0,0)) @ Matrix.Scale(orig_scale[1],4,(0,1,0)) @ Matrix.Scale(orig_scale[2],4,(0,0,1))

    obj.matrix_world = orig_loc_mat @ rot_mat @ orig_rot_mat @ orig_scale_mat 
    
# #####################################################
# Model
# #####################################################
def BuildArmature(mon):
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
        btype = bone.BoneType()
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

def CreateMaterial(material):
    mat = bpy.data.materials.new(name=material.Name().decode("utf-8"))
    mat.use_nodes = True
    return mat

def CreateMesh(ind, mesh, mats):        
    attribType = []
    alignStride = []
    totalStride = 0
    for t in range(mesh.AttributesLength()):
        attrib = mesh.Attributes(t)
        attribType.append(attrib.VertexType())
        stride = int(CalcStride(attrib.BufferFormat(), attrib.ElementCount()))
        alignStride.append(stride)
        totalStride += stride
    

    rawData = mesh.DataAsNumpy()
    print("Total bytes (mesh %d): %d" % (ind, len(rawData)))
    print("Total stride (mesh %d): %d" % (ind, totalStride))
    
    nmesh = bpy.data.meshes.new("Mesh_%d" % ind)
    
    # Create new bmesh
    bm = bmesh.new()
    bm.from_mesh(nmesh)
    
    # Parse raw buffer
    uv_map = []
    cols = []
    vc = bm.loops.layers.color.new("color")
    for v in range(int(len(rawData)/totalStride)):
        baseOff = int(v*totalStride)
        [posx,posy,posz] = struct.unpack_from('3f', rawData, baseOff)
        [normx,normy,normz,normw] = struct.unpack_from('4e', rawData, baseOff+12)
        [bnormx,bnormy,bnormz,bnormw] = struct.unpack_from('4e', rawData, baseOff+20)
        [u_coord, v_coord] = struct.unpack_from('2f', rawData, baseOff+28)
        [r1, g1, b1, a1, r2, g2, b2, a2] = struct.unpack_from('4B4B', rawData, baseOff+36)
        [boneId, boneWeight] = struct.unpack_from('If', rawData, baseOff+44)
        vert = bm.verts.new((posx,posy,posz))
        vert.normal = ((normx,normy,normz))
        uv_map.append((u_coord,v_coord))
        cols.append((r1/255.0, g1/255.0, b1/255.0, a1/255.0))
        bm.verts.index_update()
    
    # Iterate through polygons
    for poly in range(mesh.PolygonsLength()):
        polygon = mesh.Polygons(poly)
        matIdx = polygon.MaterialIndex()
        pdata = polygon.FacesAsNumpy()
        bm.verts.ensure_lookup_table()
        d=0
        bm.faces.ensure_lookup_table()
        # Set faces and cooresponding material ids
        while d < int(len(pdata)-2):
            face = bm.faces.new((bm.verts[pdata[d]], bm.verts[pdata[d+1]], bm.verts[pdata[d+2]]))
            face.material_index = matIdx
            face.normal_update()
            d+=3
            
        # Set vertex colors
        for face in bm.faces:
            for loop in face.loops:
                loop[vc] = cols[loop.vert.index]
        
    # Assign bmesh to new created mesh and link to scene
    bm.to_mesh(nmesh)
    bm.free()
    obj = bpy.data.objects.new(nmesh.name, nmesh)            
    bpy.context.collection.objects.link(obj)

    
    # Assign all materials to each mesh (maybe do this smarter later?)
    for mt in mats:
        obj.data.materials.append(mt)
        
def LoadModel(buf):
    mon = Gfbmdl.Model.Model.GetRootAsModel(buf, 0)
    
    # Create armature
    BuildArmature(mon)
    
    # Create materials
    mats = []
    matLen = mon.MaterialsLength()
    for i in range(matLen):
        mats.append(CreateMaterial(mon.Materials(i)))
    
    # Create meshes
    for i in range(mon.MeshesLength()):
        CreateMesh(i, mon.Meshes(i), mats)

    # Orient properly
    obj = [o for o in bpy.context.scene.objects if o.type == 'MESH' or o.type == 'ARMATURE']
    for o in obj:
        RotateObj(o, 90, 'X')
    
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