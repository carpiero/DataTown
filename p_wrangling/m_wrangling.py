
# wrangling functions

def fillnulls(df_fillnulls, unemployed):

    if unemployed== None:

        df_fillnulls.loc[df_fillnulls['Job Title'].isnull(), 'Job Title'] = 'Unemployed or Part time Job or Inactive'

        return df_fillnulls

    elif unemployed.lower() == 'yes':

        df_fillnulls.loc[df_fillnulls['Job Title'].isnull() , 'Job Title'] = 'Unemployed or Part time Job or Inactive'

        return df_fillnulls

    elif unemployed.lower() == 'no':

        df_fillnulls=df_fillnulls.loc[~df_fillnulls['Job Title'].isnull()].reset_index()

        return df_fillnulls

    else:

        raise TypeError



def wrangle(data, unemployed):

    return fillnulls(data, unemployed)