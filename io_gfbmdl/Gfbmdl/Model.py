# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Gfbmdl

import flatbuffers

class Model(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsModel(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Model()
        x.Init(buf, n + offset)
        return x

    # Model
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Model
    def Version(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # Model
    def Bounding(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            from .BoundingBox import BoundingBox
            obj = BoundingBox()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def TextureNames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Model
    def TextureNamesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def ShaderNames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Model
    def ShaderNamesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def Unknown(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .UnknownEmpty import UnknownEmpty
            obj = UnknownEmpty()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def UnknownLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def MaterialNames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # Model
    def MaterialNamesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def Materials(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Material import Material
            obj = Material()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def MaterialsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def Groups(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Group import Group
            obj = Group()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def GroupsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def Meshes(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Mesh import Mesh
            obj = Mesh()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def MeshesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def Bones(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Bone import Bone
            obj = Bone()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def BonesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(22))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Model
    def CollisionGroups(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .CollisionGroup import CollisionGroup
            obj = CollisionGroup()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Model
    def CollisionGroupsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(24))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def ModelStart(builder): builder.StartObject(11)
def ModelAddVersion(builder, Version): builder.PrependUint32Slot(0, Version, 0)
def ModelAddBounding(builder, Bounding): builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(Bounding), 0)
def ModelAddTextureNames(builder, TextureNames): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(TextureNames), 0)
def ModelStartTextureNamesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddShaderNames(builder, ShaderNames): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(ShaderNames), 0)
def ModelStartShaderNamesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddUnknown(builder, Unknown): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(Unknown), 0)
def ModelStartUnknownVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddMaterialNames(builder, MaterialNames): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(MaterialNames), 0)
def ModelStartMaterialNamesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddMaterials(builder, Materials): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(Materials), 0)
def ModelStartMaterialsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddGroups(builder, Groups): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(Groups), 0)
def ModelStartGroupsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddMeshes(builder, Meshes): builder.PrependUOffsetTRelativeSlot(8, flatbuffers.number_types.UOffsetTFlags.py_type(Meshes), 0)
def ModelStartMeshesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddBones(builder, Bones): builder.PrependUOffsetTRelativeSlot(9, flatbuffers.number_types.UOffsetTFlags.py_type(Bones), 0)
def ModelStartBonesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelAddCollisionGroups(builder, CollisionGroups): builder.PrependUOffsetTRelativeSlot(10, flatbuffers.number_types.UOffsetTFlags.py_type(CollisionGroups), 0)
def ModelStartCollisionGroupsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ModelEnd(builder): return builder.EndObject()
