import time
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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while city not in ['c', 'n', 'w']:
        city = input("Which city would you like to explore? \nc = chicago\nn = new york city\nw = washington\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            user_month = int(input("Which month would you like to explore? \n0 = all\n1 = january\n2 = february\n3 = march\n4 = april\n5 = may\n6 = june\n"))
            if user_month > len(months)-1:
                user_month = int(input("Which month would you like to explore? \n0 = all\n1 = january\n2 = february\n3 = march\n4 = april\n5 = may\n6 = june\n"))

            break
        except:
            print("Input the number according to the month you want to explore")
    month = months[int(user_month)]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            user_day = int(input("Which day would you like to explore? \n0 = all\n1 = monday\n2 = tuesday\n3 = wednesday\n4 = thursday\n5 = friday\n6 = saturday\n7 = sunday\n"))
            if user_day > len(days)-1:
                user_day = input("Which day would you like to explore? \n0 = all\n1 = monday\n2 = tuesday\n3 = wednesday\n4 = thursday\n5 = friday\n6 = saturday\n7 = sunday\n")

            break
        except:
            print("Input the number according to the day you want to explore")
    day = days[int(user_day)]

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most popular month: ', popular_month)
    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most popular day: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(city, df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most riders in {} start their ride from {}.'.format(city,popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most riders in {} end their ride at {}.'.format(city,popular_end))

    # display most frequent combination of start station and end station trip
    df['Start and End'] = df['Start Station'] + '/' + df['End Station']
    popular_combine = df['Start and End'].mode()[0]
    print('Most rides start and end at {}.'.format(popular_combine))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum(axis = 0, skipna = True)
    print('The total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Rides are usually {} seconds long on average.'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users, including user type, gender and birth year."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Types of users:")
    print(user_types)
    print('*'*40)
    # Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'].fillna('NA', inplace = True)
        gender_count = df['Gender'].value_counts()
        print("Gender breakdown:")
        print(gender_count)
    else:
        print("Gender is not recorded in this city")

    print('*'*40)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'].dropna()
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("Oldest rider: ", pd.to_numeric(earliest_year, downcast = 'integer'))
        print("Youngest rider: ", recent_year)
        print("Most rider: ", common_year)
    else:
        print("Birth year is not recorded in this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    df = pd.read_csv(CITY_DATA[city])
    return df
def main():
    while True:
        city, month, day = get_filters()
        cities = {'c':'chicago', 'n':'new york city', 'w':'washington'}
        city = cities[city]
        df = load_data(city, month, day)
        print("Displaying stats for:\ncity:{}\nmonth:{}\nday:{}".format(city, month, day))
        time_stats(df)
        station_stats(city,df)
        trip_duration_stats(df)
        user_stats(df)
        n=0
        df_raw = display_raw_data(city)
        raw_data = input("Would you like to view individual data? 'yes' or 'no'")
        while n < df.shape[0] and raw_data =="yes":
            print(df_raw.iloc[n:n+5])
            raw_data = input("Would you like to view individual data? 'yes' or 'no'")
            n+=5
        else:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()
