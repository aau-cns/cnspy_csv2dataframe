# csv2dataframe Package


The class [CSV2DataFrame](CSV2DataFrame.py) is intended to load [CSV-files](https://en.wikipedia.org/wiki/Comma-separated_values) into a `pandas.DataFrame`. The CSV files need to match known formats (defined by their header in the first line) according to those defined in the package [ros_csv_formats]().  
In case no format is specified, it tries to match the first line of the CSV-File with known headers from [ros_csv_formats]() and loads the data in that format. 


## Dependencies

* [numpy]()
* [pandas]()
* [ros_csv_formats]()
* [numpy_utils]()


## License


Software License Agreement (GNU GPLv3  License), refer to the LICENSE file.

*Sharing is caring!* - [Roland Jung](https://github.com/jungr-ait)  
