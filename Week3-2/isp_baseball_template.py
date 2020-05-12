"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv


##
## Provided code from Week 3 Project
##

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


##
## Provided formulas for common batting statistics
##

# Typical cutoff used for official statistics
MINIMUM_AB = 500


def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0


def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0


def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    batting_statistic_list_dict = list(filter(lambda pair: int(pair[yearid]) == year, statistics))
    return batting_statistic_list_dict


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    result = []
    for row in statistics:
        calculated_batting_average = formula(info, row)
        player_name = (row[info["playerid"]])
        player_tup = (player_name, calculated_batting_average)
        result.append(player_tup)
    sorted_tups = sorted(result, key=lambda pair: pair[1], reverse=True)
    sorted_tups = sorted_tups[:numplayers]
    return sorted_tups


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    csv_input = read_csv_as_nested_dict(info["masterfile"],
                                        info["playerid"],
                                        info["separator"],
                                        info["quote"])
    match = []
    if len(top_ids_and_stats) != 1:
        for row in range(len(top_ids_and_stats)):
            player_id = top_ids_and_stats[row][0]
            name_first = csv_input[player_id].get("nameFirst")
            firstname = csv_input[player_id].get("firstname") or name_first
            lastname = csv_input[player_id].get("lastname") or csv_input[player_id].get("nameLast")
            fullname = firstname + " " + lastname
            fullstring = "{:.3f}".format(top_ids_and_stats[row][1]) + " --- " + fullname
            match.append(fullstring)
    else:
        player_id = top_ids_and_stats[0][0]
        firstname = csv_input[player_id].get("firstname")
        lastname = csv_input[player_id].get("lastname")
        fullname = firstname + " " + lastname
        fullstring = "{:.3f}".format(top_ids_and_stats[0][1]) + " --- " + fullname
        match.append(fullstring)
    return match


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """
    csv_input = read_csv_as_list_dict(info["battingfile"],
                                      info["separator"],
                                      info["quote"])
    filtered_statistics = filter_by_year(csv_input, year, info["yearid"])
    top_player_year = top_player_ids(info, filtered_statistics, formula, numplayers)
    player_detail = (lookup_player_names(info, top_player_year))
    return player_detail


##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    aggregate = {}

    for item in statistics:
        if not item[playerid] in aggregate:
            aggregate[item[playerid]] = {playerid: item[playerid]}
            for stat in fields:
                aggregate[item[playerid]][stat] = 0
        for stat in fields:
            value = int(item[stat])
            aggregate[item[playerid]][stat] = aggregate[item[playerid]][stat] + value
    return aggregate


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """
    nested_dict_list = []
    final_list = []
    info_player = info['playerid']
    info_fields = info['battingfields']
    all_batting_stats = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    batting_aggregate = aggregate_by_player_id(all_batting_stats, info_player, info_fields)
    for inner_dict in batting_aggregate.values():
        nested_dict_list.append(inner_dict)
    top_player_carrier = top_player_ids(info, nested_dict_list, formula, numplayers)
    final_list = lookup_player_names(info, top_player_carrier)
    return final_list


##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",  # Name of Master CSV file
                        "battingfile": "Batting_2016.csv",  # Name of Batting CSV file
                        "separator": ",",  # Separator character in CSV files
                        "quote": '"',  # Quote character in CSV files
                        "playerid": "playerID",  # Player ID field name
                        "firstname": "nameFirst",  # First name field name
                        "lastname": "nameLast",  # Last name field name
                        "yearid": "yearID",  # Year field name
                        "atbats": "AB",  # At bats field name
                        "hits": "H",  # Hits field name
                        "doubles": "2B",  # Doubles field name
                        "triples": "3B",  # Triples field name
                        "homeruns": "HR",  # Home runs field name
                        "walks": "BB",  # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

# test_baseball_statistics()
