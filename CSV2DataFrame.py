#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Requirements:
# sudo pip install numpy pandas
########################################################################################################################
import os
from ros_csv_formats.CSVFormat import CSVFormat
from TUMCSV2DataFrame import TUMCSV2DataFrame
from PoseCovCSV2DataFrame import PoseCovCSV2DataFrame


class CSV2DataFrame:
    format = CSVFormat.none
    df = None

    def __init__(self, fn):
        fmt = CSVFormat.identify_format(fn)
        if fmt is not CSVFormat.none:
            self.format = fmt
            if fmt == CSVFormat.TUM:
                self.df = TUMCSV2DataFrame.load_CSV(fn)

            elif fmt == CSVFormat.PoseCov:
                self.df = PoseCovCSV2DataFrame.load_CSV(fn)
            else:
                print('CSV2DataFrame: format {0} not supported!'.format(fmt))
                self.format = CSVFormat.none


########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest


class CSV2DataFrame_Test(unittest.TestCase):
    def test_CTOR(self):
        d1 = CSV2DataFrame('../test/example/gt.csv')
        self.assertTrue(d1.format == CSVFormat.TUM)


if __name__ == '__main__':
    unittest.main()
