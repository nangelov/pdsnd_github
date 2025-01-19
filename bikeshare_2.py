import time
# see more at https://pandas.pydata.org/docs/index.html
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


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
    city = 'not specified'
    while city not in CITY_DATA.keys():
        print("\n Valid inputs here: \n", CITY_DATA.keys())
        city = input('Please specify city of interest: ').lower()
    print("\n Your city of interest is ",city)

    # get user input for month (all, january, february, ... , june)
    month = 'not specified'

    while month not in MONTHS and (month != 'all'):
        print("\n Valid inputs here are \"all\" or one of \n", MONTHS)
        month = input('Please specify month of interest or type "all" for all months \n').lower()
    print("\n Your month of interest is ",month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'not specified'
    while day not in DAYS and (day != 'all'):
        print("\n Valid inputs here \"all\" or one of \n", DAYS)
        day = input('Please specify day of interest or type "all" for all days \n').lower()
    print("\n Your day of interest is ",day)

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
    print("\n We are loaging the data...")
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # increment the index with one, as Jan = 0 in the MONTHS list
        month = MONTHS.index(month)+1

        # filter by month to create the new dataframe
        df['month'] = df[df['month'] == month]['month']
        if df['month'].empty or df['month'].isna().all():
            print("No data for the specified month and given filter criteria. Please change your filter criteria")
            return None

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = DAYS.index(day)
        df['day_of_week'] = df[df['day_of_week'] == day]['day_of_week']

        if df['day_of_week'].empty or df['day_of_week'].isna().all():
            print("No data for the specified day and given filter criteria. Please change your filter criteria")
            return None

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # adding 1 as month_name[0] is an empty string
    most_common_month = int(df['month'].mode()[0])
    print("Most common month", MONTHS[most_common_month])

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    print("Most common day of the week", DAYS[int(df['day_of_week'].mode()[0])])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common start hour", int(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station is ",df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most commonly used end station is ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['trip_start_end_station'] = df['Start Station'] + " to " + df['End Station']
    print("Most commonly used trip start to end station is ", df['trip_start_end_station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel time is ",df['Trip Duration'].sum())

    # display mean travel time
    print("Mean Travel time is ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of user types are ", df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
    # Gender column is missing from washington.csv
        print("Number of user types are ", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
    # Birth Year column is missing from washington.csv
        print("Earliest year of birth is ", df['Birth Year'].min())
        print("Most recent year of birth is ", df['Birth Year'].max())
        print("Most common year of birth is ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data from bikeshare datasets."""
    rows = 0

    disp_raw = 'tbd'
    while disp_raw not in ['yes', 'no']:
        disp_raw = input(
            "Would you like me to display 5 rows of raw data for the city of interest? \n"
            "Answer with yes or no!").lower()
        if disp_raw == 'no':
            break
        elif disp_raw == 'yes':
            disp_raw = 'not specified'
            pd.set_option('display.max_columns', 200)
            print(df.iloc[rows:rows+5,:])
            rows += 5
        else:
            disp_raw = input(
                "Would you like me to display 5 rows of raw data for the city of interest? \n"
                "Answer with yes or no!").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = 'not specified'
        while restart not in ['yes','no']:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no':
                return 0


if __name__ == "__main__":
	main()
