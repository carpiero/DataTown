# Ironhack Data Analytics M1 Project README file



![Image](https://res.cloudinary.com/springboard-images/image/upload/q_auto,f_auto,fl_lossy/wordpress/2019/05/aiexcerpt.png)

---



### :raising_hand: **Jobs Survey Reporting** 


### :baby: **Status**
Ironhack Data Analytics M1 Project

### :running: **One-liner**

```
main_script.py -p ./data/raw/raw_data_project_m1.db --country Malta --unemployed yes
```


### :computer: **Technology stack**

- Python==3.7.3
- pandas==0.24.2
- sqlalchemy==1.3.16
- requests==2.23.0
- bs4==4.9.1
- numpy==1.18.1
- argparse==3.2

## **Data:**

There are 3 different datasource involved:

- **Tables (.db).** [Here](http://www.potacho.com/files/ironhack/raw_data_project_m1.db) you can find the `.db` file with the main dataset.

- **API.** We will use the API from the [Open Skills Project](http://dataatwork.org/data/).  

- **Web Scraping.** Finally, we will need to retrieve information about country codes from [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes) website.

### :see_no_evil: **Usage**

In the first place, we want to obtain the data of a specific job per gender and country of a concrete survey.

Second I have decided to put the argument unemployed.

If the argument is yes, you obtain the percentage of a specific jobs by gender over the total number of people surveyed in a certain country. Because you have a Job title called 'Unemployed or Part time job or Inactive', These are people who answered the survey who did not have a full-time job, Therefore they can only be Unemployed or they have a Part time job or are Inactive(like students or eldery)

If the argument is no, you obtain the percentage of a specific jobs by gender over the total number of people who have a full time job in a certain country. 

Besides I have set the string 'Less than 1%' for the percentages between 1 and more than 0, to make it more readable.

Third, you get the results for a specific country with argument -country, you can also get the percentage for the total number of people surveyed or for the total number of people who have a full time job.

Fourth to handle errors when you set a wrong argument I have used two options.

when you enter a wrong country or does not appear in the survey, the terminal prints the list of possible countries.

In addition, when you enter a wrong unemployed argument, the terminal prints a native error and the choices.

### :file_folder: **Folder structure**
```
└── project
    ├── __trash__
    ├── .gitignore
    ├── .env
    ├── requeriments.txt
    ├── README.md
    ├── main_script.py
    ├── notebooks
    ├── p_acquisition
    │   ├── __init__.py
    │   └── m_acquisition.py
    ├── p_analysis
    │   ├── __init__.py
    │   └── m_analysis.py
    ├── p_reporting
    │   ├── __init__.py
    │   └── m_reporting.py
    ├── p_wrangling
    │   ├── __init__.py
    │   └── m_wrangling.py
    └── data
        ├── raw
        ├── processed
        └── results
```

![animated1](assets/readme.gif)


