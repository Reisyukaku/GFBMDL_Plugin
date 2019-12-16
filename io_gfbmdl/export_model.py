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
import sys
import os.path
import math
import operator
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

# Globals
use_binormals = True
has_UVs = [ True, False, False, False ]
has_Colors = [ True, True, False, False ]
has_bones = True

# enums
class VertexType(IntEnum):
    Position = 0
    Normal = 1
    Binormal = 2
    UV1 = 3
    UV2 = 4
    UV3 = 5
    UV4 = 6
    Color1 = 7
    Color2 = 8
    Color3 = 9
    Color4 = 10
    BoneID = 11
    BoneWeight = 12

class BufferFormat(IntEnum):
    Float = 0
    HalfFloat = 1
    Byte = 3
    Short = 5
    BytesAsFloat = 8
    
class WrapMode(IntEnum):
    Repeat = 0
    Clamp = 1
    Mirror = 2

# Temporary i guess
matSwitches = [
    ("useColorTex", 1),
    ("SwitchEmissionMaskTexUV", 0),
    ("EmissionMaskUse", 0),
    ("SwitchPriority", 0),
    ("Layer1Enable", 0),
    ("SwitchAmbientTexUV", 0),
    ("AmbientMapEnable", 1),
    ("SwitchNormalMapUV", 0),
    ("NormalMapEnable", 1),
    ("LightTableEnable", 1),
    ("SpecularMaskEnable", 0),
    ("BaseColorAddEnable", 1),
    ("SphereMapEnable", 0),
    ("SphereMaskEnable", 0),
    ("RimMaskEnable", 0),
    ("alphaShell", 0),
    ("EffectVal", 1),
    ("NormalEdgeEnable", 1),
    ("OutLineIDEnable", 0),
    ("OutLineColFixed", 0)
]

matValues = [
    ("ColorUVScaleU", 2.0),
    ("ColorUVScaleV", 1.0),
    ("ColorUVTranslateU", 0.0),
    ("ColorBaseU", 0.0),
    ("ColorUVTranslateV", 0.0),
    ("ColorBaseV", 0.0),
    ("ConstantColor0Val", 1.0),
    ("Layer1UVScaleU", 1.0),
    ("Layer1UVScaleV", 1.0),
    ("Layer1UVTranslateU", 0.0),
    ("Layer1BaseU", 0.0),
    ("Layer1UVTranslateV", 0.0),
    ("Layer1BaseV", 0.0),
    ("EmissionMaskVal", 1.0),
    ("ConstantColorSd0Val", 1.0),
    ("ConstantColor1Val", 1.0),
    ("ConstantColorSd1Val", 1.0),
    ("ColorLerpValue", 0.0),
    ("L1ConstantColor0Val", 1.0),
    ("L1AddColor0Val", 0.0),
    ("L1ConstantColor1Val", 1.0),
    ("L1AddColor1Val", 0.0),
    ("L1ConstantColorSd0Val", 1.0),
    ("L1ConstantColorSd1Val", 1.0),
    ("Layer1OverLerpValue", 1.0),
    ("NormalMapUVScaleU", 1.0),
    ("NormalMapUVScaleV", 1.0),
    ("LightTblIndex", 6.0),
    ("LightMul", 1.0),
    ("SpecularPower", 6.0),
    ("SpecularScale", 0.3),
    ("SphereMapColorVal", 1.0),
    ("RimColorVal", 1.0),
    ("RimPower", 8.0),
    ("RimStrength", 8.0),
    ("OnGameEmissionVal", 1.0),
    ("ConstantColorVal", 1.0),
    ("ConstantAlpha", 1.0),
    ("OnGameColorVal", 1.0),
    ("OnGameAlpha", 1.0),
    ("OutLineID", 0.0),
    ("ProgID", 0.0),
    ("Def0_OneMin1_FreCol", 1.0),
    ("DistortionIntensity", 1.0),
    ("Sin01", 4.0),
    ("ScaleUV", 1.0),
    ("EffectTexTranslateU", 0.0),
    ("EffectTexTranslateV", 0.0),
    ("EffectTexRotate", 0.0),
    ("EffectTexScaleU", 8.0),
    ("EffectTexScaleV", 5.0),
    ("EffectColPower", 1.0)
]

