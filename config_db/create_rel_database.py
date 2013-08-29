import sqlite3


def create_database():
  """
  Creates the database and tables, if they don't already exists
  """

  # Create the database if it doesn't already exists
  conn = sqlite3.connect("../database/jobscores.db")


  # Create a table that matches the industry to its jobs

  # Create table
  #conn.execute('''CREATE TABLE job
  #             (job_code varchar unique, job_name varchar, industry_name varchar)''')

  # Create a table that matches each job to unique job feautre identifier
  conn.execute('''CREATE TABLE job_feature
               (job_code varchar, job_feature_group varchar, job_feature_category varchar,
                job_feature_description text, job_feature_value integer)''')

  # Create a table that matches job features to a unique index
  #conn.execute('''CREATE TABLE job_feature_details
  #             (job_feature_code varchar unique, job_feature_category varchar, job_feature_description text)''')


def main():
  """
  Logic & Flow
  """


  create_database()



if __name__ == '__main__':
  main()

