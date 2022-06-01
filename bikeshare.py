import time
import pandas as pd
import numpy as np
from IPython.display import display

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Would you like to see data for Chicago, New York, or Washington?').lower()
    while city not in CITY_DATA.keys():
        city = input('Sorry, wrong city. Please, try again. Choose between Chicago, New York, or Washington').lower()

    timeFilter = input('Would you like to filter the data by month, day, both, or not at all?').lower()

    def getMonth():
        month = input('Which month - January, February, March, April, May, or June?').lower()
        while month not in (['january', 'february', 'march', 'april', 'may', 'june']):
            month = input('Sorry, wrong month. Please, try again. Choose between January, February, March, April, May, or June').lower()
        return month
    def getDay():
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
        while day not in (['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
            day = input('Sorry, wrong month. Please, try again. Choose between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday').lower()
        return day

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if timeFilter == 'both':
        month = getMonth()
        day = getDay()
    elif timeFilter == 'month':
        month = getMonth()
        day = 'all'
    elif timeFilter == 'day':
        day = getDay()
        month = 'all'
    else:
        day = 'all'
        month = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # We load city data in a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Dealing with NaN
    df.loc[:, 'User Type'].fillna('Undefined', inplace = True)
    if city != 'washington':
        df.loc[:, 'Gender'].fillna('Undefined', inplace = True)
        df.loc[:, 'Birth Year'].fillna(0, inplace = True)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    start_time_as_month = df['Start Time'].dt.month
    start_time_as_weekday = df['Start Time'].dt.dayofweek

    # FIlter by month and day
    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1
        df = df.loc[start_time_as_month == month]
    if day != 'all':
        weekdays_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = weekdays_list.index(day)
        df = df.loc[start_time_as_weekday == day]

    return df

def df_iterator(iterable, size, start_at):
    """Helper function. Generator that helps to load data piece by piece."""
    for i in range(start_at, len(iterable), size):
        yield iterable[i:i + size]

def show_raw_data():
    """Prints raw filtered data, 5 rows by iteration."""
    see_data = input('Would you like to see the raw data? Please, enter yes or no.\n').lower()
    while see_data not in (['yes','no']):
        see_data = input('\nSorry, I don\'t understand. Please, type yes or no.\n').lower()

    if see_data == 'yes':
        start_at_row = 0

        for i in df_iterator(df, 5, start_at_row):
            display(i)
            see_next_rows = input('\nWould you like to see 5 more rows of the data? Please, enter yes or no.\n').lower()
            while see_next_rows not in (['yes','no']):
                see_next_rows = input('\nIncorrect answer. Please, type yes or no.\n').lower()
            if see_next_rows.lower() != 'yes':
                break
            start_at_row += 5

def common_values(values):
    """Helper function. Helps to define most common values in a column. Returns 2 values."""
    max_value = values.value_counts().max()
    most_common_value = values.mode()[0]
    return most_common_value, max_value

def count_values(values):
    """Helper function. Helps to count values in a column. Prints values and their counts."""
    values_count = values.value_counts()
    for i in range(values_count.index.size):
        print('{}: {}'.format(values_count.index[i], values_count[i]))

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    #The month as January=1, December=12
    months = df['Start Time'].dt.month
    most_common_months_data = common_values(months)
    print('Most common month: {}, Count: {}'.format(most_common_months_data[0], most_common_months_data[1]))

    # display the most common day of week

    #The day of the week with Monday=0, Sunday=6
    weekdays = df['Start Time'].dt.dayofweek
    most_common_weekdays_data = common_values(weekdays)
    print('Most common day of week: {}, Count: {}'.format(most_common_weekdays_data[0], most_common_weekdays_data[1]))

    # display the most common start hour
    st_hour = df['Start Time'].dt.hour
    most_common_st_hour_data = common_values(st_hour)
    print('Most common start hour: {}, Count: {}'.format(most_common_st_hour_data[0], most_common_st_hour_data[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = common_values(df['Start Station'])
    print('Most common start station: {}, Count: {}'.format(most_common_start_station[0], most_common_start_station[1]))

    # display most commonly used end station
    most_common_end_station = common_values(df['End Station'])
    print('Most common end station: {}, Count: {}'.format(most_common_end_station[0], most_common_end_station[1]))

    # display most frequent combination of start station and end station trip
    stations_combo = df['Start Station'] + ' - ' + df['End Station']
    most_common_stations_combo = common_values(stations_combo)
    print('Most frequent stations combo: {}, Count: {}'.format(most_common_stations_combo[0], most_common_stations_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_sec = df[['Trip Duration']].sum()
    total_travel_time_h = total_travel_time_sec / 3600
    print('Total travel time, seconds: {}, hours: {}'.format(total_travel_time_sec.values[0], total_travel_time_h.values[0]))

    # display mean travel time using numpy
    mean_travel_time = np.mean(df[['Trip Duration']])
    print('Mean travel time', mean_travel_time.values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_values(df['User Type'])

    #city, month, day = get_filters()
    if city != 'washington':
        # Display counts of gender
        print('\nGender distribution: ')
        count_values(df['Gender'])

        # Display earliest, most recent, and most common year of birth

        #filter years to exclude 0 values and then convert to int type
        years = df['Birth Year'][df['Birth Year'] > 0].astype(np.int64)

        earliest_year = years.min()
        most_recent_year = years.max()
        most_common_year = common_values(years)

        print('\nEarliest year of birth: {},\nMost recent year of birth: {},\nMost common year of birth: {}'.format(earliest_year,most_recent_year,most_common_year[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        show_raw_data()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
