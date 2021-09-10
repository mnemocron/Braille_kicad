# -*- coding: utf-8 -*-
#!/usr/bin/env python

# https://www.lvib.org/what-is-braille/


# ISO 19028:2016   Accessible design — Information contents, figuration and display methods of tactile guide maps
# DIN 32984: 2020-12 - Bodenindikatoren im öffentlichen Raum 
# DIN 32986 „Taktile Schriften und Beschriftungen – Anforderungen an die Darstellung und Anbringung von Braille- und erhabener Profilschrift“
# DIN 32976 „Blindenschrift – Anforderungen und Maße“ 
# https://shop.taktile-leitsysteme.de/Definitionen-Allgemeines:_:18.html

import sys
import os
import csv

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree


UNITS_ = "mm"             # or "mil"
PAD_HOLE_ENABLE   = 1
PAD_HOLE_DIAMETER = 0.25
PAD_DIAMETER      = 1.524
PAD_SPACING       = 2.7
SILK_ENABLE       = 0
SILK_BORDER       = 1
SILK_LETTER       = 1
SILK_LETTER_SIZE  = 1.0
SILK_LETTER_POS   = "top"  # or "bot"

LIB_PREAMBLE      = "BrailleFont_DIN32976"
FP_PREAMBLE       = "BrailleFont"
FP_POSTAMBLE      = "NoSilk"

# BrailleFont_letter_A_DIN32976_10mm_NoSilk

if __name__ == '__main__':
    with open('braille_characters.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        
        lib_folder = '../lib/' + LIB_PREAMBLE + '.pretty'
        os.mkdir(lib_folder)
        
        for row in spamreader:
            if("description" not in row[1]):
                desc = ''
                if(row[1].isnumeric()):
                    desc = 'number'
                elif(row[1].isalpha() or ('ä' in row[1]) or ('ö' in row[1]) or ('ü' in row[1]) or ('ß' in row[1])):
                    if(len(row[1])>2 and ('eszett' not in row[1])):
                        desc = 'symbol'
                    else:
                        desc = 'letter'
                elif(len(row[0]) > 0):
                    desc = 'symbol'
                else:
                    desc = 'function'
                
                fp_name = FP_PREAMBLE + '_' + desc + '_' + row[1].lower().replace(' ', '_') + '_' + FP_POSTAMBLE
                fp_name = fp_name.replace('__', '_')
                # print(fp_name)

                # new footprint
                fp_content = ''
                fp_content += '(module ' + fp_name + '(layer F.Cu) (tedit 613B9325)\n'
                fp_content += '  (fp_text reference REF** (at 1.35 -1.9) (layer F.SilkS) hide\n'
                fp_content += '    (effects (font (size 1 1) (thickness 0.15)))\n'
                fp_content += '  )'
                fp_content += '  (fp_text value ' + fp_name + ' (at 1.35 -3.6) (layer F.Fab)\n'
                fp_content += '    (effects (font (size 1 1) (thickness 0.15)))\n'
                fp_content += '  )'
                
                if(SILK_ENABLE and (len(row[0])>0) ):
                    if(len(row[0])<2):
                        txt = row[0].upper()
                        if(('(' in txt) or (')' in txt)):
                            txt = '"' + txt + '"'
                        fp_content += '  (fp_text user ' + txt + ' (at 1.35 7) (layer F.SilkS)\n'
                        fp_content += '    (effects (font (size 1 1) (thickness 0.15)))\n'
                        fp_content += '  )\n'
                    
                    fp_content += '  (fp_arc (start 0 0) (end 0 -1.2) (angle -90) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_arc (start 2.7 0) (end 3.9 0) (angle -90) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_arc (start 2.7 5.4) (end 2.7 6.6) (angle -90) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_arc (start 0 5.4) (end -1.2 5.4) (angle -90) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_line (start 3.9 0) (end 3.9 5.4) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_line (start -1.2 5.4) (end -1.2 0) (layer F.SilkS) (width 0.1))\n'
                    fp_content += '  (fp_line (start 0 -1.2) (end 2.7 -1.2) (layer F.SilkS) (width 0.1))\n'
                
                fp_content += '  (fp_line (start -1.95 -2.7) (end 4.65 -2.7) (layer F.CrtYd) (width 0.12))\n'
                fp_content += '  (fp_line (start -1.95 8.1) (end 4.65 8.1) (layer F.CrtYd) (width 0.12))\n'
                fp_content += '  (fp_line (start -1.95 -2.7) (end -1.95 8.1) (layer F.CrtYd) (width 0.12))\n'
                fp_content += '  (fp_line (start 4.65 -2.7) (end 4.65 8.1) (layer F.CrtYd) (width 0.12))\n'
                
                if('1' in row[2]):
                    fp_content += '  (pad "" thru_hole circle (at 0 0) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                if('1' in row[7]):
                    fp_content += '  (pad "" thru_hole circle (at 2.7 5.4) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                if('1' in row[4]):
                    fp_content += '  (pad "" thru_hole circle (at 0 2.7) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                if('1' in row[3]):
                    fp_content += '  (pad "" thru_hole circle (at 2.7 0) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                if('1' in row[6]):
                    fp_content += '  (pad "" thru_hole circle (at 0 5.4) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                if('1' in row[5]):
                    fp_content += '  (pad "" thru_hole circle (at 2.7 2.7) (size 1.524 1.524) (drill 0.25) (layers *.Cu *.Mask))\n'
                    
                fp_content += ')'
                
                f = open(lib_folder + '/' + fp_name + '.kicad_mod', 'w')
                f.write(fp_content)
                f.close()
                
                
        
    








