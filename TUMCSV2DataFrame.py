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
from ros_csv_formats.CSVFormat import CSVFormat
from CSV2DataFrame import CSV2DataFrame


class TUMCSV2DataFrame(CSV2DataFrame):
    def __init__(self, fn=None):
        CSV2DataFrame.__init__(self, filename=fn, fmt=CSVFormat.TUM)

    def load_from_CSV(self, fn):
        if os.path.exists(fn):
            self.data_frame = CSV2DataFrame.load_CSV(filename=fn, fm=CSVFormat.TUM)
            self.data_loaded = True

    def save_to_CSV(self, fn):
        CSV2DataFrame.save_CSV(self.data_frame, filename=fn, format=CSVFormat.TUM)

    @staticmethod
    def DataFrame_to_numpy_dict(df):
        np_dict = {
            't': df[['t']].values.transpose()[0],
            'tx': df[['tx']].values.transpose()[0],
            'ty': df[['ty']].values.transpose()[0],
            'tz': df[['tz']].values.transpose()[0],
            'qx': df[['qx']].values.transpose()[0],
            'qy': df[['qy']].values.transpose()[0],
            'qz': df[['qz']].values.transpose()[0],
            'qw': df[['qw']].values.transpose()[0]
        }
        return np_dict

    @staticmethod
    def DataFrame_to_TPQ(data_frame):
        t_vec = data_frame.as_matrix(['t'])
        p_vec = data_frame.as_matrix(['tx', 'ty', 'tz'])
        q_vec = data_frame.as_matrix(['qx', 'qy', 'qz', 'qw'])

        return t_vec, p_vec, q_vec

    @staticmethod
    def TPQ_to_DataFrame(t_vec, p_vec, q_vec):
        t_rows, t_cols = t_vec.shape
        p_rows, p_cols = p_vec.shape
        q_rows, q_cols = q_vec.shape
        assert (t_rows == p_rows)
        assert (t_rows == q_rows)
        assert (t_cols == 1)
        assert (p_cols == 3)
        assert (q_cols == 4)

        data_frame = pandas.DataFrame(
            {'t': t_vec[:, 0], 'tx': p_vec[:, 0], 'ty': p_vec[:, 1], 'tz': p_vec[:, 2], 'qx': q_vec[:, 0],
             'qy': q_vec[:, 1], 'qz': q_vec[:, 2], 'qw': q_vec[:, 3]})
        return data_frame


########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest
import numpy as np


class TUMCSVdata_Test(unittest.TestCase):
    def load_sample_data_frame(self):
        return TUMCSV2DataFrame(
            filename='../test/example/gt.csv')

    def test_load_from_CSV(self):
        print('loading...')
        d = self.load_sample_data_frame()
        self.assertTrue(d.data_loaded)

        d = TUMCSV2DataFrame(filename='no file')
        self.assertFalse(d.data_loaded)

    def test_data_to_numpy_dict(self):
        d = self.load_sample_data_frame()
        np_dict = TUMCSV2DataFrame.DataFrame_to_numpy_dict(d.data_frame)

        self.assertTrue(len(np_dict['t']) > 100)

    def test_data_to_tqp(self):
        d = self.load_sample_data_frame()
        t_vec, p_vec, q_vec = TUMCSV2DataFrame.DataFrame_to_TPQ(d.data_frame)

        self.assertTrue(len(t_vec) > 0)
        self.assertTrue(len(t_vec) == len(p_vec))

    def test_tpq_to_data_frame(self):
        p_vec = np.array([[21, 72, 67],
                          [23, 78, 69],
                          [32, 74, 56],
                          [52, 54, 76]])
        q_vec = np.array([[0, 0, 0, 1],
                          [0, 0, 0, 1],
                          [0, 0, 0, 1],
                          [0, 0, 0, 1]])
        t_vec = np.array([[0],
                          [1],
                          [2],
                          [3]])
        df = TUMCSV2DataFrame.TPQ_to_DataFrame(t_vec, p_vec, q_vec)
        print(str(df))
        CSV2DataFrame.save_CSV(data_frame=df, filename='../results/any.csv', format=CSVFormat.TUM)

    def test_subsample_DataFrame(self):
        d = self.load_sample_data_frame()

        num_samples = 200
        df_sub = TUMCSV2DataFrame.subsample_DataFrame(d.data_frame, num_max_points=200, verbose=True)

        self.assertTrue(len(df_sub.index) <= num_samples)

        CSV2DataFrame.save_CSV(data_frame=df_sub, filename='../results/gt_sub_200.csv', format=CSVFormat.TUM)


if __name__ == "__main__":
    unittest.main()
