#!/usr/bin/env python3

import os
import sys
import argparse
import glob
import re

# To create a GIF movie with GLVIS do:
# 1. python3 glvis.py niederer.vtk sol.*.gf
# 2. glvis -run GIFScript.glvis
# 3. convert -delay 20 image.????.png Movie.gif


def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

class glvis:
    '''
    glivis solution reader
    '''
    def __init__(self, time = 1, mesh_file = 'mesh.vtk', mpi = '1',screenshot = 1):
        # file stem (we can pass something like *.0000)
        #g_matcher = file_stem
        #self.file_list = glob.glob(g_matcher)
       # self.sol_name = sol_name
        self.time = time
        self.mpi = mpi
        self.mesh_file = mesh_file
        self.screenshot = screenshot
        if(self.screenshot ):
            self.name = 'screenshot'
        else: 
            self.name = ''

        # Check if we found files
       # if len(self.file_list) == 0:
           # print('No files matching {}'.format(file_stem))
           # self.foundFiles = False
       # else:
           # print('Files matching {}'.format(self.file_list))
            #self.foundFiles = True

   # def getFoundFiles(self):
       # '''Check if files are detected or not'''
       # return self.foundFiles

    def create_GIFScript(self):
        '''Create the script for animation in glvis'''

       # print('Creating GIFScript.glvis...'.format(self.file_list), end='')
        out_file = open('GIFScript.glvis','w')

        textBlock = [
        '# Visualization window geometry',
        'window 0 0 600 600',
        '# Initial solution',
        'psolution' + ' '+self.mpi +' solution/' + self.mesh_file + ' 0 ' + 'solution/sol.0.gf',
        ' ',
        '# Setup the GLVis scene. Executed after pressing the space bar.',
        '{',
        ' perspective off',
        '# view 0 0',
        '# viewcenter 0 0',
        ' zoom 1.95',
        ' keys f',
        ' keys a',
        ' keys a',
        #' keys m',
        ' keys c',
        ' keys l'
        #' palette 16',
        ' perspective on',
        ' valuerange -83.0 30',
        '}',
        ' '
        ]
        for line in textBlock:
            out_file.write(line)
            out_file.write('\n')
        out_file.write('# Take multiple screenshots. Executed after pressing the space bar. \n')
        out_file.write('{ \n')
        for i in range(1,time):
            out_file.write('  psolution' + ' '+self.mpi +' solution/'  + self.mesh_file + ' 0 ' + 'solution/sol.'+ str(i) +'.gf ' + \
                           'valuerange -83.0 30' + ' ' + \
                           self.name + ' ' + 'image/image.'+str(i)+'.png\n'
                           )
            #out_file.write("keys ")
                           
        out_file.write('} \n')

        out_file.close()
        print('done')
        print()
if __name__ == "__main__":

    nargs = len(sys.argv)

    if nargs == 1:
        mesh_file = 'mesh'
        #sol_stem = 'sol.*.gf.*'
        mpi = '1'
        time = 1000
    elif nargs == 2:
        mesh_file = sys.argv[1]
        #sol_stem = 'sol.*.gf.*'
        mpi = '1'
        time = 1000
        screenshot = 1
    elif nargs == 3:
        mesh_file = sys.argv[1]
        #sol_stem = 'sol.*.gf.*'
        time = 1000
        mpi = sys.argv[2]
        screenshot = 1
    elif nargs == 4:
        mesh_file = sys.argv[1]
        mpi = sys.argv[2]    
        time = int(sys.argv[3])
        screenshot = 1
    elif nargs == 5:
        mesh_file = sys.argv[1]
        mpi = sys.argv[2]    
        time = int(sys.argv[3])
        screenshot = int(sys.argv[4])
   # else:
        #raise Exception('usage: python3 ~/tools_py/{} snapshot_dir_stem anatomy_dir'.format(os.path.basename(sys.argv[0])))

    # Construct of the glvis interface
    glvis_sol = glvis(time, mesh_file, mpi, screenshot)

    # Construct the script GIFScript.glvis to construct the animation
    glvis_sol.create_GIFScript()
