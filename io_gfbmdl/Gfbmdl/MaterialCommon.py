# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Gfbmdl

import flatbuffers

class MaterialCommon(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsMaterialCommon(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MaterialCommon()
        x.Init(buf, n + offset)
        return x

    # MaterialCommon
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MaterialCommon
    def Switches(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .MatSwitch import MatSwitch
            obj = MatSwitch()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # MaterialCommon
    def SwitchesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MaterialCommon
    def Values(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .MatInt import MatInt
            obj = MatInt()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # MaterialCommon
    def ValuesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MaterialCommon
    def Colors(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .MatColor import MatColor
            obj = MatColor()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # MaterialCommon
    def ColorsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def MaterialCommonStart(builder): builder.StartObject(3)
def MaterialCommonAddSwitches(builder, Switches): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(Switches), 0)
def MaterialCommonStartSwitchesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def MaterialCommonAddValues(builder, Values): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(Values), 0)
def MaterialCommonStartValuesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def MaterialCommonAddColors(builder, Colors): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(Colors), 0)
def MaterialCommonStartColorsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def MaterialCommonEnd(builder): return builder.EndObject()