import pandas as pd

# reporting functions

def print_list_countries(country_list):

    print('\n=================================|      List of countries        |===================================================\n')

    if len(country_list) % 4 == 0:
        for i in range(0 , len(country_list) - 1 , 4):
            print(
                f'{country_list[i]:<15}{country_list[i + 1]:<15}{country_list[i + 2]:<15}{country_list[i + 3]:<15}')

    elif len(country_list) % 4 == 1:
        for i in range(0 , len(country_list) - 1 , 4):
            print(
                f'{country_list[i]:<15}{country_list[i + 1]:<15}{country_list[i + 2]:<15}{country_list[i + 3]:<15}')
            print(country_list[-1])

    elif len(country_list) % 4 == 2:
        for i in range(0 , len(country_list) - 2 , 4):
            print(
                f'{country_list[i]:<15}{country_list[i + 1]:<15}{country_list[i + 2]:<15}{country_list[i + 3]:<15}')
            print(f'{country_list[-2]:<15}{country_list[-1]:<15}')

    else:
        for i in range(0 , len(country_list) - 3 , 4):
            print(
                f'{country_list[i]:<15}{country_list[i + 1]:<15}{country_list[i + 2]:<15}{country_list[i + 3]:<15}')
            print(f'{country_list[-3]:<15}{country_list[-2]:<15}{country_list[-1]:<15}')



def specific_country(results,country):

    country_list = results['Country'].unique().tolist()
    pd.DataFrame(results['Country'].unique()).to_csv('./data/results/country_list.csv')
    
    if country == None:

        print('\n\n============================|    Below you could see the table of content with all the countries     |====================================\n\n')

        return results

    else:
        if country not in country_list:
            country = country.lower()
            country = country.title()

            if country not in country_list:

                print_list_countries(country_list)

                raise NameError

            else:
                print(f'\n\n============================|    Below you could see the table of content of {country}      |====================================\n\n')

                df_specific_country = results.loc[results['Country'] \
                    .str.contains(country)].sort_values(by='Quantity' , ascending=False)

                return df_specific_country

        else:
            print(f'\n\n============================|    Below you could see the table of content of {country}      |====================================\n\n')

            df_specific_country = results.loc[results['Country'] \
                .str.contains(country)].sort_values(by='Quantity' , ascending=False)

            return df_specific_country


def reporting(results,country):

        return specific_country(results,country)