matColors = [
    ("ConstantColor0", 1.0, 1.0, 1.0),
    ("ConstantColorSd0", 0.651, 0.7, 0.63),
    ("ConstantColor1", 1.0, 1.0, 1.0),
    ("ConstantColorSd1", 0.651, 0.7, 0.63),
    ("L1ConstantColor0", 1.0, 1.0, 1.0),
    ("L1AddColor0", 1.0, 1.0, 1.0),
    ("L1ConstantColor1", 1.0, 1.0, 1.0),
    ("L1AddColor1", 1.0, 1.0, 1.0),
    ("L1ConstantColorSd0", 1.0, 1.0, 1.0),
    ("L1ConstantColorSd1", 1.0, 1.0, 1.0),
    ("DeepShadowColor", 1.0, 1.0, 1.0),
    ("SpecularColor", 0.813333, 1.0, 0.65),
    ("SphereMapColor", 1.000024, 1.000024, 1.000024),
    ("RimColor", 0.314675, 0.41, 0.2255),
    ("RimColorShadow", 0.1622, 0.2, 0.074),
    ("ConstantColor", 1.0, 1.0, 1.0),
    ("OnGameColor", 1.0, 1.0, 1.0),
    ("OutLineCol", 0.39, 0.6, 0.46),
    ("EffectColor01", 1.0, 0.0, 1.0)
]

matCommSwitch = [
    ("FogEnable", 1),
    ("DiscardEnable", 0),
    ("CastShadow", 1),
    ("ReceiveShadow", 0),
    ("TextureAlphaTestEnable", 0),
    ("ShadowMapPrevEnable", 1),
    ("LayerCalcMulti", 0),
    ("FireMaskPathEnable", 0),
    ("GPUInstancingEnable", 0),
    ("Wireframe", 0),
    ("DepthWrite", 1),
    ("DepthTest", 1),
    ("IsErase", 0),
    ("MayaPreviewEnable", 0)
]

matCommVals = [
    ("CullMode", 0),
    ("LightSetNo", 0),
    ("ShaderType", 0),
    ("Priority", 0),
    ("MipMapBias", 0),
    ("PreMultiplieMode", 0),
    ("BlendMode", 0),
    ("ColorMapUvIndex", 0),
    ("Layer1UvIdx", 0),
    ("EmissionMaskTexSS", 7),
    ("AmbientTexSS", 7),
    ("NormalMapTexSS", 7),
    ("Col0TexSS", 7),
    ("LyCol0TexSS", 7),
    ("PolygonOffset", 0)
]

texMaps = [
    "Col0Tex",
    "EmissionMaskTex",
    "LyCol0Tex",
    "AmbientTex",
    "NormalMapTex",
    "LightTblTex",
    "SphereMapTex",
    "EffectTex"
]

matCommColors = [

]

MeshAttribute = [
    (VertexType.Position, BufferFormat.Float, 3),
    (VertexType.Normal, BufferFormat.HalfFloat, 4),
    (VertexType.Binormal, BufferFormat.HalfFloat, 4),
    (VertexType.UV1, BufferFormat.Float, 2),
    (VertexType.UV2, BufferFormat.Float, 2),
    (VertexType.UV3, BufferFormat.Float, 2),
    (VertexType.UV4, BufferFormat.Float, 2),
    (VertexType.Color1, BufferFormat.Byte, 4),
    (VertexType.Color2, BufferFormat.Byte, 4),
    (VertexType.Color3, BufferFormat.Byte, 4),
    (VertexType.Color4, BufferFormat.Byte, 4),
    (VertexType.BoneID, BufferFormat.Byte, 4),
    (VertexType.BoneWeight, BufferFormat.BytesAsFloat, 4)
]

# #####################################################
# Utils
# #####################################################
def debug(str):
    print(str)

def write_file( fname, content ):
    out = open( fname, "w" )
    out.write( content )
    out.close()
   
def GetNodeWithType(mat, type):
    return [x for x in mat.node_tree.nodes if x.type==type]
    
def bounds(obj, local=False):

    local_coords = obj.bound_box[:]
    om = obj.matrix_world

    if not local:    
        worldify = lambda p: om @ mathutils.Vector(p[:]) 
        coords = [worldify(p).to_tuple() for p in local_coords]
    else:
        coords = [p[:] for p in local_coords]

    rotated = zip(*coords[::-1])

    push_axis = []
    for (axis, _list) in zip('xyz', rotated):
        info = lambda: None
        info.max = max(_list)
        info.min = min(_list)
        info.distance = info.max - info.min
        push_axis.append(info)

    import collections

    originals = dict(zip(['x', 'y', 'z'], push_axis))

    o_details = collections.namedtuple('object_details', 'x y z')
    return o_details(**originals)
    
