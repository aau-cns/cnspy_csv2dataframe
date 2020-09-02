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
import math
import pandas as pandas
import numpy as np
from ros_csv_formats.CSVFormat import CSVFormat


class CSV2DataFrame:
    format = CSVFormat.none
    data_frame = None
    data_loaded = False
    fn = None

    def __init__(self, filename, fmt=None):
        if os.path.exists(filename):
            if fmt is None:
                fmt = CSVFormat.identify_format(filename)
            if fmt is not CSVFormat.none:
                self.format = fmt
                self.data_frame = CSV2DataFrame.load_CSV(filename, fmt)
                self.data_loaded = True
                self.fn = filename
            else:
                print("CSV2DataFrame: unknown format!")

        else:
            print("CSV2DataFrame: file does not exist: {0}".format(filename))

    def subsample(self, step=None, num_max_points=None):
        self.data_frame = CSV2DataFrame.subsample_DataFrame(self.data_frame, step=step,
                                                            num_max_points=num_max_points)

    @staticmethod
    def load_CSV(filename, fmt):
        data = pandas.read_csv(filename, sep='\s+|\,', comment='#', header=None, names=CSVFormat.get_format(fmt),
                               engine='python')
        return data

    @staticmethod
    def save_CSV(data_frame, filename, fmt, save_index=False):
        head = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(head):
            os.makedirs(head)

        data_frame.to_csv(filename, sep=',', index=save_index,
                          header=CSVFormat.get_header(fmt),
                          columns=CSVFormat.get_format(fmt))

    @staticmethod
    def subsample_DataFrame(df, step=None, num_max_points=None, verbose=False):

        num_elems = len(df.index)

        if num_max_points:
            step = 1
            if (int(num_max_points) > 0) and (int(num_max_points) < num_elems):
                step = int(math.ceil(num_elems / float(num_max_points)))

        sparse_indices = np.arange(start=0, stop=num_elems, step=step)

        if (num_max_points or step):
            if verbose:
                print("CSV2DataFrame.subsample_DataFrame():")
                print("* len: " + str(num_elems) + ", max_num_points: " + str(
                    num_max_points) + ", subsample by: " + str(step))

            df_sub = df.loc[sparse_indices]
            df_sub.reset_index(inplace=True)

            return df_sub

        else:
            return df


########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest


class CSV2DataFrame_Test(unittest.TestCase):
    def test_CTOR(self):
        d1 = CSV2DataFrame('../test/example/gt.csv')
        self.assertTrue(d1.format == CSVFormat.TUM)

        d2 = CSV2DataFrame("/home/jungr/workspace/CNS/aaucns_scripts/matlab/results/TUM_test.csv", fmt=CSVFormat.TUM)
        self.assertTrue(d2.format == CSVFormat.TUM)


if __name__ == '__main__':
    unittest.main()
