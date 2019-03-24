#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Quick-Typographie-Pre-Filter: typography_latex.py

  (C)opyleft in 2019 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  1.0.0 - 21.02.2019 (nm) - Initial Commit
  1.0.1 - 22.02.2019 (nm) - Kleine Erweiterungen.
  1.0.2 - 24.02.2019 (nm) - Jetzt auch mit Dateilisten via "*.txt". Aber 
                            kleine Unterverzeichnisse!
  1.1.0 - 26.02.2019 (nm) - Jetzt werden vor und nach alleinstehenden "/" ein
                            kleines Leerzeichen eingefügt.
  1.1.1 - 01.03.2019 (nm) - Bugfix release. -- ENDLICH!
  1.2.0 - 08.03.2019 (nm) - Bugfix release. "(z.B." etc. wird nun korrekt behandelt.
                            Codeblöcke werden nun nicht mehr bearbeitet.
  1.3.0 - 09.03.2019 (nm) - mit "-mg" auf "\," statt "\thinspace{}" umschalten.
  1.4.0 - 23.03.2019 (nm) - R Codeausdrücke "\Sexpr{...}" werden erkannt und nicht behandelt.
  1.4.1 - 24.03.2019 (nm) - "\verb" ausbrücke werden korrekt behandelt.
                            


  WICHTIG:
  ========
    Benoetigt python3 !
    -> https://www.howtogeek.com/197947/how-to-install-python-on-windows/
    oder
    -> https://www.youtube.com/watch?v=dX2-V2BocqQ
    Bei *nix und macOS Systemen muss diese Datei als "executable" markiert
    sein!
    Also bitte ein
      > chmod a+x typography_latex.py
   ausfuehren!

  LaTeX:
  ======
  Der Befehl "xspace" benötigst das Paket "xspace".
  Also bitte "usepackage{xspace}" einbauen!

  Informationen zur Typographie:
  ==============================
  URL: https://www.korrekturen.de/fehler_und_stilblueten/die_sieben_haeufigsten_typographie-suenden.shtml
  URL: http://www.typolexikon.de/abstand/
  URL: https://de.wikipedia.org/wiki/Schmales_Leerzeichen


  Lizenz:
  =======
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from pathlib import Path
from _version import __version__


import shutil

import os as os  # check if file exists.
import re as re  # re fuer die Regulaeren Ausdruecke

import logging  # logging fuer die 'typography.log'-Datei
import argparse  # parsing die argumente


# Eine Log-Datei "typography_latex.log" erzeugen um einfacher zu debuggen
if os.path.exists("typography_latex.loglevel.debug"):
    DEBUGLEVEL = logging.DEBUG
elif os.path.exists("typography_latex.loglevel.info"):
    DEBUGLEVEL = logging.INFO
elif os.path.exists("typography_latex.loglevel.warning"):
    DEBUGLEVEL = logging.WARNING
elif os.path.exists("typography_latex.loglevel.error"):
    DEBUGLEVEL = logging.ERROR
else:
    DEBUGLEVEL = logging.DEBUG  # .ERROR or .DEBUG  or .INFO

logging.basicConfig(filename='typography_latex.log', level=DEBUGLEVEL)


"""
 Suchmuster (pattern) für die einzelnen Situationen

 pattern1
 ========

 Dieses Pattern sucht nach x.y. in den Fassungen:
    x.y. / (x.y. / (x.y.: / (x.y.) / x.y.: ...
 für alle Buchstaben x und y abdecken.
 Wichtig ... \D, damit keine Datumsangaben in die Mangel genommen werden!
 So soll z.B. 15.9.  eben _nicht_ in Muster fallen!
"""
pattern1 = "([\(,\[,<,\{]?\w\.)\ ?(?:[~|\xa0]?)(\D\.[\),\],>]?[:,\,,\.,\!,\?]?[\),\],\},>]?)"
recomp1 = re.compile(pattern1)

pattern2 = "^<<.*>>="
recomp2 = re.compile(pattern2)

