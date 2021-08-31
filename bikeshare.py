import time
import pandas as pd
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_check(prompt, options):
    """ Asks user to provide a string input, and checks if its an acceptable input.
    If the input is not valid, it asks the user if they want to try again.
    If not yes, then it exits.

    INPUT:
    prompt: String. A sentence requesting input from the user.
    options: List of stromgs (all lower case). A list of acceptable user inputs.

    OUTPUT:
    x: String. Accepted user inout, made lower case.

    """
    while True:
        # Asks for user input
        x = input(prompt).lower()

        # Check if input in list of acceptable inputs
        if x in options:
            # If in list, returns user input
            return x
            break
        else:
            # If not in list, then asks user if want to try again
            restart = input('\nThat\'s not a valid input. Wanna try again? Yes or No\n')
            if restart.lower() != 'yes':
                exit()

def get_filters():
    """ Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    prompt = '\nWould you like to see data for Chicago, New York City, or Washington?\n'

    city = input_check(prompt, CITY_DATA.keys())


    # Get user input for what they would like to filter (month, day, both or not at all)
    prompt = '\nWould you like to filter the data by month, day, both or none?\n'
    options = ['month', 'day', 'both', 'none']

    input_filter = input_check(prompt, options)


    # Get user input for month if applicable
    if input_filter in ['month', 'both']:
        prompt = '\nWhich month? January, February, March, April, May, or June? Please type out the full month name\n'
        options = ['january', 'february', 'march', 'april', 'may', 'june']

        month = input_check(prompt, options)
    else:
        month = 'all'

    # Get user input for day of week if applicable
    if input_filter in ['day', 'both']:
        prompt = '\nWhich day? - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Please type out the full\n'
        options = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        day = input_check(prompt, options)
    else:
        day = 'all'

    # Print spacers and return user inputs.
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """ Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month to create  new dataframe (if applicable)
    if month != 'all':
        df = df[df['month'] == month.title()]

    # Filter by day of week to create new dataframe (if applicable)
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # Start time for output
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month, and count
    popular_month = df['month'].mode()[0]
    popular_month_count = df[df['month']==popular_month].count()[0]
    print('Most Frequent Start Month:', popular_month, ', Count:', popular_month_count)

    # Display the most common day of week, and count
    popular_day = df['day_of_week'].mode()[0]
    popular_day_count = df[df['day_of_week']==popular_day].count()[0]
    print('Most Frequent Start Day of Week:', popular_day, ', Count:', popular_day_count)

    # Display the most common start hour, and count
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df[df['hour']==popular_hour].count()[0]
    print('Most Frequent Start Hour:', popular_hour, ', Count:', popular_hour_count)

    # Display time to complete
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # Start time for output
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station, and count
    popular_startstation = df['Start Station'].mode()[0]
    popular_startstation_count = df[df['Start Station']==popular_startstation].count()[0]
    print('Most Common Start Station:', popular_startstation, ', Count:', popular_startstation_count)

    # Display most commonly used end station, and count
    popular_endstation = df['End Station'].mode()[0]
    popular_endstation_count = df[df['End Station']==popular_endstation].count()[0]
    print('Most Common End Station:', popular_endstation, ', Count:', popular_endstation_count)

    # Display most frequent combination of start station and end station trip, and count
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    popular_combination_count = df.groupby(['Start Station','End Station']).size().max()
    print('Most Freqeuent Start/End Station trips:', popular_combination, ', Count:', popular_combination_count)

    # Display time to complete
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

     # Start time for output
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Dsplay total travel time
    total_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].sum().round()))
    print('Total Travel Time [days hh:mm:ss]:', total_travel_time)

    # Display mean travel time
    mean_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].mean().round()))
    print('Mean Travel Time [hh:mm:ss]:', mean_travel_time)

    # Display time to complete
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

     # Start time for output
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type']).size()
    print('Subscribers:', user_types['Subscriber'], ', Customers:', user_types['Customer'])

    # Error handler for the display of gender and age data
    try:
        # Display counts of gender
        gender = df.groupby(['Gender']).size()
        print('Male:', gender['Male'], ', Female:', gender['Female'])

        # Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:', earliest_birth)
        print('Most Recent Birth Year:', most_recent_birth)
        print('Most Common Birth Year:', most_common_birth)

    except:
        # Display messages if no gender and age data available
        print('No gender data to share')
        print('No age data to share')

    # Display time to complete
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    Main Functiom:
    1. Runs each of the above functions in turn.
    2. Asks the user if they want to see 5 lunes of raw data at a time.
    3.

    """

    while True:
        # Runs each of the key functions in turn.
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Restores dataframe to raw data, by dropping added columns from load data
        df.drop(columns=['month','day_of_week','hour'], inplace=True)
        # Sets option that allows all columns of raw data to display
        pd.set_option('display.max_columns', None)

        # Displays 5 lines of raw data when prompted by user, or until out of data.
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter Yes or No.\n')
        if raw_data.lower() == 'yes':
            i = 0
            end = df.shape[0]

            while i <= end:
                print(df[i:i+5])
                next_data = input('\nWould you like to see 5 more lines of raw data? Enter Yes or No.\n')

                if next_data.lower() != 'yes':
                    break
                i = i + 5

        # Checks if user wants to restart, or exit.
        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
