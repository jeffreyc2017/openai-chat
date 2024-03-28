import requests
from bs4 import BeautifulSoup
from helpers.openai_client_handler import get_openai_client

tool_get_website_content = {
    "type": "function",
    "function": {
        "name": "get_website_content",
        "description": "Get the website content",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL of a website with scheme.",
                },
                "full_content": {
                    "type": "boolean",
                    "description": "The boolean value True or False."
                }
            },
        },
    },
}

def get_website_content(args):
    url = args.get("url", None)
    if url:
        full_content = args.get("full_content", False)
        return fetch_website_content(url, full_content)

    return ""

def fetch_website_content(url, full_content=False):
    """
    Fetches and returns the text content from a website URL.
    """
    # Ensure the URL includes a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url  # Defaulting to http for simplicity; consider https when appropriate

    try:
        response = requests.get(url)
        if response.status_code == 200:
            if full_content:
                return response.text

            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from the HTML content. Adjust as necessary.
            text = ' '.join(soup.stripped_strings)
            return text
        else:
            print(f"Failed to access {url}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
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

def compose_prompt(url):
    website_content = fetch_website_content(url)
    summarized_content = summarize_content(website_content)
    print("website content:", website_content)
    print("summarized_content:", summarized_content)
    return f"Analyze the following content from a website: {summarized_content}"

def website_content_analysis(url, model):
    print(f"Analyzing content from: {url}")
    analyze_with_ai(model, compose_prompt(url))

if __name__ == "__main__":
    website_content_analysis("https://example.com", "gpt-3.5-turbo")
