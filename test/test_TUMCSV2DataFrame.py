########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest
import numpy as np
from csv2dataframe.TUMCSV2DataFrame import TUMCSV2DataFrame
from csv2dataframe.CSV2DataFrame import CSV2DataFrame
from spatial_csv_formats.CSVFormatPose import CSVFormatPose

class TUMCSVdata_Test(unittest.TestCase):
    def load_sample_data_frame(self):
        return TUMCSV2DataFrame(fn='./sample_data/ID1-pose-gt.csv')

    def test_load_from_CSV(self):
        print('loading...')
        d = self.load_sample_data_frame()
        self.assertTrue(d.data_loaded)

        d = TUMCSV2DataFrame(fn='no file')
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
        CSV2DataFrame.save_CSV(data_frame=df, filename='./sample_data/results/any.csv', fmt=CSVFormatPose.TUM)

    def test_subsample_DataFrame(self):
        d = self.load_sample_data_frame()

        num_samples = 200
        df_sub = TUMCSV2DataFrame.subsample_DataFrame(d.data_frame, num_max_points=200, verbose=True)

        self.assertTrue(len(df_sub.index) <= num_samples)

        CSV2DataFrame.save_CSV(data_frame=df_sub, filename='./sample_data/results/gt_sub_200.csv',
                               fmt=CSVFormatPose.TUM)


if __name__ == "__main__":
    unittest.main()
