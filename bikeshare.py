import time
import pandas as pd

'''
Created on Jan 24, 2019

@author: fred
'''
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# List to hold time filter choices given by user.
user_filters = []

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    allowed_cities = ('chicago','new york','washington')

    allowed_time_filters = ('month','day','both','none')

    allowed_months = ('january','february','march','april','may','june')

    allowed_days = ('mon','tue','wed','thur','fri','sat','sun')

    weekday_dict = {"Mon": 'Monday',"Tue": 'Tuesday',"Wed": 'Wednesday',"Thur": 'Thursday',"Fri": 'Friday',"Sat": 'Saturday',"Sun": 'Sunday'}

    print('\nHello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Would you like to see data for Chicago, New York, or Washington cities? \n")
    city = input("Enter city : \n").rstrip().lstrip()
    while city.lower() not in allowed_cities:
        print('You need to enter one of the following cities: Chicago, New York or Washington.\n')
        city = input("Enter city : \n")
    else:
        user_filters.append(city.title())

    print("Would you like to filter {}'s  data by month, day, both or not at all? Type none for no time filter.\n".format(str(user_filters[0])))

    time_filter_option = input('Enter your time filtering option: \n').rstrip().lstrip()

    while time_filter_option not in allowed_time_filters:
        print('You need to enter valid time filtering choice eg by month, day, both or not at all? Type none for no time filter.')
        time_filter_option = input('Enter your time filtering option: ').rstrip().lstrip()

    if time_filter_option.lower() == 'both':
        # get user input for month (all, january, february, ... , june)
        month = input("Enter month : ").rstrip().lstrip()
        while month.lower() not in allowed_months:
            print('You need to enter valid month name, January through June.')
            month = input("Enter month : ").rstrip().lstrip()
        else:
            user_filters.append(month.title())

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Enter weekday eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun: ").title().rstrip().lstrip()
        while day.lower() not in allowed_days:
            print('You need to enter weekday abbreviations eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun.')
            day = input("Enter weekday abbreviation eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun: ").title().rstrip().lstrip()
        else:
            user_filters.append(weekday_dict[day].title())

    elif time_filter_option.lower() == 'month':
        month = input("Enter month name, January through June: ").rstrip().lstrip()
        while month.lower() not in allowed_months:
            print('You need to enter valid month name, January through June.')
            month = input("Enter month : ").rstrip().lstrip()
        else:
            user_filters.append(month.title())
            user_filters.append('all')

    elif time_filter_option.lower() == 'day':
        day = input("Enter weekday eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun: ").title().rstrip().lstrip()
        while day.lower() not in allowed_days:
            print('You need to enter weekday abbreviations eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun.')
            day = input("Enter weekday abbreviation eg  Mon, Tue, Wed, Thur, Fri, Sat, Sun: ").title().rstrip().lstrip()
        else:
            user_filters.append('all')
            user_filters.append(weekday_dict[day].title())

    else:
        user_filters.append('all')
        user_filters.append('all')

    # Assign filter values selected by user to variables city, month, and day respectively.
    city = user_filters[0].lower()
    month = user_filters[1].lower()
    day = user_filters[2].lower()
    print()
    print('-'*80)
    print("\tFOR CITY OF '{}', YOU HAVE CHOSEN THE FOLLOWING TIME FILTERS:".format(city.upper()))
    print("\tMonth: '{}'".format(month.upper()))
    print("\tDay: '{}'".format(day.upper()))
    print('-'*80)

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start, end Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Calculate the travel time per trip and add that column to data frame.
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # extract month and day of week from Start Time to create new columns
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
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

    # display the most common month
    #count how many times a particular month occurs in data frame.
    popular_month = df['month'].mode()[0]
    months = {1: 'January', 2: 'February',3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    print('\tMost popular month is: {} \n'.format(months[popular_month]))

    # display the most common day of week
    #count how many times a particular day of the week occurs in data frame.
    popular_d_o_w = df['day_of_week'].mode()[0]
    print('\tMost popular day of the week is: {} \n'.format(popular_d_o_w))

    # display the most common start hour
    # count how many times a particular start hour occurs in data frame.
    popular_hour = df['Start Hour'].mode()[0]
    print('\tMost popular hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # count how many times a particular start station occurs in data frame.
    popular_station = df['Start Station'].mode()[0]
    df0 = df.groupby(['Start Station']).size().reset_index().rename(columns={0:'start station count'})
    max_start_station_count = str(df0['start station count'].max())
    print('\tMost commonly used start station: {} and it was used {} times \n'.format(popular_station,max_start_station_count))

    # display most commonly used end station
    # count how many times a particular end station occurs in data frame.
    popular_end_station = df['End Station'].mode()[0]
    df01 = df.groupby(['End Station']).size().reset_index().rename(columns={0:'end station count'})
    max_end_station_count = str(df01['end station count'].max())
    print('\tMost commonly used end station: {} and it was used {} times \n'.format(popular_end_station,max_end_station_count))

    # display most frequent combination of start station and end station trip
    # group by start and end station pair and count how many times the pair occurred.
    df1 = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'})

    # convert df1 series object type to dictionary for easy access of dict elements
    df2 = df1.loc[df1['count'].idxmax()].to_dict()

    print("\tThe combination of Start station: '{}' and end station: '{}' were the most frequently used. \n\tThis combination of stations  were used {} times. ".format(df2['Start Station'],df2['End Station'],str(df2['count'])))

    # Print the time taken to process statistics.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_time = str(df['Travel Time'].sum())
    print('\tThe total time for all trips made is : ' + total_trip_time)

    # display mean travel time
    trip_time_mean = str(df['Travel Time'].mean())
    print('\n\tThe average travel time is : ' + trip_time_mean)

    # Print the time taken to process statistics.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The following are the counts of the types of users that hired bikes: \n')

    df3 = df.dropna(axis=0,subset=['User Type'])

    user_type_counts = df3['User Type'].value_counts().to_dict()

    unique_user_types = df3['User Type'].unique().tolist()

    for unique_user_type in unique_user_types:
        print('\tThere is/are ' + str(user_type_counts[unique_user_type]) + ' count/s of user type: ' + unique_user_type + '\n')

    # Display counts of gender
    if user_filters[0] == 'Chicago' or user_filters[0] == 'New York':
        df4 = df.dropna(axis=0,subset=['Gender'])
        gender_counts = df4['Gender'].value_counts().to_dict()
        genders = df4['Gender'].unique().tolist()

        for gender in genders:
            print('\tThere are ' + str(gender_counts[gender]) + ' counts of gender type: ' + gender + '\n')

        # Display earliest, most recent, and most common year of birth
        print('These are earliest, most recent, and most common year of birth: \n')

        print('\tThe earliest year of birth is : ' + str(int(df4['Birth Year'].min())) + '\n')

        print('\tThe most recent year of birth is : ' + str(int(df4['Birth Year'].max())) + '\n')

        print('\tThe most common year of birth is : ' + str(int(df4['Birth Year'].mode())) + '\n')

    else:
        print('\tSorry Washington does not have gender and birth based data.')

    # Print the time taken to process statistics.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Displays raw data for the time filter option/s given by the user. Slices of five rows of raw data are shown when a user types 'y' for yes
    and quits displaying raw data when 'n' for no is typed in prompt.
    """

    # Drop columns that I added to help me answer descriptive statistics questions.
    df1 = df.drop(columns=['Travel Time','Start Hour','End Hour','month','day_of_week'])
    # Get the length of data frame to avoid out of range index errors.
    df_row_count = df1.shape[0]
    lower_index = 0
    upper_index = 10
    allowed_user_choices = ['y','n']
    # Ensure that user response is either y or n.
    list_next_five_rows = input("\nDo you want to display sets of ten rows of raw data? Enter 'y' for yes or 'n' for no: ").lower().rstrip().lstrip()
    while list_next_five_rows not in allowed_user_choices:
        print("You need to type in 'y' for yes or 'n' for no.")
        list_next_five_rows = input("\nDo you want to display sets of ten rows of raw data? Enter 'y' for yes or 'n' for no: ").lower().rstrip().lstrip()

    #Loop for as long as rows are within the index range of data frame.
    while upper_index < df_row_count:
        if list_next_five_rows == 'y':
            print(df1[lower_index:upper_index])
            lower_index = upper_index
            upper_index += 10
            list_next_five_rows = input("\nDo you want to display sets of ten rows of raw data? Enter 'y' for yes or 'n' for no: \n").lower().rstrip().lstrip()
            while list_next_five_rows not in allowed_user_choices:
                print("You need to type in 'y' for yes or 'n' for no.")
                list_next_five_rows = input('\nDo you want to display sets of ten rows of raw data? ').lower().rstrip().lstrip()
        else:
            print('\nYou have either opted not to proceed showing raw data or you have reached the end of raw data.')
            lower_index = 0
            upper_index = 10
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Calculates time statistics.
        time_stats(df)
        # Calculates station statistics.
        station_stats(df)
        # Calculates trip duration statistics.
        trip_duration_stats(df)
        # Calculates bike renter statistics.
        user_stats(df)
        # Shows requested raw data.
        show_raw_data(df)
        # Clears filter ready for next run.
        user_filters.clear()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