def RotateObj(obj, angle, axis):
    rot_mat = Matrix.Rotation(radians(angle), 4, axis)

    orig_loc, orig_rot, orig_scale = obj.matrix_world.decompose()
    orig_loc_mat = Matrix.Translation(orig_loc)
    orig_rot_mat = orig_rot.to_matrix().to_4x4()
    orig_scale_mat = Matrix.Scale(orig_scale[0],4,(1,0,0)) @ Matrix.Scale(orig_scale[1],4,(0,1,0)) @ Matrix.Scale(orig_scale[2],4,(0,0,1))

    obj.matrix_world = orig_loc_mat @ rot_mat @ orig_rot_mat @ orig_scale_mat
    
def GenerateWeightsAndIndices(mesh):
    boneid = [0] * len(mesh.vertices)
    weights = [0] * len(mesh.vertices)
    arm_obj = [x for x in bpy.data.objects if x.type == 'ARMATURE'][0]
    mesh_obj = [x for x in bpy.data.objects if x.type == 'MESH' and x.name == mesh.name][0]
    b=0
    # Iterate through bones and find associated vertex group with same name
    for bone in arm_obj.data.bones:
        for g in range(len(mesh_obj.vertex_groups)):
            if bone.name == mesh_obj.vertex_groups[g].name:
                # Iterate through vertex group to find verts associated with bone
                for v in mesh.vertices:
                    for vg in v.groups:
                        if vg.group == g:
                            boneid[v.index] = b
                            weights[v.index] = vg.weight
                            break
                    else:
                        continue
                    break;
        b+=1
    return boneid, weights    
    
def CreateBoolSwitch(builder, entry):
    str = builder.CreateString(entry[0])
    b = entry[1]
    
    # create switch
    Gfbmdl.MatSwitch.MatSwitchStart(builder)
    Gfbmdl.MatSwitch.MatSwitchAddName(builder, str)
    Gfbmdl.MatSwitch.MatSwitchAddValue(builder, b)
    return Gfbmdl.MatSwitch.MatSwitchEnd(builder)
    
def CreateFloatValue(builder, val):
    str = builder.CreateString(val[0])
    f = val[1]
    
    # create value
    Gfbmdl.MatFloat.MatFloatStart(builder)
    Gfbmdl.MatFloat.MatFloatAddName(builder, str)
    Gfbmdl.MatFloat.MatFloatAddValue(builder, f)
    return Gfbmdl.MatFloat.MatFloatEnd(builder)
    
def CreateIntValue(builder, val):
    str = builder.CreateString(val[0])
    i = val[1]
    
    # create value
    Gfbmdl.MatInt.MatIntStart(builder)
    Gfbmdl.MatInt.MatIntAddName(builder, str)
    Gfbmdl.MatInt.MatIntAddValue(builder, i)
    return Gfbmdl.MatInt.MatIntEnd(builder)
    
def CreateColorValue(builder, col):
    color = builder.CreateString(col[0])
    
    # create color
    Gfbmdl.MatColor.MatColorStart(builder)
    Gfbmdl.MatColor.MatColorAddName(builder, color)
    Gfbmdl.MatColor.MatColorAddColor(builder, Gfbmdl.ColorRGB32.CreateColorRGB32(builder, col[1], col[2], col[3]))
    return Gfbmdl.MatColor.MatColorEnd(builder)
 
# #################################
# Texture maps
# #################################
def GetMaterialTexIndex(name, mat):
    ind = 0 # dummy_col
    if name == "Col0Tex":
        arr = [x for x in range(len(mat.node_tree.nodes)) if mat.node_tree.nodes[x].type=='TEX_IMAGE']
        ind = arr[0] if len(arr) > 0 else 0
    return ind

def CreateMapping(builder):
    Gfbmdl.TextureMapping.TextureMappingStart(builder)
    Gfbmdl.TextureMapping.TextureMappingAddUnknown1(builder, 0)
    Gfbmdl.TextureMapping.TextureMappingAddWrapModeX(builder, WrapMode.Mirror)
    Gfbmdl.TextureMapping.TextureMappingAddWrapModeY(builder, WrapMode.Repeat)
    Gfbmdl.TextureMapping.TextureMappingAddWrapModeZ(builder, WrapMode.Repeat)
    Gfbmdl.TextureMapping.TextureMappingAddUnknown5(builder, 0)
    Gfbmdl.TextureMapping.TextureMappingAddUnknown6(builder, 0)
    Gfbmdl.TextureMapping.TextureMappingAddUnknown7(builder, 0)
    Gfbmdl.TextureMapping.TextureMappingAddUnknown8(builder, 0)
    Gfbmdl.TextureMapping.TextureMappingAddLodBias(builder, 0.0)
    return Gfbmdl.TextureMapping.TextureMappingEnd(builder)
    