pattern3 = "^@"
recomp3 = re.compile(pattern3)

pattern4 = r"\\verb(?P<verbs>\S)(.*?)(?P=verbs)" #"\\verb(?P<verbs>\S)(.*?)(?P=verbs)"
#pattern4 = "\\verb@(.+?)@"
recomp4 = re.compile(pattern4)

pattern5 = "\\Sexpr{(.*?)}"
recomp5 = re.compile(pattern5)

thinspace_mg = "\\,"
thinspace_nm = "\\thinspace{}"
thinspace = thinspace_nm

in_code_block = False

def get_backup_filename(filename):
    tmp_path = Path(filename)
    return tmp_path.with_suffix(tmp_path.suffix + ".bak")


def process_line_points(line):
    global thinspace
    logging.debug("Process_line_points:"+str(line))
    new_line = line
    if recomp1.search(line):
        pat1_split = recomp1.split(line)
        logging.debug("->splitting:"+str(pat1_split))
        new_line = ""
        flag = False
        for part in pat1_split:
            if len(part) >= 2:
                if part[1] == "." or (part[0] in ("(", "[", "{") and part[2] == "."):
                    new_line += part
                    if len(part) == 2 or (len(part) == 3 and part[0] in ("(", "[", "{")):
                        new_line += thinspace
                        flag = True
                    else:
                        flag = False
                else:
                    if flag:
                        # print("***")
                        new_line = new_line.rstrip(thinspace) + part
                        flag = False
                    else:
                        new_line += part
            else:
                if flag:
                    # print("---")
                    new_line = new_line.rstrip(thinspace) + " " + part
                    flag = False
                else:
                    new_line += part
        # print(new_line)
    return new_line


def process_line_sexpr(line): 
    logging.debug("Process_line_sexpr:"+str(line))
    pat5_split = recomp5.split(line)
    logging.debug("->splitting:"+str(pat5_split))
    newline = ""
    flag = False
    for part in pat5_split:
        if flag:
            newline += "Sexpr{" 
            newline += part
        else:
            newline += process_line_slashes(process_line_points(part))
        if flag:
            newline += "}"
            flag = False
        else:
            flag = True
    return newline
    

def process_line_verb(line): 
    logging.debug("Process_line_verb:" + str(line))
    pat4_split = recomp4.split(line)
    logging.debug("->splitting:"+str(pat4_split))
    newline = ""
    lim = ""
    count = 0
    for part in pat4_split:
        if count == 3:
            newline += lim
            count = 0
        if count == 2:
            newline += part
            count = 3
        if count == 1:
            newline += "\\verb"
            lim = part
            newline += part
            count = 2
        if count == 0:
            newline += process_line_sexpr(part)
            count = 1
    return newline


def process_line_slashes(line):
    global thinspace
    new_line = line
    chunks = line.split(" / ")
    if len(chunks) > 1:
        new_line = ""
        for chunk in chunks:
            new_line += chunk
            new_line += thinspace+"/"+thinspace
    return new_line


def start_code_block(line):
    return recomp2.search(line)


def end_code_block(line):
    return recomp3.search(line)


def has_sexpr(line):
    return recomp5.search(line)

def process_line(line):
    global in_code_block

    logging.debug("Process line with code_block_flag: "+ str(in_code_block) )

    if start_code_block(line):
        in_code_block = True
        logging.debug("Start of Codeblock!")

    if in_code_block:
        if end_code_block(line):
            logging.debug("End of Codeblock!")
            in_code_block = False
        logging.debug("Simply return line!")
        return line

    logging.debug("process sub functions!")
    
    return process_line_verb(line)


def remove_old_backup_file(filename):
    logging.debug("Process remove_old_backup_file")
    old_backup_file = get_backup_filename(filename)
    if old_backup_file.is_file():
        logging.debug("Remove/delete "+str(old_backup_file))
        os.remove(old_backup_file)


