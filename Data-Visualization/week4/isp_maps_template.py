"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    plot_country_codes = {}
    separator = codeinfo["separator"]
    with open(codeinfo["codefile"], newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=codeinfo["quote"])
        for row in csvreader:
            plot_country_codes.update({row[codeinfo["plot_codes"]]: row[codeinfo["data_codes"]]})

    return plot_country_codes


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    matched_dictionary = {}
    not_matched_set = set()
    separator = codeinfo["separator"]
    nested_dict = {}
    with open(codeinfo["codefile"], newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=codeinfo["quote"])
        for row in csvreader:
            rowid = row[codeinfo["plot_codes"]].lower()
            nested_dict[rowid] = row
    for countries in plot_countries:
        if countries.lower() in nested_dict or countries.upper() in nested_dict:
            if nested_dict[countries.lower()][codeinfo["data_codes"]].upper() in gdp_countries or nested_dict[countries.lower()][codeinfo["data_codes"]].lower() in gdp_countries:
                gdp_code = nested_dict[countries.lower()][codeinfo["data_codes"]]
                matched_dictionary.update({countries: gdp_code})
            else:
                not_matched_set.add(countries)
        else:
            not_matched_set.add(countries)
    return matched_dictionary, not_matched_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_dict = {}
    nested_dict = {}
    gdp_not_found_set = set()
    separator = gdpinfo["separator"]
    with open(gdpinfo["gdpfile"], newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=gdpinfo["quote"])
        for row in csvreader:
            rowid = row[gdpinfo["country_code"]]
            gdp_dict[rowid] = row
        print(gdp_dict)
        matched_country_dict, not_matched_set = reconcile_countries_by_code(codeinfo, plot_countries, gdp_dict)
        print(matched_country_dict)
        for match in matched_country_dict:
            country_name = matched_country_dict[match].upper()
            if year in gdp_dict[country_name] and gdp_dict[country_name][year] != '':
                gdp = float(gdp_dict[country_name][year])
                nested_dict.update({match: math.log10(gdp)})
            else:
                gdp_not_found_set.add(match)
    return nested_dict, not_matched_set, gdp_not_found_set


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")

# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()