def CreateTexMap(builder, prop, mat):
    Name = builder.CreateString(prop)
    mapping = CreateMapping(builder)
    index = GetMaterialTexIndex(prop, mat)
    
    Gfbmdl.TextureMap.TextureMapStart(builder)
    Gfbmdl.TextureMap.TextureMapAddSampler(builder, Name)
    Gfbmdl.TextureMap.TextureMapAddIndex(builder, index)
    Gfbmdl.TextureMap.TextureMapAddParams(builder, mapping)
    return Gfbmdl.TextureMap.TextureMapEnd(builder)
    
# #################################
# Material common
# ################################# 
def CreateCommonSwitch(builder):
    switches = []
    for s in matCommSwitch:
        switches.append(CreateBoolSwitch(builder, s))
    Gfbmdl.MaterialCommon.MaterialCommonStartSwitchesVector(builder, len(switches))
    for s in reversed(switches):
        builder.PrependUOffsetTRelative(s)
    return builder.EndVector(len(switches))
    
def CreateCommonValues(builder):
    values = []
    for v in matCommVals:
        values.append(CreateIntValue(builder, v))
    Gfbmdl.MaterialCommon.MaterialCommonStartValuesVector(builder, len(values))
    for v in reversed(values):
        builder.PrependUOffsetTRelative(v)
    return builder.EndVector(len(values))
    
def CreateCommonColors(builder):
    colors = []
    for c in matCommColors:
        colors.append(CreateColorValue(builder, c))
    Gfbmdl.MaterialCommon.MaterialCommonStartColorsVector(builder, len(colors))
    for c in reversed(colors):
        builder.PrependUOffsetTRelative(c)
    return builder.EndVector(len(colors))
    
# #################################
# Material
# #################################
def CreateMaterialTex(builder, mat):
    maps = []
    for t in texMaps:
        maps.append(CreateTexMap(builder, t, mat))
    Gfbmdl.Material.MaterialStartTextureMapsVector(builder, len(maps))
    for t in reversed(maps):
        builder.PrependUOffsetTRelative(t)
    return builder.EndVector(len(maps))
    
def CreateMatSwitches(builder):
    switches = []
    for s in matSwitches:
        switches.append(CreateBoolSwitch(builder, s))
    Gfbmdl.Material.MaterialStartSwitchesVector(builder, len(switches))
    for s in reversed(switches):
        builder.PrependUOffsetTRelative(s)
    return builder.EndVector(len(switches))
    
def CreateMatValues(builder):
    values = []
    for v in matValues:
        values.append(CreateFloatValue(builder, v))
    Gfbmdl.Material.MaterialStartValuesVector(builder, len(values))
    for v in reversed(values):
        builder.PrependUOffsetTRelative(v)
    return builder.EndVector(len(values))
    
def CreateMatColors(builder):
    colors = []
    for c in matColors:
        colors.append(CreateColorValue(builder, c))
    Gfbmdl.Material.MaterialStartColorsVector(builder, len(colors))
    for c in reversed(colors):
        builder.PrependUOffsetTRelative(c)
    return builder.EndVector(len(colors))
    
def CreateMatCommon(builder):
    switch = CreateCommonSwitch(builder)
    vals = CreateCommonValues(builder)
    cols = CreateCommonColors(builder)
    
    Gfbmdl.MaterialCommon.MaterialCommonStart(builder)
    Gfbmdl.MaterialCommon.MaterialCommonAddSwitches(builder, switch)
    Gfbmdl.MaterialCommon.MaterialCommonAddValues(builder, vals)
    #Gfbmdl.MaterialCommon.MaterialCommonAddColors(builder, cols)
    return Gfbmdl.MaterialCommon.MaterialCommonEnd(builder)
    
