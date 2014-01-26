

code = '3303'

detail_link = "http://www.onetonline.org/link/details/" + code
job_codes_file = "industry-job-codes.csv"


tasks_link_template = "http://www.onetonline.org/link/table/details/tk/%s/Tasks_%s.csv?fmt=csv&s=IM&t=-10"
knowledge_link_template = "http://www.onetonline.org/link/table/details/kn/%s/Knowledge_%s?fmt=csv&s=IM&t=-10"


def main():


  # Open job codes file
  with open(job_codes_file, 'rb') as csvfile:
    myreader = csv.reader(csvfile, delimiter=',')

    # Iterate through job codes
    for row in myreader:
      job_code = myreader[2]
      print job_code

      tasks_link = tasks_link_template % (job_code, job_code)





