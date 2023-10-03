LLM_TEMPLATE_EN = """
Here is a database schema:
department:
CREATE TABLE "department" (
"Department_ID" INTEGER PRIMARY KEY,
  "Name" TEXT,
  "Creation" TEXT,
  "Ranking" INTEGER,
  "Budget_in_Billions" REAL,
  "Num_Employees" REAL
)

head:
CREATE TABLE "head" (
"head_ID" INTEGER PRIMARY KEY,
  "name" TEXT,
  "born_state" TEXT,
  "age" REAL
)

management:
CREATE TABLE "management" (
"department_ID" INTEGER PRIMARY KEY,
  "head_ID" INTEGER,
  "temporary_acting" TEXT
)

Previous conversation:

Please write me a SQL statement that answers the following question: How many heads of the departments are older than 56 ? [/INST] select count ( * ) from head where age > 56; [INST] Here is a database schema:
book_club:
CREATE TABLE "book_club" (
"book_club_id" INTEGER PRIMARY KEY,
  "Year" INTEGER,
  "Author_or_Editor" TEXT,
  "Book_Title" TEXT,
  "Publisher" TEXT,
  "Category" TEXT,
  "Result" TEXT
)

culture_company:
CREATE TABLE "culture_company" (
"Company_name" TEXT PRIMARY KEY,
  "Type" TEXT,
  "Incorporated_in" TEXT,
  "Group_Equity_Shareholding" REAL,
  "book_club_id" TEXT,
  "movie_id" TEXT
)

movie:
CREATE TABLE "movie" (
"movie_id" INTEGER PRIMARY KEY,
  "Title" TEXT,
  "Year" INTEGER,
  "Director" TEXT,
  "Budget_million" REAL,
  "Gross_worldwide" INTEGER
)

Previous conversation:
Human: Show me movies for 2022
AI: SELECT Title,
       Year
FROM movie
WHERE Year = "2022";
Human: What is the number of movies per year?
AI: SELECT count(*)
FROM cust_order
GROUP BY Year;
Human: Show me company movie pairs
AI: SELECT Company_name,
       Title
FROM culture_company as c
LEFT JOIN movie as m
ON c.movie_id = m.movie_id;

Please write me a SQL statement that answers the following question: What are all company names that have a corresponding movie directed in the year 1999? [/INST] select culture_company.company_name from movie inner join culture_company on movie.movie_id = culture_company.movie_id where movie.year = 1999; [INST] Here is a database schema:
station:
CREATE TABLE "station" (
"id" INTEGER PRIMARY KEY,
  "name" TEXT,
  "lat" REAL,
  "long" REAL,
  "dock_count" INTEGER,
  "city" TEXT,
  "installation_date" TEXT
)

status:
CREATE TABLE "status" (
"station_id" INTEGER,
  "bikes_available" INTEGER,
  "time" TEXT,
)

trip:
CREATE TABLE "trip" (
"id" INTEGER PRIMARY KEY,
  "duration" INTEGER,
  "start_date" TEXT,
  "start_station_name" TEXT,
  "start_station_id" INTEGER,
  "end_date" TEXT,
  "end_station_name" TEXT,
  "end_station_id" INTEGER,
  "bike_id" INTEGER,
  "subscription_type" TEXT,
  "zip_code" INTEGER,
)

weather:
CREATE TABLE "weather" (
"date" TEXT,
  "max_temperature_f" INTEGER,
  "mean_temperature_f" INTEGER,
  "min_temperature_f" INTEGER,
  "mean_dew_point_f" INTEGER,
  "max_dew_point_f" INTEGER,
  "min_dew_point_f" INTEGER,
  "max_humidity" INTEGER,
  "mean_humidity" INTEGER,
  "max_sea_level_pressure_inches" REAL,
  "mean_sea_level_pressure_inches" REAL,
  "min_sea_level_pressure_inches" REAL,
  "max_visibility_miles" INTEGER,
  "mean_visibility_miles" INTEGER,
  "min_visibility_miles" INTEGER,
  "max_wind_Speed_mph" INTEGER,
  "mean_wind_speed_mph" INTEGER,
  "max_gust_speed_mph" INTEGER,
  "precipitation_inches" INTEGER,
  "cloud_cover" TEXT,
  "events" REAL,
  "wind_dir_degrees" INTEGER,
  "zip_code" INTEGER,
)


Please write me a SQL statement that answers the following question: What are the ids of stations that have latitude above 37.4 and never had bike availability below 7? [/INST] select id from station where lat > 37.4 except select station_id from status group by station_id having min ( bikes_available ) < 7; [INST] Here is a database schema:
{schema}

Previous conversation:
{{chat_history}}

Please write me a SQLite statement that answers the following question: {{question}}
Do not provide any commentary or explanation of what the code does, just the SQL statement ending in a semicolon.
Answer:
"""

