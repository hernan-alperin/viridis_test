import urllib2
import os
import csv
import requests


job_codes_file = "industry-job-codes.csv"

def define_link_templates():
  """
  Define data link templates
  """

  link_templates = [None] * 7

  # Tasks
  link_templates[0] = "http://www.onetonline.org/link/table/details/tk/%s/Tasks_%s.csv?fmt=csv&s=IM&t=-10"

  # Knowledge
  link_templates[1] = "http://www.onetonline.org/link/table/details/kn/%s/Knowledge_%s?fmt=csv&s=IM&t=-10"

  # Skills
  link_templates[2] = "http://www.onetonline.org/link/table/details/sk/%s/Skills_%s?fmt=csv&s=IM&t=-10"

  # Abilities
  link_templates[3] = "http://www.onetonline.org/link/table/details/ab/%s/Abilities_%s?fmt=csv&s=IM&t=-10"

  # Work Activities
  link_templates[4] = "http://www.onetonline.org/link/table/details/wa/%s/Work_Activities_%s?fmt=csv&s=IM&t=-10"

  # Work Context
  link_templates[5] = "http://www.onetonline.org/link/table/details/cx/%s/Work_Context_%s?fmt=csv&s=IM&t=-10"

  # Job Zone
  link_templates[6] = "http://www.onetonline.org/link/table/details/jz/%s/Job_Zone_%s?fmt=csv&s=IM&t=-10"


  return link_templates





def main():

  link_templates = []

  # Get the link templates
  link_templates  = define_link_templates()

  # Current directory
  current_dir = os.path.dirname(os.path.abspath(__file__))
  data_dir = os.path.join(current_dir, 'data')


  # Open job codes file
  with open(job_codes_file, 'rb') as csvfile:
    myreader = csv.reader(csvfile, delimiter=',')
    headerline = myreader.next()

    # Iterate through job codes
    for row in myreader:
      job_code = str(row[2])
      print job_code


      my_links = []

      # Interpolate the string with the current job code
      for idx, link in enumerate(link_templates):
        my_links.append(link_templates[idx] % (job_code, job_code))


        # Target file to save downloaded csv
        filename = "%s/%s_%s.csv" % (data_dir, job_code, idx)

        # Download the file and save to disk
        url = my_links[idx]

        try:
          req = urllib2.urlopen(url)


          CHUNK = 16 * 1024
          with open(filename, 'wb') as fp:
            while True:
              chunk = req.read(CHUNK)
              if not chunk: break
              fp.write(chunk)


        except urllib2.HTTPError, e:
          print url,'not found'





# Call the main function
if __name__ == '__main__':
  main()