def CreateMaterial(builder, mat):
    # make strings first
    Name = builder.CreateString(mat.name)
    Shdr = builder.CreateString("PokeDefaultShader")
    
    # build components
    tex = CreateMaterialTex(builder, mat)
    switches = CreateMatSwitches(builder)
    vals = CreateMatValues(builder)
    cols = CreateMatColors(builder)
    common = CreateMatCommon(builder)
    
    # build material
    debug("Creating Material object. [%s]" % Name)
    Gfbmdl.Material.MaterialStart(builder)
    Gfbmdl.Material.MaterialAddName(builder, Name)
    Gfbmdl.Material.MaterialAddShaderGroup(builder, Shdr)
    Gfbmdl.Material.MaterialAddRenderLayer(builder, 0)
    Gfbmdl.Material.MaterialAddUnknown1(builder, 1)
    Gfbmdl.Material.MaterialAddUnknown2(builder, 1)
    Gfbmdl.Material.MaterialAddParameter1(builder, 0)
    Gfbmdl.Material.MaterialAddParameter2(builder, 0)
    Gfbmdl.Material.MaterialAddParameter3(builder, 0)
    Gfbmdl.Material.MaterialAddShaderIndex(builder, 0)
    Gfbmdl.Material.MaterialAddParameter4(builder, 0)
    Gfbmdl.Material.MaterialAddParameter5(builder, 0)
    Gfbmdl.Material.MaterialAddTextureMaps(builder, tex)
    Gfbmdl.Material.MaterialAddSwitches(builder, switches)
    Gfbmdl.Material.MaterialAddValues(builder, vals)
    Gfbmdl.Material.MaterialAddColors(builder, cols)
    Gfbmdl.Material.MaterialAddUnknown3(builder, 0)
    Gfbmdl.Material.MaterialAddUnknown4(builder, 1)
    Gfbmdl.Material.MaterialAddUnknown5(builder, 0)
    Gfbmdl.Material.MaterialAddUnknown6(builder, 0)
    Gfbmdl.Material.MaterialAddUnknown7(builder, 0)
    Gfbmdl.Material.MaterialAddCommon(builder, common)
    return Gfbmdl.Material.MaterialEnd(builder)

# #################################
# Group data
# #################################
def CreateGroup(builder, boneid, meshid, bound):
    bb = bounds(bound)
    
    Gfbmdl.Group.GroupStart(builder)
    Gfbmdl.Group.GroupAddBoneIndex(builder, boneid)
    Gfbmdl.Group.GroupAddMeshIndex(builder, meshid)
    Gfbmdl.Group.GroupAddBounding(builder, CreateBoundBox(builder, bb.x.min, bb.y.min, bb.z.min, bb.x.max, bb.y.max, bb.z.max))
    return Gfbmdl.Group.GroupEnd(builder)

# #################################
# Mesh data
# #################################
def CalculateBufferStride():
    global use_binormals
    global has_UVs
    global has_Colors
    global has_bones
    stride = 20
    if use_binormals:
        stride += 8
    for c in range(4):
        if not has_Colors[c]:
            continue
        stride += 4
    for u in range(4):
        if not has_UVs[u]:
            continue
        stride += 8
    if has_bones:
        stride += 8
    return stride
    
def CalculateBinormals(mesh):
    if not has_UVs[0]:
        bi = [(0.0, 0.0, 0.0)] * len(mesh.vertices)
        return bi
    bi = []
    mesh.calc_tangents() # slow as all  fuck
    for l in mesh.loops:
        bi.append(l.bitangent_sign * l.normal.cross(l.tangent))
    return bi

def GenerateVertexBuffer(mesh):
    global use_binormals
    global has_UVs
    global has_Colors
    global has_bones
    
    stride = CalculateBufferStride()
    debug("Vertex buffer stride: %d" % stride)
    
    buff = bytearray(len(mesh.vertices)*stride)
    # Populate colors
    cols = []
    col = []
    for c in range(4):
        if has_Colors[c]:
            # Writing colors from vert color object
            if len(mesh.vertex_colors) > c:
                debug("Vertex color1 count: %d" % len(mesh.vertex_colors[c].data))
                for i in range(len(mesh.vertex_colors[c].data)):
                    r = int(mesh.vertex_colors[c].data[i].color[0] * 255)
                    g = int(mesh.vertex_colors[c].data[i].color[1] * 255)
                    b = int(mesh.vertex_colors[c].data[i].color[2] * 255)
                    a = int(mesh.vertex_colors[c].data[i].color[3] * 255)
                    col.append(((r << 24)&0xFF000000) | ((g << 16)&0xFF0000) | ((b << 8)&0xFF00) | a&0xFF)
                cols.append(col)
            # If no color object is found, create default one
            else:
                for c in range(len(mesh.vertices)):
                    col.append(int(0xFF000000))
                cols.append(col)
        
    # Populate UVs
    uvs = []
    uv = []
    for u in range(4):
        if has_UVs[u]:
            if len(mesh.uv_layers) > u:
                debug("Vertex UV count: %d" % len(mesh.uv_layers[u].data))
                for i in mesh.uv_layers[u].data:
                    uv.append(i.uv)
                uvs.append(uv)

    # Pack data
    for i in range(len(mesh.vertices)):
        binormal = CalculateBinormals(mesh)
        pos = mesh.vertices[i].co
        norm = mesh.vertices[i].normal
        boneids, weights = GenerateWeightsAndIndices(mesh)
        baseOff = int(i*stride)
        off = 0
        # Pack vert/face data
        struct.pack_into('3f', buff, baseOff, pos[0], pos[1], pos[2])
        struct.pack_into('4e', buff, baseOff+12, norm[0], norm[1], norm[2], 0.0)
        off += 20
        if use_binormals:
            struct.pack_into('4e', buff, baseOff+off, binormal[i][0], binormal[i][1], binormal[i][2], 0.0)
            off += 8
        # Pack UVs
        for u in uvs:
            struct.pack_into('2f', buff, baseOff+off, u[i][0], u[i][1])
            off += 8
        # Pack colors
        for c in cols:
            struct.pack_into('I', buff, baseOff+off, c[i])
            off += 4
        # Pack bone data
        if has_bones:
            struct.pack_into('I', buff, baseOff+off, boneids[i])
            off += 4
            struct.pack_into('f', buff, baseOff+off, weights[i])
    return buff