def move_file_to_new_backup_file(filename):
    logging.debug("Process move_file_to_new_backup_file")
    cur_file = Path(filename)
    if cur_file.is_file():
        new_backup_file = get_backup_filename(filename)
        logging.debug("Move "+str(cur_file)+" to "+str(new_backup_file))
        os.rename(cur_file, new_backup_file)


def process_backup_to_new_file(filename):
    logging.debug("Process process_backup_to_new_file")
    new_file = Path(filename)
    old_file = get_backup_filename(filename)
    logging.debug("Process backup file "+str(old_file)+" to new file "+str(new_file))
    with open(new_file, "w") as out_file:
        with open(old_file, "r") as in_file:
            for line in in_file:
                out_file.write(process_line(line))


def copy_backup_to_file(filename):
    logging.debug("Process copy_backup_to_file")
    cur_file = Path(filename)
    backup_file = get_backup_filename(filename)
    if cur_file.is_file():
        logging.debug("Remove "+str(cur_file))
        os.remove(cur_file)
    logging.debug("Copy "+str(backup_file)+" to "+str(cur_file))
    shutil.copy2(backup_file, cur_file)


def move_backup_to_file(filename):
    logging.debug("Process move_backup_to_file")
    cur_file = Path(filename)
    backup_file = get_backup_filename(filename)
    if cur_file.is_file():
        logging.debug("Remove "+str(cur_file))
        os.remove(cur_file)
    logging.debug("Rename "+str(backup_file)+" to "+str(cur_file))
    os.rename(backup_file, cur_file)


def process_file_undo(filename, force=False):
    logging.debug("Process process_file_undo")
    if force:
        move_backup_to_file(filename)
    else:
        copy_backup_to_file(filename)


def process_file_normal(filename, force_backup=False):
    logging.debug("Process process_file_normal")
    if force_backup:
        remove_old_backup_file(filename)
    move_file_to_new_backup_file(filename)
    process_backup_to_new_file(filename)


def process_file(filename, force_backup=False, undo=False):
    logging.info(
        "Process file "+str(filename)+"\t force_backup: "+str(force_backup)+"\t undo: "+str(undo)
    )
    undo_backup = undo
    if undo:  
        process_file_undo(filename, force_backup)
    else:
        process_file_normal(filename, force_backup)


def process_file_list(file_list, force_backup=False, undo=False):
    logging.debug(
        "Process file list"+str(file_list)+"\t force_backup: "+str(force_backup)+"\t undo: "+str(undo)
    )
    for filename in file_list:
        process_file(filename, force_backup, undo)


def main():
    """main function.
    """
    global thinspace
    global thinspace_nm
    global thinspace_mg
    
    logging.info("Start pandoc filter 'typography_latex.py'")

    parser = argparse.ArgumentParser(description='Processes LaTeX-Files to add more style and typography.')

    parser.add_argument('-u', '--undo',
                        help="undo via copy",
                        action="store_true",
                        dest="undo",
                        default=False)
    parser.add_argument('-f', '--force',
                        help="force overwrite backup file",
                        action="store_true",
                        dest="force",
                        default=False)
    parser.add_argument('-mg', '--mgversion',
                        help="use \\, instead of \\thinspace{}",
                        action="store_true",
                        dest="mgversion",
                        default=False)
    parser.add_argument('-v', '--version',
                        help="print version information",
                        action='version',
                        version='%(prog)s release {version}'.format(version=__version__))
    parser.add_argument('file',
                        help='filename(s)',
                        nargs="+",
                        default=None)

    args = parser.parse_args()

    # print([Path(x) for x in args.file if Path(x).is_file()])
    
    if args.mgversion:
        thinspace = thinspace_mg  # Mathias Gehrke Version
    else:
        thinspace = thinspace_nm  # default aka Norman Markgraf Version
    
    logging.debug(
        "force: "+str(args.force)+"\t undo: "+str(args.undo)
    )
    
    process_file_list(
        [Path(x) for x in args.file if Path(x).is_file()],
        force_backup=args.force, 
        undo=args.undo
    )
    
    logging.info("End pandoc filter 'typography_latex.py'")


if __name__ == "__main__":
    main()