LLM_TEMPLATE_PL = """
Oto schemat bazy danych:
department:
CREATE TABLE "department" (
"Department_ID" INTEGER PRIMARY KEY,
  "Name" TEXT,
  "Creation" TEXT,
  "Ranking" INTEGER,
  "Budget_in_Billions" REAL,
  "Num_Employees" REAL
)

head:
CREATE TABLE "head" (
"head_ID" INTEGER PRIMARY KEY,
  "name" TEXT,
  "born_state" TEXT,
  "age" REAL
)

management:
CREATE TABLE "management" (
"department_ID" INTEGER PRIMARY KEY,
  "head_ID" INTEGER,
  "temporary_acting" TEXT
)

Poprzednia konwersacja:

Proszę o napisanie instrukcji SQL odpowiadającej na pytanie: Ilu kierowników działów ma więcej niż 56 lat? [/INST] select count ( * ) from head where age > 56; [INST] Oto schemat bazy danych:
book_club:
CREATE TABLE "book_club" (
"book_club_id" INTEGER PRIMARY KEY,
  "Year" INTEGER,
  "Author_or_Editor" TEXT,
  "Book_Title" TEXT,
  "Publisher" TEXT,
  "Category" TEXT,
  "Result" TEXT
)

culture_company:
CREATE TABLE "culture_company" (
"Company_name" TEXT PRIMARY KEY,
  "Type" TEXT,
  "Incorporated_in" TEXT,
  "Group_Equity_Shareholding" REAL,
  "book_club_id" TEXT,
  "movie_id" TEXT
)

movie:
CREATE TABLE "movie" (
"movie_id" INTEGER PRIMARY KEY,
  "Title" TEXT,
  "Year" INTEGER,
  "Director" TEXT,
  "Budget_million" REAL,
  "Gross_worldwide" INTEGER
)

Poprzednia konwersacja:
Human: Pokaż mi filmy z 2022
AI: SELECT Title,
       Year
FROM movie
WHERE Year = "2022";
Human: Jaka jest liczba filmów rocznie?
AI: SELECT count(*)
FROM cust_order
GROUP BY Year;
Human: Pokaż mi pary filmów firma
AI: SELECT Company_name,
       Title
FROM culture_company as c
LEFT JOIN movie as m
ON c.movie_id = m.movie_id;

Proszę o napisanie instrukcji SQL odpowiadającej na pytanie: Jakie są nazwy wszystkich firm, którym odpowiada film wyreżyserowany w 1999 roku? [/INST] select culture_company.company_name from movie inner join culture_company on movie.movie_id = culture_company.movie_id where movie.year = 1999; [INST] Oto schemat bazy danych:
station:
CREATE TABLE "station" (
"id" INTEGER PRIMARY KEY,
  "name" TEXT,
  "lat" REAL,
  "long" REAL,
  "dock_count" INTEGER,
  "city" TEXT,
  "installation_date" TEXT
)

status:
CREATE TABLE "status" (
"station_id" INTEGER,
  "bikes_available" INTEGER,
  "time" TEXT,
)

trip:
CREATE TABLE "trip" (
"id" INTEGER PRIMARY KEY,
  "duration" INTEGER,
  "start_date" TEXT,
  "start_station_name" TEXT,
  "start_station_id" INTEGER,
  "end_date" TEXT,
  "end_station_name" TEXT,
  "end_station_id" INTEGER,
  "bike_id" INTEGER,
  "subscription_type" TEXT,
  "zip_code" INTEGER,
)

weather:
CREATE TABLE "weather" (
"date" TEXT,
  "max_temperature_f" INTEGER,
  "mean_temperature_f" INTEGER,
  "min_temperature_f" INTEGER,
  "mean_dew_point_f" INTEGER,
  "max_dew_point_f" INTEGER,
  "min_dew_point_f" INTEGER,
  "max_humidity" INTEGER,
  "mean_humidity" INTEGER,
  "max_sea_level_pressure_inches" REAL,
  "mean_sea_level_pressure_inches" REAL,
  "min_sea_level_pressure_inches" REAL,
  "max_visibility_miles" INTEGER,
  "mean_visibility_miles" INTEGER,
  "min_visibility_miles" INTEGER,
  "max_wind_Speed_mph" INTEGER,
  "mean_wind_speed_mph" INTEGER,
  "max_gust_speed_mph" INTEGER,
  "precipitation_inches" INTEGER,
  "cloud_cover" TEXT,
  "events" REAL,
  "wind_dir_degrees" INTEGER,
  "zip_code" INTEGER,
)

Proszę o napisanie instrukcji SQL odpowiadającej na pytanie: Jakie są identyfikatory stacji, które mają szerokość geograficzną powyżej 37,4 i nigdy nie miały dostępności rowerów poniżej 7? [/INST] select id from station where lat > 37.4 except select station_id from status group by station_id having min ( bikes_available ) < 7; [INST] Oto schemat bazy danych:
{schema}

Poprzednia konwersacja:
{{chat_history}}

Proszę o napisanie instrukcji SQL odpowiadającej na pytanie: {{question}}
Nie podawaj żadnego komentarza ani wyjaśnienia działania kodu, wystarczy instrukcja SQL zakończona średnikiem.
Odpowiedź:
"""
