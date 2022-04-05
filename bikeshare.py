import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_data('cities')
    # get user input for month (all, january, february, ... , june)
    while True:
        enter = input(
            'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
        if enter == 'none':
            month = 'all'
            day = 'all'
            break
        elif enter == 'both':
            month = get_data('months')
            day = get_data('days')
            break
        elif enter == 'month':
            month = get_data('months')
            day = 'all'
            break
        elif enter == 'day':
            month = 'all'
            day = get_data('days')
            break
        else:
            print('Sorry, please input a correct content')
    #  get user input for day of week (all, monday, tuesday, ... sunday)

    print('-' * 40)
    return city, month, day

def get_data(data):
    cities = ['Chicago', 'New York City', 'Washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = { '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday',
            '6': 'Saturday','7': 'Sunday'}
    while True:
        if data == 'cities':
            return typein_check('Would you like to see data for Chicago, New York City or Washington: \n', cities)
        elif data == 'months':
            return typein_check('Which month? January, February, March, April, May or June?\n', months)
        elif data == 'days':
            while True:
                day = input('Which day? Please type an integer(e.g., 1=Monday): \n')
                if day in days:
                    return days[day]
                    break
                print('Sorry, please enter a correct integer(e.g., 1=Monday)')

def typein_check(typein_print, typein_data):

    while True:
        ret = input(typein_print).title()
        if ret in typein_data:
            return ret.lower()
            break
        print('Sorry, please enter {}.'.format(typein_data))

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
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
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    # display the most common month
    month_no = df['month'].mode()[0]
    common_month = months[month_no]
    print('Most common month: {}.'.format(common_month))

    # display the most common day of week
    common_day_no = df['day_of_week'].mode()[0]
    print('Most common day of week: {}.'.format(common_day_no))

    # display the most common start hour
    common_hour_no = df['Start Time'].dt.hour.mode()[0]
    print('Most common start hour: {}.'.format(common_hour_no))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    common_start = df['Start Station'].value_counts().index[0]
    print('Most commonly used start station: {}.'.format(common_start))

    #  display most commonly used end station
    common_end = df['End Station'].value_counts().index[0]
    print('Most commonly used end station: {}.'.format(common_end))

    #  display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + '/ ' + df['End Station']
    common_combine = df['combination'].value_counts().index[0]
    print('Most frequent combination of start and end station trip: {}.'.format(common_combine))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds.'.format(total_time))

    #  display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds.'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_specific = df['User Type'].value_counts()
    print('User type\n{0}: {1}\n{2}: {3}'.format(user_specific.index[0], user_specific.iloc[0], user_specific.index[1],
                                                 user_specific.iloc[1]))

    # Display counts of gender
    cities_columns = df.columns
    if 'Gender' in cities_columns:
        user_gender = df['Gender'].value_counts()
        print('Male:{0}\nFemale:{1}. '.format(user_gender.loc['Male'], user_gender.loc['Female']))
    else:
        print("Sorry, this city don't have gender data")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in cities_columns:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].value_counts().index[0]
        print('Earliest user year of birth: %i.' % (earliest))
        print('Most recent user year of birth: %i.' % (recent))
        print('Most common user year of birth: %i.' % (common))
    else:
        print("Sorry, this city don't have birth year data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
