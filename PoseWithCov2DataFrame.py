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
import numpy as np
import pandas as pandas
from numpy_utils.matrix_conversions import *


class PoseWithCov2DataFrame(CSV2DataFrame):
    def __init__(self, fn=None):
        CSV2DataFrame.__init__(self, filename=fn, fmt=CSVFormat.PoseWithCov)

    def load_from_CSV(self, fn):
        if os.path.exists(fn):
            self.data_frame = CSV2DataFrame.load_CSV(filename=fn, fm=CSVFormat.PoseWithCov)
            self.data_loaded = True

    def save_to_CSV(self, fn):
        CSV2DataFrame.save_CSV(self.data_frame, filename=fn, format=CSVFormat.PoseWithCov)

    @staticmethod
    def DataFrame_to_TPQCov(data_frame):
        t_vec = data_frame.as_matrix(['t'])
        p_vec = data_frame.as_matrix(['tx', 'ty', 'tz'])
        q_vec = data_frame.as_matrix(['qx', 'qy', 'qz', 'qw'])
        cov_vec_p = data_frame.as_matrix(['pxx', 'pxy', 'pxz', 'pyy', 'pyz', 'pzz'])
        cov_vec_q = data_frame.as_matrix(['qrr', 'qrp', 'qry', 'qpp', 'qpy', 'qyy'])

        l = t_vec.shape[0]

        P_vec_p = np.zeros((l, 3, 3))
        P_vec_q = np.zeros((l, 3, 3))
        # P_vec_p[:, ] = tri_vec_to_mat(cov_vec_p[:, ], n=3)

        for i in range(0, l):
            P_vec_p[i] = tri_vec_to_mat(cov_vec_p[i,], n=3)
            P_vec_q[i] = tri_vec_to_mat(cov_vec_q[i,], n=3)

        return t_vec, p_vec, q_vec, P_vec_p, P_vec_q

    @staticmethod
    def TPQCov_to_DataFrame(t_vec, p_vec, q_vec, P_vec_p, P_vec_q):
        t_rows, t_cols = t_vec.shape  # does not work in Python 3
        p_rows, p_cols = p_vec.shape
        q_rows, q_cols = q_vec.shape
        P_p_len, P_p_rows, P_p_cols = P_vec_p.shape
        assert (t_rows == p_rows)
        assert (t_rows == q_rows)
        assert (p_cols == 3)
        assert (q_cols == 4)
        assert (P_p_len == t_rows)
        assert (P_p_rows == 3 and P_p_cols == 3)
        assert (P_vec_p.shape == P_vec_q.shape)

        l = t_rows
        cov_vec_p = np.zeros((l, 6))
        cov_vec_q = np.zeros((l, 6))
        for i in range(0, l):
            cov_vec_p[i] = mat_to_tri_vec(P_vec_p[i])
            cov_vec_q[i] = mat_to_tri_vec(P_vec_q[i])

        data_frame = pandas.DataFrame(
            {'t': t_vec[:, 0], 'tx': p_vec[:, 0], 'ty': p_vec[:, 1], 'tz': p_vec[:, 2],
             'qx': q_vec[:, 0], 'qy': q_vec[:, 1], 'qz': q_vec[:, 2], 'qw': q_vec[:, 3],
             'pxx': cov_vec_p[:, 0], 'pxy': cov_vec_p[:, 1], 'pxz': cov_vec_p[:, 2], 'pyy': cov_vec_p[:, 3],
             'pyz': cov_vec_p[:, 4], 'pzz': cov_vec_p[:, 5],
             'qrr': cov_vec_q[:, 0], 'qrp': cov_vec_q[:, 1], 'qry': cov_vec_q[:, 2], 'qpp': cov_vec_q[:, 3],
             'qpy': cov_vec_q[:, 4], 'qyy': cov_vec_q[:, 5]})
        return data_frame


# https://stackoverflow.com/questions/17527693/transform-the-upper-lower-triangular-part-of-a-symmetric-matrix-2d-array-into/58806626#58806626
# https://stackoverflow.com/questions/8905501/extract-upper-or-lower-triangular-part-of-a-numpy-matrix

########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest
import time


class PoseWithCov2DataFrame_Test(unittest.TestCase):
    start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        print("Process time: " + str((time.time() - self.start_time)))

    def load_(self):
        print('loading...')
        fn = '../sample_data/ID1-pose-est-cov.csv'
        obj = PoseWithCov2DataFrame(fn=fn)
        return obj

    def test_load_trajectory_from_CSV(self):
        obj = self.load_()
        self.assertTrue(obj.data_loaded)
        self.start()
        t_vec, p_vec, q_vec, P_vec_p, P_vec_q = PoseWithCov2DataFrame.DataFrame_to_TPQCov(obj.data_frame)
        self.stop()

        print(P_vec_p[1000])
        print(P_vec_q[1000])
        print(p_vec[1000])
        print(q_vec[1000])


if __name__ == "__main__":
    unittest.main()
