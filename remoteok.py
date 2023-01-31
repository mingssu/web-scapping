from bs4 import BeautifulSoup
import requests

def extract_remoteok_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  results = []
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all('tr', class_="job")
    for job in jobs:
      job_posts = job.find('td', class_="company position company_and_position")
      job_information = job_posts.find('a', class_="preventLink")
      job_link = job_information['href']
      job_title = job_posts.find('h2')
      job_company = job_posts.find('h3')

      job_locations = job_posts.find_all('div', class_="location")

      locations = []
      for mark in job_locations:
        if "$" in mark.string:
          salary = mark.string
        elif "⏰" in mark.string:
          contract = mark.string
        else:
          locations.append(mark.string)
      job_result = {
        'link': "https://remoteok.com/" + job_link,
        'title': job_title.string.replace("\n", ""),
        'company': job_company.string,
        'location': ', '.join(locations)
      }
      results.append(job_result)

  else:
    print("Can't get jobs.")

  return results