def CreatePolyFaces(builder, gons):
    Gfbmdl.MeshPolygon.MeshPolygonStartFacesVector(builder, len(gons))
    for g in reversed(gons):
        builder.PrependUint16(g)
    return builder.EndVector(len(gons))

def CreatePolygon(builder, mesh, id):
    gons = []
    for p in mesh.polygons:
        if p.material_index == id:
            for v in p.vertices:
                gons.append(v)
    if len(gons) > 0:
        data = CreatePolyFaces(builder, gons)
    else:
        data = 0
    
    Gfbmdl.MeshPolygon.MeshPolygonStart(builder)
    Gfbmdl.MeshPolygon.MeshPolygonAddMaterialIndex(builder, id)
    Gfbmdl.MeshPolygon.MeshPolygonAddFaces(builder, data)
    return Gfbmdl.MeshPolygon.MeshPolygonEnd(builder)

def CreateMeshPolygons(builder, mesh):
    poly = []
    for id in range(len(mesh.materials)):
        poly.append(CreatePolygon(builder, mesh, id))
    Gfbmdl.Mesh.MeshStartPolygonsVector(builder, len(poly))
    for a in reversed(poly):
        builder.PrependUOffsetTRelative(a)
    return builder.EndVector(len(poly))

def CreateAttribute(builder, align):
    type = int(align[0])
    format = int(align[1])
    count = align[2]
    
    Gfbmdl.MeshAttribute.MeshAttributeStart(builder)
    Gfbmdl.MeshAttribute.MeshAttributeAddVertexType(builder, type)
    Gfbmdl.MeshAttribute.MeshAttributeAddBufferFormat(builder, format)
    Gfbmdl.MeshAttribute.MeshAttributeAddElementCount(builder, count)
    return Gfbmdl.MeshAttribute.MeshAttributeEnd(builder)
    
def CreateMeshAttributes(builder):
    global use_binormals
    global has_UVs
    global has_Colors
    global has_bones
    
    attrib = []
    attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Position]))
    attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Normal]))
    if use_binormals:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Binormal]))
    if has_UVs[0]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.UV1]))
    if has_UVs[1]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.UV2]))
    if has_UVs[2]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.UV3]))
    if has_UVs[3]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.UV4]))
    if has_Colors[0]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Color1]))
    if has_Colors[1]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Color2]))
    if has_Colors[2]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Color3]))
    if has_Colors[3]:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.Color4]))
    if has_bones:
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.BoneID]))
        attrib.append(CreateAttribute(builder, MeshAttribute[VertexType.BoneWeight]))
        
    Gfbmdl.Mesh.MeshStartAttributesVector(builder, len(attrib))
    for a in reversed(attrib):
        builder.PrependUOffsetTRelative(a)
    return builder.EndVector(len(attrib))
    
def CreateMeshData(builder, mesh):
    data = GenerateVertexBuffer(mesh)
    Gfbmdl.Mesh.MeshStartDataVector(builder, len(data))
    for d in reversed(data):
        builder.PrependByte(d)
    return builder.EndVector(len(data))

