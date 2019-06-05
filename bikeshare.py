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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('Which city data you want to see(chicago, new york city, washington) :')
        if city.lower() in ('chicago','new york city','washington'):
            city=city.lower()
            break
        print('enter a vlid city name')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month=input('Enter name of the month[january, february, ... , june] to be filter by, or "all" to apply no filetr :')
        if month.lower() in ('january','february','march','april','may','june','all') :
            month=month.lower()
            break
        print('Enter Valid month')
            #months = ['january', 'february', 'march', 'april', 'may', 'june']
            #month = months.index(month) + 1
            #df = df[df['month'] == month]        
            

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Enter the day you want to filer by [monday, tuesday, ... sunday] or "all" to apply no filter :')
        if day.lower() in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'):
            day=day.lower()
            break
        print('Enter a valid day')
        # filter by day of week to create the new dataframe
        #df = df[df['day_of_week'] == day.title()]


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
              
    # load data file into a dataframe
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

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month= df['month'].mode()[0]
    print("Most common month : ",months[popular_month-1])


    # TO DO: display the most common day of week
    popular_day=df['day_of_week'].mode()[0]
    print("Most common month : ",popular_day)

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station=df["Start Station"].mode()[0]
    print("Most common Start Station is : ", popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station=df["End Station"].mode()[0]
    print("Most common End Station is : ", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    
    df=df.groupby(['Start Station','End Station']).size().reset_index(name='counts')
    df=df[df['counts']==df['counts'].max()]
    
    print("Most frequent combination of start station '{}' and end station '{}'  ".format(df['Start Station'].astype(str),df['End Station'].astype(str)))
     
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total Travel Time = ',total_travel_time)
    
    # TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('Mean Travel Time = ',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types",user_types)


    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts=df['Gender'].value_counts()
        print("Gender Counts ",gender_counts)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest Birth Year :",df['Birth Year'].min())
        print("Most recent Birth Year :",df['Birth Year'].max())
    
        df=df.groupby('Birth Year').size().reset_index(name='counts')
        df=df[df['counts']==df['counts'].max()]
        print("Most Common Birth Year ",df['Birth Year'] )
    
    
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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
