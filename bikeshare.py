import time
import datetime
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data! ')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nEnter one of the following: chicago, new york city, washington: ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("\nLooks like you entered in an invalid choice.")
            continue
        break
    print("\nYou entered:", city)

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nEnter one of the following options: all, january, february, march, april, may, june:  ").lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print("\nLooks like you entered in an invalid choice.")
            continue
        break
    print("\nYou entered:", month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nEnter one of the following options: all, monday, tuesday, ... sunday: ").lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("\nLooks like you entered in an invalid choice.")
            continue
        break
    print("\nYou entered:", day)

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    df['month'] = df['Start Time'].dt.month
    month_classifying = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6:'June'}
    df['month_cat'] = df['month'].map(month_classifying)
    most_common_month = df['month_cat'].mode()[0]

    print('\nThe most common month is:', most_common_month)

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    most_common_day = df['day_of_week'].mode()[0]

    print('\nThe most common day is:', most_common_day)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    print('\nThe most common hour is (Note: in miltary time):', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    most_common_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start statition is:', most_common_start_station)
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nThe most common end statition is:', most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combo = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Frequency of Route')
    frequent_combos = combo.sort_values(by='Frequency of Route', ascending=False)
    most_frequent_combos = frequent_combos.iloc[0]
    print('\nThe most frequent combination is:', most_frequent_combos)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    sum_trip_duration = df['Trip Duration'].sum()
    print('\nHere is the total time traveled for each rider in the dataset.\n', round(sum_trip_duration), 'seconds')
    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('\nHere is the average time traveled.', round(mean_trip_duration), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('\nHere is the data for user type counts\n', user_types_counts)

    # TO DO: Display counts of gender
    try:
        gender_breakdown = df['Gender'].value_counts()
        print('\nHere is the data for gender counts\n', gender_breakdown)
    except:
        print('\nDataset doesnt have gender breakdown\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        birthyear_earliest = df['Birth Year'].min()
        print('\nHere is the earliest birthyear of a rider\n', int(birthyear_earliest))

        most_recent_date = df['End Time'].max()
        birthyear_for_most_recent_date = df.loc[df['End Time'] == most_recent_date, 'Birth Year'].values[0]
        print("\nHere is the most recent rider's birth year\n", int(birthyear_for_most_recent_date))

        birthyear_common = df['Birth Year'].mode()
        print('\nHere is the most common birthyear of a rider\n', int(birthyear_common))
    except:
        print('\nDataset doesnt have birth year breakdown\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        def display_raw_data(df):
            """ Displays rawdata for bikeshare users. """
            i = 0
            raw = input("\nWould you like to see the rawdata of bikeshare users? Enter Yes or No:  ").lower() # TO DO: convert the user input to lower case using lower() function
            pd.set_option('display.max_columns',200)

            while True:
                if raw == 'no':
                    break
                elif raw == 'yes':
                    print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
                    raw = input("\nWould you like to see an additional 5 rows of rawdata of bikeshare users? Enter Yes or No: ").lower()
                    i += 5
                else:
                    raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
