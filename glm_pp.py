"""GDB pretty-printer for GLM vector and matrix types

Supported types:
  glm::vec2, glm::vec3
  glm::mat3, glm::mat4

Matrices are displayed in the classical row-major order (i.e., row by row),
regardless of GLM's internal column-major storage.

This pretty-printer is compatible with both legacy (tvec/tmat) and current (vec/mat) GLM template syntax.
"""


print("INFO : Loading glm_pp...")

import gdb.printing


class Vec2Printer(gdb.ValuePrinter):
  def __init__(self, val):
    self.__val = val

  def to_string(self):
    x = self.__val['x']
    y = self.__val['y']
    return f"glm::vec2({x}, {y})"


class Vec3Printer(gdb.ValuePrinter):
  def __init__(self, val):
    self.__val = val

  def to_string(self):
    x = self.__val['x']
    y = self.__val['y']
    z = self.__val['z']
    return f"glm::vec3({x}, {y}, {z})"


class Mat3Printer(gdb.ValuePrinter):
  def __init__(self, val):
    self.__val = val['value']

  def to_string(self):
    output_string = ""

    names = ['x','y','z']
    for name in names:
      for column in range(3):
        output_string += f"{self.__val[column][name]} "
      output_string += '\n'

    return output_string


class Mat4Printer(gdb.ValuePrinter):
  def __init__(self, val):
    self.__val = val['value']

  def to_string(self):
    output_string = ""

    names = ['x','y','z','w']
    for name in names:
      for column in range(4):
        output_string += f"{self.__val[column][name]} "
      output_string += '\n'

    return output_string
            

def build_pretty_printer():
  pp = gdb.printing.RegexpCollectionPrettyPrinter("glm_pp")

  # regex to match following patterns :
  # glm::tvec2<TYPE, (glm::precision)0>
  # glm::vec<2, TYPE, (glm::qualifier)0>
  pp.add_printer("glm::vec2", r"^glm::(?:t)?vec(?:2<|<2,\s*)\w+,\s*\(glm::(?:precision|qualifier)\)0>$", Vec2Printer)

  # regex to match following patterns :
  # glm::tvec3<TYPE, (glm::precision)0>
  # glm::vec<3, TYPE, (glm::qualifier)0>
  pp.add_printer("glm::vec3", r"^glm::(?:t)?vec(?:3<|<3,\s*)\w+,\s*\(glm::(?:precision|qualifier)\)0>$", Vec3Printer)

  # regex to match following patterns :
  # glm::tmat3x3<TYPE, (glm::precision)0>
  # glm::mat<3, 3, TYPE, (glm::qualifier)0>
  pp.add_printer("glm::mat3", r"^glm::(?:t)?mat(?:3x3<|<3,\s*3,)\s*\w+,\s*\(glm::(?:precision|qualifier)\)0\s*>$", Mat3Printer)

  # regex to match following patterns :
  # glm::tmat4x4<TYPE, (glm::precision)0>
  # glm::mat<4, 4, TYPE, (glm::qualifier)0>
  pp.add_printer("glm::mat4", r"^glm::(?:t)?mat(?:4x4<|<4,\s*4,)\s*\w+,\s*\(glm::(?:precision|qualifier)\)0\s*>$", Mat4Printer)
  
  return pp


gdb.printing.register_pretty_printer(gdb.current_objfile(), build_pretty_printer())
