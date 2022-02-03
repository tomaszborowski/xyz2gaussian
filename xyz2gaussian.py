#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script to generate a series of Gaussian input files for a series of geometries
stored in a single xyz file

Reads: #1 gaussian template input file with %Chk= line
       #2 xyz file with geometries for which input files are to be created


Outputs: a series of files with names based on the name of the xyz file and ending
        with a sequance number: _0XYZ.com

@authors: A. Gomółka, Z. Wojdyla, T. Borowski
last update: 16.01.2022
"""
import sys

from xyz2gaussian_aux import read_head_tail, read_xyz, count_lines
from xyz2gaussian_aux import int_digits, head_remove_guess, head_add_oldchk, head_add_chk_label
from xyz2gaussian_aux import head_change_comment, gen_file_name, gen_new_body
from xyz2gaussian_aux import write_g_input, div_into_lists

### ---------------------------------------------------------------------- ###
### Seting the file names                                                  ###
main_file_name = sys.argv[1]
xyz_file_name = sys.argv[2]

### ---------------------------------------------------------------------- ###
### reading head, body, tail
main_file = open(main_file_name, 'r')
main_file_content = read_head_tail(main_file)
head, body, tail = div_into_lists(main_file_content)
main_file.close()

n_lines_body = len(body)

### ---------------------------------------------------------------------- ###
### check consistency between body and xyz file content, calculate number
### of geometries to be read
xyz_f = open(xyz_file_name, 'r')
n_lines_xyz = count_lines(xyz_f)

if n_lines_xyz % (n_lines_body + 2) != 0:
    print("Inconsitency between number of lines in the xyz and the body files")
    print("body: ", n_lines_body)
    print("xyz file: ", n_lines_xyz)
    exit(1)
else:
    n_geoms = n_lines_xyz // (n_lines_body + 2)  
    n_atoms = n_lines_body

### ---------------------------------------------------------------------- ###
### main loop of the script

label_n_digits = int_digits(n_geoms) + 1

for i in range(n_geoms):
    n_read, comment_line, geo = read_xyz(xyz_f)
    if n_read != n_lines_body:
        print("Inconsitency between number of atoms read from the xyz file \
              and number of line in the body file")
        print("body: ", n_lines_body)
        print("xyz file: ", n_read)
        exit(1)
    if i == 0:
        head_new = head_remove_guess(head)
        head_new = head_add_chk_label(head_new, label_n_digits, i)  # added line
    else:
        head_new = head_add_oldchk(head, label_n_digits, i)

    head_new = head_change_comment(head_new, comment_line)
    body_new = gen_new_body(body, geo)
    out_file_name = gen_file_name(xyz_file_name, label_n_digits, i)
    write_g_input(out_file_name, head_new, body_new, tail)

xyz_f.close()
