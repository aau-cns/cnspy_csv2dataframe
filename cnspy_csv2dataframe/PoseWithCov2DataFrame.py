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
from sys import version_info
import pandas as pandas
import numpy as np
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
import cnspy_numpy_utils.matrix_conversions as matrix_conversions

# TODOs:
# - TODO: rename to PosOrientWithCov2DataFrame, as correlation between position and orientation is missing
# - TODO: extend PosOrientWithCov2DataFrame to PoseWithCov2DataFrame supporting full upper tri 6x6 pose covariance
class PoseWithCov2DataFrame(CSV2DataFrame):
    def __init__(self, fn=None):
        # identify the covariance format via fmt=None!
        CSV2DataFrame.__init__(self, filename=fn, fmt=None)

    @staticmethod
    def DataFrame_to_TPQCov(data_frame):
        assert (isinstance(data_frame, pandas.DataFrame))
        if version_info[0] < 3:
            t_vec = data_frame.as_matrix(['t'])
            p_vec = data_frame.as_matrix(['tx', 'ty', 'tz'])
            q_vec = data_frame.as_matrix(['qx', 'qy', 'qz', 'qw'])  # JPL/Shuster
            cov_vec_T = data_frame.as_matrix(['Txx', 'Txy', 'Txz', 'Txa', 'Txb', 'Txc', 'Tyy', 'Tyz', 'Tya', 'Tyb',
                                              'Tyc', 'Tzz', 'Tza', 'Tzb', 'Tzc', 'Taa', 'Tab', 'Tac', 'Tbb', 'Tbc',
                                              'Tcc'])
        else:
            # FIX(scm): for newer versions as_matrix is deprecated, using to_numpy instead
            # from https://stackoverflow.com/questions/60164560/attributeerror-series-object-has-no-attribute-as-matrix-why-is-it-error
            t_vec = data_frame[['t']].to_numpy()
            p_vec = data_frame[['tx', 'ty', 'tz']].to_numpy()
            q_vec = data_frame[['qx', 'qy', 'qz', 'qw']].to_numpy() # JPL/Shuster
            cov_vec_T = data_frame[['Txx', 'Txy', 'Txz', 'Txa', 'Txb', 'Txc', 'Tyy', 'Tyz', 'Tya', 'Tyb', 'Tyc', 'Tzz',
                                    'Tza', 'Tzb', 'Tzc', 'Taa', 'Tab', 'Tac', 'Tbb', 'Tbc', 'Tcc']].to_numpy()
            # TODO: IMPORTANT -> reassign the indices to match tri_vec_to_mat!

        l = t_vec.shape[0]

        P_vec_T = np.zeros((l, 6, 6))

        for i in range(0, l):
            P_vec_T[i] = matrix_conversions.tri_vec_to_mat(cov_vec_T[i,], n=6)

        return t_vec, p_vec, q_vec, P_vec_T

    @staticmethod
    def TPQCov_to_DataFrame(t_vec, p_vec, q_vec, P_vec):
        t_rows, t_cols = t_vec.shape  # does not work in Python 3
        p_rows, p_cols = p_vec.shape
        q_rows, q_cols = q_vec.shape
        P_p_len, P_p_rows, P_p_cols = P_vec.shape
        assert (t_rows == p_rows)
        assert (t_rows == q_rows)
        assert (p_cols == 3)
        assert (q_cols == 4)
        assert (P_p_len == t_rows)
        assert (P_p_rows == 6 and P_p_cols == 6)

        l = t_rows
        cov_vec = np.zeros((l, 21))

        for i in range(0, l):
            # https://stackoverflow.com/questions/17527693/transform-the-upper-lower-triangular-part-of-a-symmetric-matrix-2d-array-into/58806626#58806626
            # https://stackoverflow.com/questions/8905501/extract-upper-or-lower-triangular-part-of-a-numpy-matrix
            cov_vec[i] = matrix_conversions.mat_to_tri_vec(P_vec[i])

        data_frame = pandas.DataFrame(
            {'t': t_vec[:, 0], 'tx': p_vec[:, 0], 'ty': p_vec[:, 1], 'tz': p_vec[:, 2],
             'qx': q_vec[:, 0], 'qy': q_vec[:, 1], 'qz': q_vec[:, 2], 'qw': q_vec[:, 3],
             # TODO: IMPORTANT -> reassign the indices to match tri_vec_to_mat!
             'Txx': cov_vec[:, 0], 'Txy': cov_vec[:, 1], 'Txz': cov_vec[:, 2],
             'Txa': cov_vec[:, 3], 'Txb': cov_vec[:, 4], 'Txc': cov_vec[:, 5],
             'Tyy': cov_vec[:, 6], 'Tyz': cov_vec[:, 7], 'Tya': cov_vec[:, 8],
             'Tyb': cov_vec[:, 9], 'Tyc': cov_vec[:, 10], 'Tzz': cov_vec[:, 11],
             'Tza': cov_vec[:, 12], 'Tzb': cov_vec[:, 13], 'Tzc': cov_vec[:, 14],
             'Taa': cov_vec[:, 15], 'Tab': cov_vec[:, 16], 'Tac': cov_vec[:, 17],
             'Tbb': cov_vec[:, 18], 'Tbc': cov_vec[:, 19], 'Tcc': cov_vec[:, 20],
             })
        return data_frame

        