def CreateMesh(builder, mesh):
    polys = CreateMeshPolygons(builder, mesh)
    attrib = CreateMeshAttributes(builder)
    data = CreateMeshData(builder, mesh)
    
    Gfbmdl.Mesh.MeshStart(builder)
    Gfbmdl.Mesh.MeshAddPolygons(builder, polys)
    Gfbmdl.Mesh.MeshAddAttributes(builder, attrib)
    Gfbmdl.Mesh.MeshAddData(builder, data)
    return Gfbmdl.Mesh.MeshEnd(builder)

# #################################
# Collision data
# #################################

def CreateCollisionGroup(builder):
    Gfbmdl.RenderInfo.CollisionGroupStart(builder)
    Gfbmdl.RenderInfo.CollisionGroupAddBoneIndex(builder, 0)
    Gfbmdl.RenderInfo.CollisionGroupAddUnknown1(builder, 0)
    Gfbmdl.RenderInfo.CollisionGroupAddBoneChildren(builder, 0)
    Gfbmdl.RenderInfo.CollisionGroupAddBounding(builder, 0)
    return Gfbmdl.RenderInfo.RenderInfoEnd(builder)

# #################################
# Model data
# #################################
def GetBoneIndex(bone):
    i=0
    if bone == None:
        return -1
    for b in bpy.data.armatures[0].bones:
        if (b.name == bone.name):
            return i
        i+=1
    return -1
    
def CreateBone(builder, bone):
    Name = builder.CreateString(bone.name)

    Gfbmdl.Bone.BoneStart(builder)
    Gfbmdl.Bone.BoneAddName(builder, Name)
    Gfbmdl.Bone.BoneAddBoneType(builder, int(bone.use_deform))
    Gfbmdl.Bone.BoneAddParent(builder, GetBoneIndex(bone.parent))
    Gfbmdl.Bone.BoneAddZero(builder, 0)
    Gfbmdl.Bone.BoneAddVisible(builder, int(bone.use_deform))
    Gfbmdl.Bone.BoneAddScale(builder, Gfbmdl.Vector3.CreateVector3(builder, 1.0, 1.0, 1.0))
    Gfbmdl.Bone.BoneAddRotation(builder, Gfbmdl.Vector3.CreateVector3(builder, 0.0, 0.0, 0.0))
    Gfbmdl.Bone.BoneAddTranslation(builder, Gfbmdl.Vector3.CreateVector3(builder, bone.head[0], bone.head[1], bone.head[2]))
    Gfbmdl.Bone.BoneAddRadiusStart(builder, Gfbmdl.Vector3.CreateVector3(builder, 0.0, 0.0, 0.0))
    Gfbmdl.Bone.BoneAddRadiusEnd(builder, 0)
    Gfbmdl.Bone.BoneAddRigidCheck(builder, 0)
    return Gfbmdl.Bone.BoneEnd(builder)
    
def CreateBoundBox(builder, x1, y1, z1, x2, y2, z2):
    bb = Gfbmdl.BoundingBox.CreateBoundingBox(builder, x1, y1, z1, x2, y2, z2)
    return bb
    
def CreateTexNames(builder):
    names = []
    textures = []
    for ob in bpy.data.objects:
        if ob.type == "MESH":
            for mat_slot in ob.material_slots:
                if mat_slot.material:
                    if mat_slot.material.node_tree:
                        textures.extend([x for x in mat_slot.material.node_tree.nodes if x.type=='TEX_IMAGE'])
    size = len(textures)
    debug("Textures: %d" % size)
    for n in textures:
        names.append(builder.CreateString(n.image.name))
        debug(n.image.name)
    Gfbmdl.Model.ModelStartTextureNamesVector(builder, size)
    for n in reversed(names):
        builder.PrependUOffsetTRelative(n)
    return builder.EndVector(size)
    
def CreateMatNames(builder):
    names = []
    size = len(bpy.data.materials)
    debug("Materials: %d" % size)
    for n in bpy.data.materials:
        names.append(builder.CreateString(n.name))
    Gfbmdl.Model.ModelStartMaterialNamesVector(builder, size)
    for n in reversed(names):
        builder.PrependUOffsetTRelative(n)
    return builder.EndVector(size)
    
def CreateShaderNames(builder):
    names = []
    size = len(bpy.data.materials)
    debug("Shaders: %d" % size)
    for n in bpy.data.materials:
        names.append(builder.CreateString(n.name))
    Gfbmdl.Model.ModelStartShaderNamesVector(builder, size)
    for n in reversed(names):
        builder.PrependUOffsetTRelative(n)
    return builder.EndVector(size)
    
def CreateUnknown(builder):
    Gfbmdl.Model.ModelStartUnknownVector(builder, 0)
    return builder.EndVector(0)
    
