import requests
from bs4 import BeautifulSoup
from openai_client_handler import get_openai_client

def fetch_website_content(url):
    """
    Fetches and returns the text content from a website URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the HTML content. Adjust as necessary.
        text = ' '.join(soup.stripped_strings)
        return text
    else:
        print(f"Failed to access {url}")
        return ""

def summarize_content(content, max_length=300):
    """
    Summarizes the content to fit within a specified maximum length.
    This is a simplistic approach; more sophisticated methods may be used.
    """
    if len(content) <= max_length:
        return content
    else:
        return content[:max_length] + "..."

def analyze_with_ai(model, prompt):
    """
    Sends the prompt to the AI for analysis and prints the response.
    This function is a placeholder; you should implement it according to your AI model's API.
    """
    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(model=model, messages=[{"role": "system", "content": prompt}])
    print(response.choices[0].message.content)

def website_content_analysis(url, model):
    print(f"Analyzing content from: {url}")
    website_content = fetch_website_content(url)
    summarized_content = summarize_content(website_content)
    print("website content:", website_content)
    print("summarized_content:", summarized_content)
    analyze_with_ai(model, f"Analyze the following content from a website: {summarized_content}")

if __name__ == "__main__":
    url = "https://example.com"
    website_content = fetch_website_content(url)
    summarized_content = summarize_content(website_content)
    prompt = f"Analyze the following content from a website: {summarized_content}"
    analyze_with_ai("gpt-3.5-turbo", prompt)  # Adjust the model parameter as necessary.