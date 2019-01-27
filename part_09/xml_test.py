from os import path
from xml.dom.minidom import parse

xml_file_path = path.join(path.dirname(__file__), "../img/spritesheet_jumper.xml")
print(xml_file_path)

dom_tree = parse(xml_file_path)
root_textures = dom_tree.documentElement
sub_textures = root_textures.getElementsByTagName("SubTexture")

for texture in sub_textures:
    print("name:", texture.getAttribute("name"), ",x:",
          texture.getAttribute("x"), ",y:", texture.getAttribute("y"),
          ",width:", texture.getAttribute("width"), ",height:", texture.getAttribute("height"))
