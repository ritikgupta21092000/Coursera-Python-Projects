"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    nested_dict = {}

    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            nested_dict[rowid] = row
    return nested_dict


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    sorted_list = []
    minimum_year = gdpinfo["min_year"]
    maximum_year = gdpinfo["max_year"]
    for row in range(minimum_year, maximum_year + 1):
        for year in gdpdata:
            if str(row) == year and gdpdata[year] != '':
                year_gdp_tuple = (int(year), float(gdpdata[year]))
                sorted_list.append(year_gdp_tuple)
    return sorted_list


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    mapped_dictionary = {}
    year_dict = {}
    file_name = gdpinfo["gdpfile"]
    name_keyfield = gdpinfo["country_name"]
    sep = gdpinfo["separator"]
    country_nested_dict = read_csv_as_nested_dict(file_name, name_keyfield, sep, gdpinfo["quote"])
    for name_of_country in country_list:
        if name_of_country in country_nested_dict:
            for row in country_nested_dict:
                if row == name_of_country:
                    for year in range(gdpinfo["min_year"], gdpinfo["max_year"] + 1):
                        year_dict.update({str(year): country_nested_dict[row][str(year)]})
                    year_tup = build_plot_values(gdpinfo, year_dict)
                    mapped_dictionary.update({name_of_country: year_tup})
        else:
            mapped_dictionary.update({name_of_country: []})

    return mapped_dictionary


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    country_mapped_dict = build_plot_dict(gdpinfo, country_list)
    xyplot = pygal.XY(x_title="Year", y_title="GDP in current US dollars")
    xyplot.title = "Plot of GDP for select countries spanning 1960 to 2015"
    for country_name in country_list:
        coords = [(xval, yval) for xval, yval in country_mapped_dict[country_name]]
        xyplot.add(country_name, coords)
    xyplot.render_to_file(plot_file)
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")

# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()

