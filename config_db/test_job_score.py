
import job_score



candidate_matrix = {

    3: {
      "The ability to quickly move the arms and legs.":8, #50 importance
      "The ability to identify and understand the speech of another person.":4 #53 importance
    },
    2: {
      "Talking to others to convey information effectively.":7, #47 importance
      "Adjusting actions in relation to others' actions.":6, #44 importance

      }
}


def main():

  import pdb
  pdb.set_trace()

  js = job_score.JobScore()

  myjobs = js.find_best_match_jobs(candidate_matrix)
  print myjobs




if __name__ == '__main__':
  main()
