#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Quick-Typographie-Pre-Filter: typography_latex.py

  (C)opyleft in 2019 by Norman Markgraf (nmarkgraf@hotmail.com)

  Release:
  ========
  1.0.0 - 21.02.2019 (nm) - Initial Commit


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
    DEBUGLEVEL = logging.ERROR  # .ERROR or .DEBUG  or .INFO

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

def process_line(line):
    new_line = line
    if recomp1.search(line):
        pat1_split = recomp1.split(line)
        # print(pat1_split)
        new_line = ""
        flag = False
        for part in pat1_split:
            if len(part) >= 2:
                if part[1] == ".":
                    new_line += part
                    if len(part) == 2:
                        new_line += "\\thinspace{}"
                        flag = True
                    else:
                        flag = False
                else:
                    if flag:
                        # print("***")
                        new_line = new_line.rstrip("\\thinspace{}") + " " + part
                        flag = False
                    else:
                        new_line += part
            else:
                if flag:
                    # print("---")
                    new_line = new_line.rstrip("\\thinspace{}") + " " + part
                    flag = False
                else:
                    new_line += part
        print(new_line)
    return new_line


def remove_old_backup_file(filename):
    old_backup_file = Path(filename+".bak")
    if old_backup_file.is_file():
        os.remove(old_backup_file)


def move_file_to_new_backup_file(filename):
    cur_file = Path(filename)
    if cur_file.is_file():
        new_backup_file = Path(filename+".bak")
        os.rename(cur_file, new_backup_file)


def process_backup_to_new_file(filename):
    new_file = Path(filename)
    old_file = Path(filename+".bak")
    with open(new_file, "w") as out_file:
        with open(old_file, "r") as in_file:
            for line in in_file:
                out_file.write(process_line(line))


def process_file(filename):
    remove_old_backup_file(filename)
    move_file_to_new_backup_file(filename)
    process_backup_to_new_file(filename)


def process_file_list(file_list):
    for filename in file_list:
        process_file(filename)


def main():
    """main function.
    """
    logging.debug("Start pandoc filter 'typography_latex.py'")
    parser = argparse.ArgumentParser(description='Processes LaTeX-Files to add more style and typography.')
    parser.add_argument('--dir', help='Show some help')
    process_file_list(["test.txt"])
    logging.debug("End pandoc filter 'typography_latex.py'")

if __name__ == "__main__":
    main()