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
import math
import pandas as pandas
import numpy as np
from cnspy_spatial_csv_formats.CSVSpatialFormat import CSVSpatialFormat
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType


class CSV2DataFrame:
    format = CSVSpatialFormat()
    data_frame = None
    data_loaded = False
    fn = None

    def __init__(self, filename=None, fmt=None):
        if filename is None:
            pass  # Do nothing.. data can be loaded later on!
        else:
            self.load_from_CSV(fn=filename, fmt_type=fmt)

    def subsample(self, step=None, num_max_points=None):
        if self.data_loaded:
            self.data_frame = CSV2DataFrame.subsample_DataFrame(self.data_frame, step=step,
                                                                num_max_points=num_max_points)
        else:
            print("CSV2DataFrame: data was not loaded!")

    def load_from_CSV(self, fn, fmt_type=None):
        """

        Parameters
        ----------
        fn
        fmt_type: allows to load a CSV is a manually specified format; if not specified the format is automatically
        identified.

        Returns: True/False
        -------

        """
        if os.path.exists(fn):
            if fmt_type is not None:
                assert(isinstance(fmt_type, CSVSpatialFormatType) or isinstance(fmt_type, CSVSpatialFormat))

                if isinstance(fmt_type, CSVSpatialFormatType):
                    fmt_ = CSVSpatialFormat(fmt_type=fmt_type)
                elif isinstance(fmt_type, CSVSpatialFormat):
                    fmt_ = fmt_type
            else:
                # use the already specified format
                fmt_ = self.format

            # if the format type is not known (none) then try to identify it:
            if fmt_.type is CSVSpatialFormatType.none:
                fmt_ = CSVSpatialFormat.identify_format(fn)

            # if the format is still not known it cannot be loaded
            if fmt_.type is not CSVSpatialFormatType.none:
                self.data_frame = CSV2DataFrame.load_CSV(filename=fn, fmt=fmt_)
                self.fn = fn
                self.data_loaded = True
                self.format = fmt_
                return True
        else:
            print("CSV2DataFrame.load_from_CSV(): file does not exist: {0}".format(fn))

        # default assignment
        self.data_frame = None
        self.fn = None
        self.data_loaded = False
        self.format = CSVSpatialFormat()
        return False

    def save_to_CSV(self, fn, fmt=None):
        if fmt is None or not isinstance(fmt, CSVSpatialFormat):
            fmt_ = self.format

        if self.data_loaded:
            CSV2DataFrame.save_CSV(data_frame=self.data_frame, filename=fn, fmt=fmt_)
        else:
            print("CSV2DataFrame: data was not loaded!")

    @staticmethod
    def load_CSV(filename, fmt):
        if isinstance(fmt, CSVSpatialFormatType):
            data = pandas.read_csv(filename, sep='\s+|\,', comment='#', header=None,
                                   names=CSVSpatialFormatType.get_format(fmt),
                                   engine='python')
        elif isinstance(fmt, CSVSpatialFormat):
            data = pandas.read_csv(filename, sep='\s+|\,', comment='#', header=None,
                                   names=fmt.get_format(),
                                   engine='python')

        return data

    @staticmethod
    def save_CSV(data_frame, filename, fmt, save_index=False):
        head = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(head):
            os.makedirs(head)

        if isinstance(fmt, CSVSpatialFormatType):
            data_frame.to_csv(filename, sep=',', index=save_index,
                              header=CSVSpatialFormatType.get_header(fmt),
                              columns=CSVSpatialFormatType.get_format(fmt))
        elif isinstance(fmt, CSVSpatialFormat):
            data_frame.to_csv(filename, sep=',', index=save_index,
                              header=fmt.get_header(),
                              columns=fmt.get_format())

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

