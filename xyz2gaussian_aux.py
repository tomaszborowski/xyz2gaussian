#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A collection of functions for xyz2gaussian

Created on Thu Sep  2 08:32:04 2021

@authors: A. Gomółka, T. Borowski
"""
import math, re

'''
Note: 
For the head_add_chk_label() and head_add_oldchk() functions - the file must end with a ".chk" extension
'''
'''
print(function_name._doc_) - displaying docstring documentation for the function named "function name"
'''

def count_lines(file):

    """
    Counts number of lines in a file

    Parameters
    ----------
    file : file object

    Returns
    -------
    i: int
        number of lines in a file
    """

    file.seek(0)
    i = -1
    for i, l in enumerate(file):
        pass
    file.seek(0)

    return i + 1


def int_digits(n):

    """
    For a positive integer n returns its number of digits

    Parameters
    ----------
    n : INT

    Returns
    -------
    digits : int
            number of digits

    """

    digits = int(math.log10(n))+1
    return digits


def read_head_tail(file):

    """
    Reading the contents of a file

    Parameters
    ----------
    file : file object

    Returns
    -------
    split_line: list
            a list containing the following lines of the file

    """

    file.seek(0)
    line = file.read()   # this line reads the entire file
    split_line = line.splitlines()
    file.seek(0)

    return split_line


def read_xyz(file):

    """
    Listing x, y and z coordinates

    Parameters
    ----------
    file : file object

    Returns
    -------
    numberOfatoms : int
                number of atoms
    comment : str
            string containing the comment
    geo : list
        a list with x, y and z coordinates

    """

    comment = ""
    numberOfatoms  = int(file.readline())
    comment = file.readline() # taking a comment
    comment = comment.rstrip('\n')
    comment = comment.lstrip()

    geo = []

    for j in range(numberOfatoms):
        floatString = ""

        split_line = file.readline()
        split_line = split_line.split()
        split_line = split_line[1:]
        floatString = "  ".join(split_line)

        geo.append(floatString)

    return numberOfatoms, comment, geo


def read_body(file):

    """
    Listing all data except for coordinates x, y and z

    Parameters
    ----------
    file : file object

    Returns
    -------
    body : list
        a list of tuples containing all data except x, y and z

    """

    file.seek(0)
    body = []
    n_lines = count_lines(file)
    split_line = file.readline()
    split_line = split_line.split()

    index_floatList = []
    for i, variable in enumerate(split_line):
        if ((re.match("^[-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", variable)) or (re.match("^[-]?[0-9]+$", variable))):
            index_floatList.append(i)

    ints = [int(x) for x in index_floatList]

    if (len(index_floatList) == 4):
        ints.pop(0)

    for _ in range(n_lines):
        bodyStringRight = ""
        bodyStringLeft = ""
        bodyStringLeft = "  ".join(split_line[:ints[0]])
        bodyStringRight = "  ".join(split_line[(ints[2] + 1):])

        body.append(tuple([bodyStringLeft,bodyStringRight]))
        split_line = file.readline()
        split_line = split_line.split()

    file.seek(0)
    return body


def head_remove_guess(head):

    """
    Removing "guess = read" expression from head

    Parameters
    ----------
    head : list

    Returns
    -------
    new_head : list
        a list containing elements of a new head

    """

    head_new = head.copy()
    new_head = []
    for i in head_new:
        if "guess=read" in i:
            i = i.replace("guess=read","")

        new_head.append(i)
    return new_head


# First version of the head_add_chk_label() function
# Labeled line as the first item in the list (at the beginning of the file

def head_add_chk_label(head,label_digits,index):

    """
    Adding a label specifying the file number and data set number

    Parameters
    ----------
    head : list
    label_digits : int
    index : int

    Returns
    -------
    head_new : list
        a list containing elements of a new head

    """

    head_new = head.copy()
    line_withoutLabel = ', '.join([item for item in head_new if item.startswith('%Chk' or '%chk')])
    head_new.remove(line_withoutLabel)

    start_fileName = line_withoutLabel.find("=") + len("=")
    end_filename = line_withoutLabel.find(".chk") # the file must end with a ".chk" extension
    file_name = line_withoutLabel[start_fileName:end_filename]

    label = str(index).zfill(label_digits)
    fileName_withLabel = file_name + label
    head_withLabel = line_withoutLabel.replace(file_name,fileName_withLabel)
    head_new[0] = head_withLabel

    return head_new


# Second version of the head_add_chk_label() function
# A line with a label at the position of the line to be changed

def head_add_chk_label(head,label_digits,index):

    """
    Adding a label specifying the file number and data set number

    Parameters
    ----------
    head : list
    label_digits : int
    index : int

    Returns
    -------
    head_new : list
        a list containing elements of a new head

    """

    head_new = head.copy()
    line_withoutLabel = ', '.join([item for item in head_new if item.startswith('%Chk' or '%chk')])
    index_line_withoutLabel = head_new.index(line_withoutLabel)

    start_fileName = line_withoutLabel.find("=") + len("=")
    end_filename = line_withoutLabel.find(".chk") # the file must end with a ".chk" extension
    file_name = line_withoutLabel[start_fileName:end_filename]

    label = str(index).zfill(label_digits)
    fileName_withLabel = file_name + label
    head_withLabel = line_withoutLabel.replace(file_name,fileName_withLabel)
    head_new[index_line_withoutLabel] = head_withLabel

    return head_new


def head_add_oldchk(head,label_digits,index):

    """
    Adding a label specifying the previous file number with the phrase "Old"

    Parameters
    ----------
    head : list
    label_digits : int
    index : int

    Returns
    -------
    head_new : list
        a list containing elements of a new head

    """

    head_new = head.copy()
    head_firstLine = ', '.join([item for item in head_new if item.startswith('%Chk' or '%chk')])
    head_new = head_add_chk_label(head_new, label_digits, index) # head z label

    start_fileName = head_firstLine.find("=") + len("=")
    end_filename = head_firstLine.find(".chk") # the file must end with a ".chk" extension
    file_name = head_firstLine[start_fileName:end_filename]

    label = str(index-1).zfill(label_digits)
    fileName_withLabel = file_name + label
    head_withLabel = head_firstLine.replace(file_name, fileName_withLabel)

    start_old = head_withLabel.find("%") + len("%")
    head_with_oldAndlabel = head_withLabel[:start_old] + "Old" + head_withLabel[start_old:]
    head_new.insert(0, head_with_oldAndlabel)

    return head_new


def head_change_comment(head, comm_line):

    """
    Adding a comment in place of the word "test"

    Parameters
    ----------
    head : list
    comm_line : str

    Returns
    -------
    new_head : list
        a list containing elements of a new head

    """

    new_head = head.copy()
    new_head[-3] = comm_line

    return new_head


def gen_file_name(xyz_fileName, label_digits,index):

    """
    Generating a file name - adding a label and changing the extension

    Parameters
    ----------
    xyz_fileName : str
    label_digits : int
    index : int

    Returns
    -------
    new_fileName : str
        a string that specifies the new file name

    """

    start_fileName = 0
    end_filename = xyz_fileName.find(".xyz")
    new_fileName = xyz_fileName[start_fileName:end_filename]

    label = str(index).zfill(label_digits) + ".com"
    new_fileName = new_fileName + label

    return new_fileName


# First version of the gen_new_body() function

def gen_new_body(body, geo):

    """
    Combining the contents of the body list with the contents of the geo list

    Parameters
    ----------
    body : tuples list
    geo : tuples list

    Returns
    -------
    newBody_list : list
        a list consisting of geo and body lists

    """

    list_length = len(body)
    newBody_list = []
    for i in range(list_length):
        newBody_list.append((body[i])[0] + "  " + geo[i] + "  " + (body[i])[1])

    return newBody_list


# Second version of the gen_new_body() function

def gen_new_body(body, geo):

    """
    Combining the contents of the body list with the contents of the geo list

    Parameters
    ----------
    body : tuples list
    geo : tuples list

    Returns
    -------
    newBody_list : list
        a list consisting of geo and body lists

    """

    list_length = len(body)
    newBody_list = []
    for i in range(list_length):
        if (len(body[i][1]) > 0):
            newBody_list.append((body[i])[0] + "  " + geo[i] + "  " + (body[i])[1])
        else:
            newBody_list.append((body[i])[0] + "  " + geo[i])

    return newBody_list


# Third version of the gen_new_body() function

def gen_new_body(body, geo):

    """
    Combining the contents of the body list with the contents of the geo list

    Parameters
    ----------
    body : tuples list
    geo : tuples list

    Returns
    -------
    newBody_list : list
        a list consisting of geo and body lists

    """

    list_length = len(body)
    newBody_list = []
    newBody = ""
    for i in range(list_length):
        if (len(body[i][1]) > 0):
            newBody = body[i][0] + "  " + geo[i] + "  " + body[i][1]
        else:
            newBody = body[i][0] + "  " + geo[i]
        newBody_list.append(newBody)

    return newBody_list



def write_g_input(out_file_name, head_new, body_new, tail):

    """
    Create a file with specific content

    Parameters
    ----------
    out_file_name : str
    head_new : list
    body_new : list
    tail : list

    Returns
    -------
    Specified file containing head, body, x, y and z coordinates, and tail

    """

    file_output = open(out_file_name, 'w')

    for part in [head_new, body_new, tail]:
        for i in range(len(part)):
            file_output.write(part[i] + "\n")

    file_output.close()


def div_into_files(read_file):

    """
    Dividing the main,input file into smaller files named head, body, and tail

    Parameters
    ----------
    read_file : file

    Returns
    -------
    Files containing head, body and tail

    """

    blankLine_counter = 0
    head_end_index = 0
    body_end_index = 0
    file_output_head = open('head_test', 'w')
    file_output_body = open('body_test', 'w')
    file_output_tail = open('tail_test', 'w')

    for i, var in enumerate(read_file):

        if (read_file[i] == ''):
            blankLine_counter += 1
            if (blankLine_counter == 2):
                head_end_index = i + 2  # the beginning of the body (index)
            if (blankLine_counter == 3):
                body_end_index = i + 1  # the beginning of the tail (index)
                break

    file_output_head.write("\n".join(read_file[0:head_end_index]))
    file_output_body.write("\n".join(read_file[head_end_index:body_end_index]))
    file_output_tail.write("\n".join(read_file[body_end_index:]))

    file_output_head.close()
    file_output_body.close()
    file_output_tail.close()