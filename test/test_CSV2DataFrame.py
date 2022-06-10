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
########################################################################################################################
import os
import unittest
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_spatial_csv_formats.EstimationErrorType import EstimationErrorType
from cnspy_spatial_csv_formats.ErrorRepresentationType import ErrorRepresentationType

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class CSV2DataFrame_Test(unittest.TestCase):
    def test_CTOR(self):
        d1 = CSV2DataFrame(str(SAMPLE_DATA_DIR + '/ID1-pose-gt.csv'))
        self.assertTrue(d1.format.type == CSVSpatialFormatType.TUM)
        self.assertTrue(d1.data_loaded)
        d2 = CSV2DataFrame(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov.csv'), fmt=CSVSpatialFormatType.PosOrientWithCov)
        self.assertTrue(d2.format.type == CSVSpatialFormatType.PosOrientWithCov)
        self.assertTrue(d2.data_loaded)

        d3 = CSV2DataFrame()
        d3.load_from_CSV(fn=str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov.csv'))
        self.assertTrue(d3.data_loaded)
        self.assertTrue(d3.format.type == CSVSpatialFormatType.PosOrientWithCov)
        d3.save_to_CSV(fn=str(SAMPLE_DATA_DIR + '/results/ID1-pose-est-cov.COPY.csv'))

    def test_formats(self):
        d4 = CSV2DataFrame()
        d4.load_from_CSV(fn=str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov-type1-thetaR.csv'))
        self.assertTrue(d4.data_loaded)
        self.assertTrue(d4.format.type == CSVSpatialFormatType.PosOrientWithCov)
        self.assertTrue(d4.format.estimation_error_type == EstimationErrorType.type1)
        self.assertTrue(d4.format.rotation_error_representation == ErrorRepresentationType.R_small_theta)

        d5 = CSV2DataFrame()
        d5.load_from_CSV(fn=str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov-type2-thetaq.csv'))
        self.assertTrue(d5.data_loaded)
        self.assertTrue(d5.format.type == CSVSpatialFormatType.PosOrientWithCov)
        self.assertTrue(d5.format.estimation_error_type == EstimationErrorType.type2)
        self.assertTrue(d5.format.rotation_error_representation == ErrorRepresentationType.q_small_theta)

    def test_wrong_format_type(self):
        d2 = CSV2DataFrame(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov.csv'), fmt=CSVSpatialFormatType.PosOrientCov)
        self.assertTrue(d2.data_loaded)
        self.assertTrue(d2.format.type == CSVSpatialFormatType.PosOrientCov)
        d2.save_to_CSV(fn=str(SAMPLE_DATA_DIR + '/results/ID1-pose-cov-wrong.COPY.csv'))



    def test_not_existing_file(self):
        d6 = CSV2DataFrame()
        d6.load_from_CSV(fn=str(SAMPLE_DATA_DIR + '/123123123123.csv'))
        self.assertFalse(d6.data_loaded)

if __name__ == '__main__':
    unittest.main()
