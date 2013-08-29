import sqlite3
import numpy as np
import operator



class JobScore(object):
  # Connect or create the database if it doesn't already exists
  conn = sqlite3.connect("../database/jobscores.db")

  def calculate_job_score(self,candidate_matrix, job_importance_matrix):
    """
    Iterates through available jobs to find the highest 'job score'
    """

    # Define var to return
    group_score = {}

    for k,v in candidate_matrix.iteritems():
      # Initialize a list for the candidate ranks, and the job importances for a specific grouping

      feature_keys = v.keys()


      # Get matching matrices for the candidate ranking and the job importance rating
      # Note that job importance features that do not match up to available candidate ranking are thrown out
      c_row = [v.setdefault(feature_key,0) for feature_key in feature_keys]


      job_v = job_importance_matrix[k]
      j_row = [job_v.setdefault(feature_key,0) for feature_key in feature_keys]


      c_row = np.mat(c_row)
      j_row = np.mat(j_row)

      # Calculate the dot product of the candidate's rank vs the job feature importance
      group_score[k] = np.dot(c_row, j_row.T)


    # The sum of the group_score elements should give a good numerical assessment of how close a candidate fits a particular job
    total_job_score = int(sum(group_score.values()))
    return total_job_score


  def generate_job_importance_matrix(self,job_code):

    # Define the job_features
    job_feature_groups = {
        0: 'Tasks',
        1: 'Knowledge',
        2: 'Skills',
        3: 'Abilities',
        4: 'Work_Activities',
        5: 'Work_Context',
        5: 'Job_Zone'
        }

    # define return var
    job_importance_matrix = {}


    groups = job_feature_groups.keys()

    for group in groups:
      # Iterate through each group and get the job_feature

      cursor = self.conn.execute("SELECT job_feature_description, job_feature_value FROM job_feature WHERE job_code=? AND job_feature_group=?", (job_code,group))

      # Match format of the candidate matrix
      job_importance_matrix[group]= dict(cursor.fetchall())





    return job_importance_matrix


  def find_best_match_jobs(self,candidate_matrix):
    """
    return a list of the top 5 jobs best suited for a candidate
    """

    """
    Example format for input:
    candidate_matrix =
     {
       0: {"This is a skill description": 10, "This is another skill description": 7},
       1: {"This is a knowledge description" : 8, "This is another knowledge description": 6}
      }
    """






    # Get a list of all job codes to begin importing details for
    cursor = self.conn.execute("SELECT job_code FROM job")

    # Get python list of all job codes
    job_codes = cursor.fetchall()


    job_score = {}

    for job_code in job_codes:
      job_code = job_code[0]
      job_importance_matrix = self.generate_job_importance_matrix(job_code)


      job_score[job_code] = self.calculate_job_score(candidate_matrix, job_importance_matrix)


    # Sort by job scores!
    sorted_jobs = sorted(job_score.iteritems(), key=operator.itemgetter(1))

    # Get in descending order
    sorted_jobs.reverse()

      # Return the jobs with the top 5 job scores for the candidate
    return sorted_jobs[:5]






