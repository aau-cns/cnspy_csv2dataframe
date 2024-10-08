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

from cnspy_csv2dataframe.PosOrientWithCov2DataFrame import PosOrientWithCov2DataFrame
from cnspy_csv2dataframe.TUMCSV2DataFrame import TUMCSV2DataFrame
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
import cnspy_numpy_utils.matrix_conversions as matrix_conversions


class PoseTypedStamped2DataFrame(CSV2DataFrame):
    def __init__(self, fn=None):
        # identify the covariance format via fmt=None!
        CSV2DataFrame.__init__(self, fn=fn, fmt=None)

    @staticmethod
    def from_DataFrame(data_frame):
        assert (isinstance(data_frame, pandas.DataFrame))
        t_vec, p_vec, q_vec = TUMCSV2DataFrame.from_DataFrame(data_frame)
        if version_info[0] < 3:
            scale_vec = data_frame.as_matrix(['scale'])
            est_err_type_vec = data_frame.as_matrix(['est_err_type'])
        else:
            scale_vec = data_frame[['scale']].to_numpy()
            est_err_type_vec = data_frame[['est_err_type']].to_numpy()

        return t_vec, p_vec, q_vec, scale_vec, est_err_type_vec

    @staticmethod
    def to_DataFrame(t_vec, p_vec, q_vec, scale_vec, est_err_type_vec):
        t_rows, t_cols = t_vec.shape  # does not work in Python 3
        assert (len(est_err_type_vec) == t_rows)
        assert (len(scale_vec) == t_rows)
        p_rows, p_cols = p_vec.shape
        q_rows, q_cols = q_vec.shape
        assert (t_rows == p_rows)
        assert (t_rows == q_rows)
        assert (t_cols == 1)
        assert (p_cols == 3)
        assert (q_cols == 4)

        df1 = TUMCSV2DataFrame.to_DataFrame(t_vec, p_vec, q_vec)
        df2 = pandas.DataFrame(
            {'scale': scale_vec.tolist(), 'est_err_type': est_err_type_vec.tolist()})
        return pandas.concat([df1, df2], axis=1)
