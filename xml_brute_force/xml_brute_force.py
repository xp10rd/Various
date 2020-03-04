import xml.etree.ElementTree as ET
import sys
import os
import shutil

extension = ".xml"


class Config:
    def __init__(self, config_file_name):
        config_xml_tree = ET.parse(config_file_name)
        config_root = config_xml_tree.getroot()
        self.tags = {}
        for tag in config_root:
            if tag.tag == "base":
                self.base_folder_name = tag.text
            elif tag.tag == "wrapped":
                if tag.text == "True":
                    self.wrapped_into_folder = True
                else:
                    self.wrapped_into_folder = False
            elif tag.tag == "gen_type":
                self.gen_type = tag.text
            elif tag.tag == "file_name":
                self.xml_tree = ET.parse(self.base_folder_name + os.sep + tag.text)
            else:
                self.tags[tag] = []
                for child in tag:
                    self.tags[tag].append(Attribute(tag.tag, child.tag, child.text))


# TODO: add conditions for attributes modifying
class Attribute:
    def __init__(self, parent_tag, attribute_name, new_value):
        self.attribute_name = attribute_name
        self.new_value = new_value
        # self.conditions_dict = conditions_dict
        self.parent_tag = parent_tag

    # def check(self, tag):
    #     passed = True
    #     for condition in self.conditions_dict:
    #         if tag.get(condition) != self.conditions_dict[condition]:
    #             print(tag.get(condition) + " " + self.conditions_dict[condition])
    #             passed = False
    #             break
    #
    #     return passed

    def modify(self, tag):
        tag.set(self.attribute_name, self.new_value)

    def __ne__(self, other):
        return self.parent_tag != other.parent_tag or self.attribute_name != other.attribute_name

    def name(self):
        return self.attribute_name + "-" + self.new_value.replace(".", "")


def linear_gen_xml_files(base_folder_name, tags, xml_tree, wrapped_into_folder):
    for tag in tags:
        for attr in tags[tag]:
            folder_prefix = base_folder_name
            if wrapped_into_folder:
                folder_prefix = folder_prefix + os.sep + attr.name()
                if os.path.exists(folder_prefix):
                    shutil.rmtree(folder_prefix)
                os.mkdir(folder_prefix)
            # TODO: add conditions for attributes modifying
            for possible_tag in xml_tree.getroot().iter(tag.tag):
                # if attr.check(possible_tag):
                attr.modify(possible_tag)
                xml_tree.write(folder_prefix + os.sep + attr.name() + extension)


def cross_gen_xml_files(base_folder_name, tags, idx, attr_list, xml_tree, wrapped_into_folder):
    if idx >= len(tags):
        # TODO: add conditions for attributes modifying
        # result = True
        # for condition in attr_list:
        #     for possible_tag in xml_tree.getroot().iter(condition.parent_tag):
        #         result = result and condition.check(possible_tag)

        # if result:
        file_name = ""
        for attr in attr_list:
            file_name = file_name + attr.name() + "-"
        file_name = file_name[0:len(file_name) - 1]

        # create folders
        folder_prefix = base_folder_name
        if wrapped_into_folder:
            folder_prefix = base_folder_name + os.sep + file_name
            if os.path.exists(folder_prefix):
                shutil.rmtree(folder_prefix)
            os.mkdir(folder_prefix)

        # modify attributes
        for attr in attr_list:
            for tag in xml_tree.getroot().iter(attr.parent_tag):
                attr.modify(tag)
        xml_tree.write(folder_prefix + os.sep + file_name + extension)
    else:
        i = 0
        for attr1 in tags[idx][1]:
            tmp_attr_list1 = attr_list.copy()
            tmp_attr_list1.append(attr1)
            one_attr_flag = True  # case of one-attribute changing
            j = 0
            for attr2 in tags[idx][1]:
                if attr1 != attr2:
                    one_attr_flag = False
                    if j > i:
                        tmp_attr_list2 = tmp_attr_list1.copy()
                        tmp_attr_list2.append(attr2)
                        cross_gen_xml_files(base_folder_name, tags, idx + 1, tmp_attr_list2, xml_tree,
                                            wrapped_into_folder)
                j = j + 1
            if one_attr_flag:
                cross_gen_xml_files(base_folder_name, tags, idx + 1, tmp_attr_list1, xml_tree, wrapped_into_folder)
            i = i + 1


def gen_xml_files(base_folder_name, tags, xml_tree, gen_type, wrapped_into_folder):
    if not os.path.exists(base_folder_name):
        print(base_folder_name + " : no such directory!")
        return
    if gen_type == "linear":
        linear_gen_xml_files(base_folder_name, tags, xml_tree, wrapped_into_folder)
    elif gen_type == "cross":
        cross_gen_xml_files(base_folder_name, list(tags.items()), 0, [], xml_tree, wrapped_into_folder)
    else:
        print("xml_brute_force: unrecognized parameter \"" + gen_type + "\"")


if len(sys.argv[1:]) < 1:
    print("usage: python3 xml_brute_force <path-to-config>")
    exit(-1)

config = Config(sys.argv[1])
gen_xml_files(config.base_folder_name, config.tags, config.xml_tree, config.gen_type, config.wrapped_into_folder)
