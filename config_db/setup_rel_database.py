import sqlite3
import sys

import csv


class DBSetup(object):

  # Connect or create the database if it doesn't already exists
  conn = sqlite3.connect("../database/jobscores.db")


  def get_job_features_from_files(self,job_code, job_feature_group_code):
    """
    Finds file(s) corresponding to a job code
    """

    # Get the file name for a specific category
    filename = job_code + "_" + job_feature_group_code + ".csv"

    #define var to return
    job_features = []

    try:
      # Open job features file on disk
      with open("../data/" + filename, 'rb') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        headerline = myreader.next()


        try:

          # Iterate through job codes
          for row in myreader:
            job_feature_value = row[0]
            job_feature_category = row[1]
            job_feature_description = row[2]

            # Create job_feature object
            job_feature = [job_code, job_feature_group_code,job_feature_category, job_feature_description, job_feature_value]
            job_features.append(job_feature)
        except Exception, e:
          import pdb
          pdb.set_trace()

          print e


    except IOError:
      # Why this exception not raised?
      print 'file not found'

    return job_features



  def import_job_features(self):
    """
    Iterates through a list of files and imports all the data to the specified table in the database
    """

    # Define the job_features
    '''
    job_feature_groups = {
        0: 'Tasks',
        1: 'Knowledge',
        2: 'Skills',
        3: 'Abilities',
        4: 'Work_Activities',
        5: 'Work_Context',
        6: 'Job_Zone'
    }
    '''

    job_feature_groups = {
        0: 'Tasks',
        1: 'Knowledge',
        2: 'Skills',
        3: 'Abilities'
    }


    # Get a list of all job codes to begin importing details for
    res = self.conn.execute("SELECT job_code FROM job")

    # Get python list
    job_codes = res.fetchall()


    # Iterate through each unique job code identified in the job table
    for job_code_tuple in job_codes:

      # Get the first element of the tuple job_code
      job_code = job_code_tuple[0]

      # Get the job_feature contents for each csv file
      for g in job_feature_groups.keys():



        job_feature_group_code = str(g)
        job_features = self.get_job_features_from_files(job_code, job_feature_group_code)


        # Ignore cases where features not found for te job_code
        if len(job_features):
          # read the data from the file
          # import the list of job features into the database

          # Insert the data into the job definition table
          self.conn.executemany("insert into job_feature values (?,?,?,?,?)", job_features)

          # commit to the database
          self.conn.commit()



  def import_job(self):
    filename = "../industry-job-codes.csv"



    with open(filename, 'r') as csvfile:

      myreader = csv.reader(csvfile, delimiter=',')
      headerline = myreader.next()


      full_data = []


      # Iterate through job codes
      for row in myreader:
        industry_name = row[0]
        job_code = row[2]
        job_name = row[3]

        full_data.append((job_code, job_name, industry_name))




    # Insert the data into the job definition table
    self.conn.executemany("insert into job values (?,?,?)", full_data)

    # commit to the database
    self.conn.commit()






def main():
  """
  Logic & Flow
  """

  db = DBSetup()

  if sys.argv[1] == 'job':
    # Import the job/industry/job-code data into the 'job' table
    db.import_job()
  elif sys.argv[1] == 'job_feature':
    # Import the features (skills, knowledge, etc) required for each job and the importance score
    db.import_job_features()
  elif sys.argv[1] == 'job_feature_details':
    pass

  #close the db connection
  db.conn.close()

if __name__ == '__main__':
  main()
