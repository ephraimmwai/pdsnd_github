import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities, months, days, city, month, day = [], ['all'], ['all'], '', '', ''

    for key, value in CITY_DATA.items():
        cities.append(key)

    for i in range(1, 7):
        months.append(calendar.month_name[i].lower())

    for day in calendar.day_name:
        days.append(day.lower())

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while city not in cities:
        city = input('Enter name of city (chicago , new york city, washington)').lower()
    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input('Enter month name (all, january, february ... june)').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input('Enter day of week (all, monday, tuesday ... sunday)').lower()


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
    # city, month, day='washington','february','sunday'
    csv_data = pd.read_csv(CITY_DATA[city])
    # print(csv_data)

    df = pd.DataFrame(data=csv_data)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = []
        for i in range(1, 7):
            months.append(calendar.month_name[i].lower())
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_data(df):

    #get user input to see more data option
    x = 5
    while True:
        display = ''
        # input_value = True
        while display not in ['yes', 'no']:
            display = input('Would you like to see more data? (yes,no)').lower()

        if display == 'no':
            #exit display data function
            return
        else:
            # while x <= df.shape[0]:
            print(df.head(x))
        x += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month= calendar.month_name[df['month'].mode()[0]]
    print('Most common Month: {}'.format(most_common_month))

    # display the most common day of week
    most_common_week_day = df['day_of_week'].mode()[0]
    print('Most Common week day: {}'.format(most_common_week_day))

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common start hour: {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Commont Start station: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common End station: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' - ' + df['End Station']
    most_frequent_station_combination = df['Station Combination'].mode()[0]
    print('Most common Start station and End station combination: {}'.format(most_frequent_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time - minutes
    df['travel time'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])) / np.timedelta64(1, 'm')
    total_travel_time = df['travel time'].sum()

    print('Total travel time(minutes): {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['travel time'].mean()
    print('Mean travel time(minutes): {}'.format(round(mean_travel_time, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count per user type:\n {}'.format(df['User Type'].value_counts()))


    if 'Gender' in (df.columns) and 'Birth Year' in (df.columns):

        # Display counts of gender
        print('Count per Gender: \n {}'.format(df['Gender'].value_counts()))

        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth:  {}'.format(min(df['Birth Year'])))
        print('The most recent year of birth: {}'.format(max(df['Birth Year'])))
        print('The most common year of birth: {}'.format(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
