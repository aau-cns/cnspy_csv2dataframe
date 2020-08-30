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
import pandas as pandas
from csv2dataframe.TUMCSV2DataFrame import TUMCSV2DataFrame
from ros_csv_formats.CSVFormat import CSVFormat


class PoseCovCSV2DataFrame:
    data_frame = None
    data_loaded = False

    def __init__(self, filename=None):
        if filename:
            self.load_from_CSV(filename=filename)

    def load_from_CSV(self, filename):
        if os.path.exists(filename):
            self.data_frame = PoseCovCSV2DataFrame.load_CSV(filename=filename)
            self.data_loaded = True

    def save_to_CSV(self, filename):
        PoseCovCSV2DataFrame.save_CSV(self.data_frame, filename=filename)

    def subsampe(self, step=None, num_max_points=None):
        self.data_frame = TUMCSV2DataFrame.subsample_DataFrame(self.data_frame, step=step,
                                                               num_max_points=num_max_points)

    @staticmethod
    def load_CSV(filename, sep='\s+|\,', comment='#',
                 header=CSVFormat.get_format(CSVFormat.PoseCov)):
        data = pandas.read_csv(filename, sep=sep, comment=comment, header=None, names=header, engine='python')
        return data

    @staticmethod
    def save_CSV(data_frame, filename, save_index=False):
        head = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(head):
            os.makedirs(head)

        data_frame.to_csv(filename, sep=',', index=save_index,
                          header=CSVFormat.get_header(CSVFormat.PoseCov),
                          columns=CSVFormat.get_format(CSVFormat.PoseCov))
