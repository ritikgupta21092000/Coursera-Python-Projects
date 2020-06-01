"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    matched_countries_dict = {}
    not_matched_countries_set = set()
    for countries_plot in plot_countries:
        if plot_countries[countries_plot] in gdp_countries:
            matched_countries_dict.update({countries_plot: plot_countries[countries_plot]})
        else:
            not_matched_countries_set.add(countries_plot)
    return matched_countries_dict, not_matched_countries_set


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    nested_dict = {}
    gdp_dict = {}
    gdp_not_found_set = set()
    separator = gdpinfo["separator"]
    with open("C:/Users/acer/Desktop/Coursera/Coursera-Python-Projects/Data-Visualization/week3/" + gdpinfo["gdpfile"],
              newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=gdpinfo["quote"])
        for row in csvreader:
            rowid = row[gdpinfo["country_name"]]
            nested_dict[rowid] = row

        matched_dict, not_matched_set = reconcile_countries_by_name(plot_countries, nested_dict)
        for match in matched_dict:
            country_name = matched_dict[match]
            if year in nested_dict[country_name] and nested_dict[country_name][year] != '':
                gdp = float(nested_dict[country_name][year])
                gdp_dict.update({match: math.log10(gdp)})
            else:
                gdp_not_found_set.add(match)

    return gdp_dict, not_matched_set, gdp_not_found_set


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    gdp_dict, not_match_set, not_found_set = build_map_dict_by_name(gdpinfo, plot_countries, year)
    world_map_chart = pygal.maps.world.World()
    world_map_chart.title = "GDP by country for " + year + " (log scale), unified by common country NAME"
    world_map_chart.add("GDP for " + year, gdp_dict)
    world_map_chart.add("Missing from world map", not_match_set)
    world_map_chart.add("No GDP Data", not_found_set)
    world_map_chart.render_to_file(map_file)
    return


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