def CreateMaterials(builder):
    mats = []
    size = len(bpy.data.materials)
    for n in bpy.data.materials:
        mats.append(CreateMaterial(builder, n))
    Gfbmdl.Model.ModelStartMaterialsVector(builder, size)
    for n in reversed(mats):
        builder.PrependUOffsetTRelative(n)
    return builder.EndVector(size)
    
def CreateGroups(builder):
    groups = []
    meshBounds = [x for x in bpy.data.objects if x.type == 'MESH']
    for g in range(len(bpy.data.meshes)):
        groups.append(CreateGroup(builder, 0, g, meshBounds[g]))
    Gfbmdl.Model.ModelStartGroupsVector(builder, len(groups))
    for g in reversed(groups):
        builder.PrependUOffsetTRelative(g)
    return builder.EndVector(len(groups))
    
def CreateMeshes(builder):
    meshes = []
    for m in bpy.data.meshes:
        meshes.append(CreateMesh(builder, m))
    Gfbmdl.Model.ModelStartMeshesVector(builder, len(meshes))
    for m in reversed(meshes):
        builder.PrependUOffsetTRelative(m)
    return builder.EndVector(len(meshes))
    
def CreateBones(builder):
    bones = []
    # Leave stub if no armature
    if len(bpy.data.armatures) <= 0:
        Gfbmdl.Model.ModelStartMeshesVector(builder, 0)
        return builder.EndVector(0)
        return
    # Get first armature data.. should only be one
    arm = bpy.data.armatures[0]
    print("Total bones: %d" % len(arm.bones))
    for b in arm.bones:
        bones.append(CreateBone(builder, b))
    Gfbmdl.Model.ModelStartMeshesVector(builder, len(arm.bones))
    for b in reversed(bones):
        builder.PrependUOffsetTRelative(b)
    return builder.EndVector(len(arm.bones))
    
def CreateCollisionData(builder):
    Gfbmdl.Model.ModelStartCollisionGroupsVector(builder, 0)
    return builder.EndVector(0)
        
def get_model_string( ctxt ):
    # Orient properly
    obj = [o for o in bpy.context.scene.objects if o.type == 'MESH' or o.type == 'ARMATURE']
    for o in obj:
        RotateObj(o, -90, 'X')
        
    try:
        builder = flatbuffers.Builder(0)
        details = bounds(([x for x in bpy.data.objects if x.type == 'ARMATURE'])[0])
        
        texNames = CreateTexNames(builder)
        shdrNames = CreateShaderNames(builder)
        unk = CreateUnknown(builder)
        matNames = CreateMatNames(builder)
        mats = CreateMaterials(builder)
        group = CreateGroups(builder)
        mesh = CreateMeshes(builder)
        bones = CreateBones(builder)
        colData = CreateCollisionData(builder)
        
        # Build Model
        debug("Creating model object.")
        Gfbmdl.Model.ModelStart(builder)
        Gfbmdl.Model.ModelAddVersion(builder, 403704096)
        Gfbmdl.Model.ModelAddBounding(builder, CreateBoundBox(builder, details.x.min, details.y.min, details.z.min, details.x.max, details.y.max, details.z.max))
        Gfbmdl.Model.ModelAddTextureNames(builder, texNames)
        Gfbmdl.Model.ModelAddShaderNames(builder, shdrNames)
        Gfbmdl.Model.ModelAddUnknown(builder, unk)
        Gfbmdl.Model.ModelAddMaterialNames(builder, matNames)
        Gfbmdl.Model.ModelAddMaterials(builder, mats)
        Gfbmdl.Model.ModelAddGroups(builder, group)
        Gfbmdl.Model.ModelAddMeshes(builder, mesh)
        Gfbmdl.Model.ModelAddBones(builder, bones)
        Gfbmdl.Model.ModelAddCollisionGroups(builder, colData)
        model = Gfbmdl.Model.ModelEnd(builder)
        
        builder.Finish(model)
        
    finally:
        # Orient back to normal
        obj = [o for o in bpy.context.scene.objects if o.type == 'MESH' or o.type == 'ARMATURE']
        for o in obj:
            RotateObj(o, 90, 'X')
    
    return builder.Bytes, builder.Head()


# #####################################################
# Main
# #####################################################
class ExportModel():
    def save( operator, context ):
        debug("Saving to " + operator.filepath)
        
        bin, off = get_model_string( context )
        f = open(operator.filepath, 'wb')
        f.write(bin[off:])
        f.close()
        
        return {"FINISHED"}