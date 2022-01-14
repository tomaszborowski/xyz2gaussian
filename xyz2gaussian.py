#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script to generate a series of Gaussian input files for a series of geometries
stored in a single xyz file

Reads: #1  head file (head of Gaussian input, up to and including the charge/spin line)
       #2  body file (template geometry section of the Gaussian input; xyz are later ignored)
       #3  tail file (all that needs to be in the input below the geometry)
       #4  xyz file with geometries for which input files are to be created

Outputs: a series of files with names based on the name of the xyz file and ending
        with a sequance number: _0XYZ.com

Created on Thu Sep  2 08:03:08 2021
@authors: A. Gomółka, T. Borowski
"""
# import sys

from xyz2gaussian_aux import read_head_tail, read_body, read_xyz, count_lines
from xyz2gaussian_aux import int_digits, head_remove_guess, head_add_oldchk, head_add_chk_label
from xyz2gaussian_aux import head_change_comment, gen_file_name, gen_new_body
from xyz2gaussian_aux import write_g_input

### ---------------------------------------------------------------------- ###
### Seting the file names                                                  ###
# head_file_name = sys.argv[1]
# body_file_name = sys.argv[2]
# tail_file_name = sys.argv[3]
# xyz_file_name = sys.argv[4]

### Seting the file names - wczytywanie danych z głównego pliku inputowego
# main_file_name = sys.argv[1]
# xyz_file_name = sys.argv[2]


### ---------------------------------------------------------------------- ###
### test cases
head_file_name = 'head'
body_file_name = 'body'
tail_file_name = 'tail'
xyz_file_name = 'oh_h2o.irc_ts.xyz'
body_oniom_file_name = 'body_oniom'
tail_oniom_file_name = 'tail_oniom'

### ---------------------------------------------------------------------- ###
### reading head, body, tail
head_f = open(head_file_name, 'r')
head = read_head_tail(head_f)
head_f.close()

body_f = open(body_file_name, 'r')
body = read_body(body_f)
n_lines_body = count_lines(body_f)
body_f.close()

# added lines
body_oniom_f = open(body_oniom_file_name, 'r')
body_oniom = read_body(body_oniom_f)
body_oniom_f.close()

tail_f = open(tail_file_name, 'r')
tail = read_head_tail(tail_f)
tail_f.close()

# added lines
tail_oniom_f = open(tail_oniom_file_name, 'r')
tail_oniom = read_head_tail(tail_oniom_f)
tail_oniom_f.close()

### reading the main file
# main_file_f = open(main_file_name, 'r')
# main_file = read_head_tail(main_file_f)

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