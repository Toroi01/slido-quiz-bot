from bs4 import BeautifulSoup


def parse_html():
  # Path to your HTML file
  file_path = "sample2.html"  # Change this to the path of your file

  # Read the HTML content from the file
  with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

  # Parse the HTML
  soup = BeautifulSoup(html_content, "html.parser")

  # Extract the question title
  question_element = soup.find("span", class_="poll-question__title-text")
  question_title = question_element.get_text(strip=True) if question_element else "Question not found"

  # Extract all possible answers
  answers = []
  answer_elements = soup.find_all(
    "span",
    class_="MuiTypography-root MuiFormControlLabel-label MuiTypography-body1",
  )

  for answer_element in answer_elements:
    print(answer_element)
    answer_text = answer_element.get_text(strip=True)
    if answer_text:
      answers.append(answer_text)

  # Output the results
  print("Question Title:", question_title)
  print("Possible Answers:")
  for i, answer in enumerate(answers, start=1):
    print(f"{i}. {answer}")


def main():
  parse_html()


if __name__ == "__main__":
  main()
