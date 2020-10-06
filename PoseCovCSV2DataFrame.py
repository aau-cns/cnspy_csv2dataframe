#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
#
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
from csv2dataframe.CSV2DataFrame import CSV2DataFrame


class PoseCovCSV2DataFrame(CSV2DataFrame):
    def __init__(self, fn=None):
        CSV2DataFrame.__init__(self, filename=fn, fmt=CSVFormat.PoseCov)

    def load_from_CSV(self, fn):
        if os.path.exists(fn):
            self.data_frame = PoseCovCSV2DataFrame.load_CSV(fn=fn, fm=CSVFormat.PoseCov)
            self.data_loaded = True

    def save_to_CSV(self, fn):
        PoseCovCSV2DataFrame.save_CSV(self.data_frame, fn=fn, format=CSVFormat.PoseCov)
