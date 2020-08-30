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


class CSV2DataFrame:
    def __init__(self):
        pass

    @staticmethod
    def identify_format(fn):
        if os.path.exists(fn):
            with open(fn, "r") as file:
                header = str(file.readline()).rstrip("\n\r")
                for fmt in list(CSVFormat):
                    h_ = ",".join(CSVFormat.get_header(fmt))
                    if h_.replace(" ", "") == header.replace(" ", ""):
                        return CSVFormat(fmt)

        return CSVFormat.none


########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest


class CSV2DataFrame_Test(unittest.TestCase):
    def test_identify(self):
        fmt = CSV2DataFrame.identify_format('../test/example/gt.csv')
        print('identify_format:' + str(fmt))
        fmt = CSV2DataFrame.identify_format('../test/example/sensor_PoseCov.csv')
        print('identify_format:' + str(fmt))
        fmt = CSV2DataFrame.identify_format('../test/example/uwb.csv')
        print('identify_format:' + str(fmt))


if __name__ == '__main__':
    unittest.main()
